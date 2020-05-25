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

logging.info("Main process is starting ... ")
logging.debug("Warning: Debugging is enabled.")

# Initialize pins
GPIO.setmode(GPIO.BCM)
for pin in config.TRIGGERS + config.ECHOS:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(config.SERVO_PIN, GPIO.OUT)

# Setup redis
db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

# Instantiate driving class
driving = Drive(config.SERVO_PIN)

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
logging.info("Main process is ready!")
try:
    while True:

        # Read inputs from gamepad
        events = inputs.get_gamepad()

        for event in events:

            # Check if shutdown is requested
            if event.code == "BTN_MODE":
                call("sudo poweroff", shell=True)

            # Update output_dict and give new commands for driving
            if event.code in output_dict.keys():

                # update Cache
                output_dict[event.code] = event.state

                if output_dict["BTN_EAST"] == 1:
                    pass  # self-drive
                else:
                    driving.drive(output_dict)  # manual driving
                    db.publish(config.CHANNEL_GAMEPAD, json.dumps(output_dict))

except KeyboardInterrupt:
    driving.disable()
    time.sleep(SLEEP_TIME)
    GPIO.cleanup()
    sys.exit()
