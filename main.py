import sys
import time
import inputs
import random
import RPi.GPIO as GPIO
from record import Record
from drive import Drive
from subprocess import call

#initialize pins
#######CHOOSE PINS WHICH ARE NOT USED BY MOTOR DRIVER HAT#########
GPIO.setmode(GPIO.BCM)
TRIGGER_1 = 20
GPIO.setup(TRIGGER_1, GPIO.OUT)
TRIGGER_2 = 21
GPIO.setup(TRIGGER_2, GPIO.OUT)
TRIGGER_3 = 22
GPIO.setup(TRIGGER_3, GPIO.OUT)

ECHO_1 = 23
GPIO.setup(ECHO_1, GPIO.IN)
ECHO_2 = 24
GPIO.setup(ECHO_2, GPIO.IN)
ECHO_3 = 25
GPIO.setup(ECHO_3, GPIO.IN)

SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)

#instantiate driving class
driving = Drive(SERVO_PIN)

#instantiate record class
TRIGGERS = [TRIGGER_1]#, TRIGGER_2, TRIGGER_3]
ECHOS = [ECHO_1]#, ECHO_2, ECHO_3]
recording = Record(TRIGGERS, ECHOS)

pads = inputs.devices.gamepads
if len(pads) == 0:
	raise Exception("Could not find Gamepads!")

output_dict = {"BTN_TL": 0, "BTN_TR": 0, "ABS_RX": 0, "ABS_Y": 0, "BTN_EAST": 0}

SLEEP_TIME = 1
time.sleep(SLEEP_TIME)


try:
    while True:
        events = inputs.get_gamepad()
        for event in events:
	    if event.code == "BTN_MODE":
		call("sudo poweroff", shell = True)
            if event.code in output_dict.keys():
                output_dict[event.code] = event.state
                end = time.time()
                if output_dict["BTN_EAST"] == 1:
                    pass
                else:
                    driving.drive(output_dict)

                if output_dict["BTN_TL"] == 1 and output_dict["BTN_TR"] == 1 and random.random() < 0.025:
                    recording.record(output_dict)

except KeyboardInterrupt:
	driving.disable()
	time.sleep(SLEEP_TIME)
	GPIO.cleanup()
	sys.exit()
