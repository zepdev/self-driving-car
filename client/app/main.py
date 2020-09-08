import sys
import time
import json
import redis
import config
import inputs
import logging
import RPi.GPIO as GPIO
from drive import Motor, Drive
from subprocess import call

logging.info("Main process is starting ... ")
logging.debug("Warning: Debugging is enabled.")
time.sleep(config.START_SLEEP_TIME)

# Setup redis
db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

# Instantiate motor and driving class
GPIO.setmode(GPIO.BCM)  # BCM = GPIO PIN-numbering (NOT BOARD-Numbering)
motor = Motor(config.PWM_PIN, config.EN_PIN, config.DIR_PIN, config.FLT_PIN)
driving = Drive(config.SERVO_PIN, config.servo_angles, motor, config.MAX_SPEED)

# Check connection with gamepad
pads = inputs.devices.gamepads
if len(pads) == 0:
    raise Exception("Could not find gamepads!")

# Cache for outputs from gamepad
output_dict = {"BTN_TL": 0, "BTN_TR": 0, "ABS_RX": 0, "ABS_Y": 0, "BTN_EAST": 0, "BTN_NORTH": 1}

# Start
logging.info("Main process is ready!")
time.sleep(config.MAIN_SLEEP_TIME)

try:
    while True:

        # Read all inputs from gamepad
        events = inputs.get_gamepad()  # INFO: THIS BLOCKS UNTIL AN EVENT COMES !!!

        for event in events:
            # Check if shutdown is requested
            if event.code == "BTN_MODE":
                driving.disable()
                time.sleep(config.MAIN_SLEEP_TIME)
                GPIO.cleanup()
                call("sudo poweroff", shell=True)

            if event.code in output_dict.keys():
                output_dict[event.code] = event.state  # update
                db.set(config.GAMEPAD, json.dumps(output_dict))  # update redis cache
                if output_dict["BTN_EAST"] == 0:
                    driving.drive(output_dict)  # drive, otherwise self-driving is enabled


except KeyboardInterrupt:
    driving.disable()
    time.sleep(config.MAIN_SLEEP_TIME)
    GPIO.cleanup()
    sys.exit()
