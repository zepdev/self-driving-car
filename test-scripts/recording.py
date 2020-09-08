import inputs
import sys
import RPi.GPIO as GPIO
import time
import random

SLEEP_TIME_SHORT = 0.5
SLEEP_TIME_LONG = 2






print('Starting ...')
pads = inputs.devices.gamepads
if len(pads) == 0:
	raise Exception("Could not find Gamepads!")

time.sleep(SLEEP_TIME_LONG)
print('Ready!')

input_dict = {"BTN_TL": 0, "BTN_TR": 0, "ABS_RX": 0, "ABS_Y": 0}
input_btns = ("BTN_TL", "BTN_TR", "ABS_RX", "ABS_Y")

training_data = {}
try:
	while True:
		events = inputs.get_gamepad()
		for event in events:
			if event.code in input_btns:
				input_dict[event.code] = event.state
			if input_dict["BTN_TL"] == 1 and input_dict["BTN_TR"] == 1 and random.random() < 0.01:
			    print(input_dict, time.time())
			

except KeyboardInterrupt:
	print(input_dict)
	sys.exit()
