import sys
import time
import json
import redis
import config
import inputs
import random
import logging
import RPi.GPIO as GPIO
from record import Record
from drive import Drive
from subprocess import call

logging.info("Initializing ... ")
logging.debug("Warning: Debugging is enabled.")

# Setup redis
db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

# Initialize pins
#######CHOOSE PINS WHICH ARE NOT USED BY MOTOR DRIVER HAT#########
GPIO.setmode(GPIO.BCM)
TRIGGER_1 = 21 # 20
GPIO.setup(TRIGGER_1, GPIO.OUT)
# TRIGGER_2 = 21
# GPIO.setup(TRIGGER_2, GPIO.OUT)
# TRIGGER_3 = 22
# GPIO.setup(TRIGGER_3, GPIO.OUT)

ECHO_1 = 24 # 23
GPIO.setup(ECHO_1, GPIO.IN)
# ECHO_2 = 24
# GPIO.setup(ECHO_2, GPIO.IN)
# ECHO_3 = 25
# GPIO.setup(ECHO_3, GPIO.IN)

# TODO: DO we need that line or can it be deleted?
# GPIO.output(TRIGGER_1, GPIO.LOW)

SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Instantiate driving class
driving = Drive(SERVO_PIN)

# Instantiate record class
TRIGGERS = [TRIGGER_1]  # , TRIGGER_2, TRIGGER_3]
ECHOS = [ECHO_1]  # , ECHO_2, ECHO_3]
recording = Record(TRIGGERS, ECHOS)

# Check connection with gamepad
pads = inputs.devices.gamepads
if len(pads) == 0:
    raise Exception("Could not find gamepads!")

# Cache for outputs from gamepad
output_dict = {"BTN_TL": 0, "BTN_TR": 0, "ABS_RX": 0, "ABS_Y": 0, "BTN_EAST": 0}

# Sleep before starting
SLEEP_TIME = 1
time.sleep(SLEEP_TIME)

# Start
logging.info("Ready!")

# TODO: This is just for testing.
recs = recording.record(output_dict)
db.rpush(config.QUEUE_NAME, json.dumps(recs))
logging.debug("Sent recordings to redis queue.")

try:
    while True:

        # Read inputs from gamepad
        events = inputs.get_gamepad()

        for event in events:

            # Check if shutdown is requested
            if event.code == "BTN_MODE":
                call("sudo poweroff", shell=True)

            if event.code in output_dict.keys():

                # update Cache
                output_dict[event.code] = event.state

                if output_dict["BTN_EAST"] == 1:
                    pass  # self-drive
                else:
                    driving.drive(output_dict)  # manual driving

                if output_dict["BTN_TL"] == 1 and output_dict["BTN_TR"] == 1 and random.random() < 0.025:
                    recs = recording.record(output_dict)  # record current state
                    db.rpush(config.QUEUE_NAME, json.dumps(recs))
                    logging.debug("Sent recordings to redis queue.")

except KeyboardInterrupt:
    driving.disable()
    time.sleep(SLEEP_TIME)
    GPIO.cleanup()
    sys.exit()
