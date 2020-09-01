import sys
import time
import json
import redis
import config
import inputs
import logging
import RPi.GPIO as GPIO
from drive import Motor, Drive
from autopilot import Autopilot
from subprocess import call

logging.info("Main process is starting ... ")
logging.debug("Warning: Debugging is enabled.")

# Setup redis
db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

# Instantiate motor and driving class
GPIO.setmode(GPIO.BCM)  # BCM = GPIO PIN-numbering (NOT BOARD-Numbering)
GPIO.setup(config.SERVO_PIN, GPIO.OUT)
motor = Motor()  # could give pins here
driving = Drive(config.SERVO_PIN, config.servo_angles)

# Instantiate autopilot
autopilot = Autopilot(model_path=config.model_path)

# Check connection with gamepad
pads = inputs.devices.gamepads
if len(pads) == 0:
    raise Exception("Could not find gamepads!")

# Cache for outputs from gamepad
output_dict = {"BTN_TL": 0, "BTN_TR": 0, "ABS_RX": 0, "ABS_Y": 0, "BTN_EAST": 0}
autopilot_active = False

# Start
time.sleep(config.START_SLEEP_TIME)
logging.info("Main process is ready!")

try:
    while True:

        # Read all inputs from gamepad
        events = inputs.get_gamepad()

        # autopilot
        if len(events) == 0:
            if output_dict["BTN_EAST"] == 1:
                output_dict = autopilot.predict(output_dict)
                driving.drive(output_dict)
                autopilot_active = True
            if (output_dict["BTN_EAST"] == 0) and autopilot_active:
                output_dict["ABS_RX"] = 0
                output_dict["ABS_Y"] = 0
                autopilot_active = False
            continue

        for event in events:

            # Check if shutdown is requested
            if event.code == "BTN_MODE":
                driving.disable()
                time.sleep(config.MAIN_SLEEP_TIME)
                GPIO.cleanup()
                call("sudo poweroff", shell=True)

            # update output_dict
            if event.code in output_dict.keys():
                output_dict[event.code] = event.state  # update
                driving.drive(output_dict)  # drive
                db.set(config.GAMEPAD, json.dumps(output_dict))  # update redis cache

except KeyboardInterrupt:
    driving.disable()
    time.sleep(config.MAIN_SLEEP_TIME)
    GPIO.cleanup()
    sys.exit()
