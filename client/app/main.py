import sys
import time
import json
import redis
import config
import inputs
import logging
import RPi.GPIO as GPIO
from drive import Drive
from subprocess import call

logging.info("Main process is starting ... ")
logging.debug("Warning: Debugging is enabled.")

# Setup redis
db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

# Instantiate driving class
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.SERVO_PIN, GPIO.OUT)
driving = Drive(config.SERVO_PIN, config.servo_angles)

# Check connection with gamepad
pads = inputs.devices.gamepads
if len(pads) == 0:
    raise Exception("Could not find gamepads!")

# Cache for outputs from gamepad
output_dict = {"BTN_TL": 0, "BTN_TR": 0, "ABS_RX": 0, "ABS_Y": 0, "BTN_EAST": 0}

# Start
time.sleep(config.MAIN_SLEEP_TIME)
logging.info("Main process is ready!")
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
                    db.set(config.GAMEPAD, json.dumps(output_dict))  # update_cache

except KeyboardInterrupt:
    driving.disable()
    time.sleep(config.MAIN_SLEEP_TIME)
    GPIO.cleanup()
    sys.exit()
