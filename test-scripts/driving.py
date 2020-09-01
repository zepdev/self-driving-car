import inputs
import sys
import RPi.GPIO as GPIO
import time

SLEEP_TIME_SHORT = 0.5
SLEEP_TIME_LONG = 2

#range: 3.5 - 11
SERVO_MIN_ANGLE = 5.5
SERVO_MIDDLE_ANGLE = 7
SERVO_MAX_ANGLE = 8.5


def steer(x):
	"""
	:param x: float between -1 and 1
	"""
	angle = SERVO_MIN_ANGLE + (x + 1)*(SERVO_MAX_ANGLE-SERVO_MIN_ANGLE) / 2
	return angle


print('Starting ...')
pads = inputs.devices.gamepads
if len(pads) == 0:
	raise Exception("Could not find Gamepads!")

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
servo = GPIO.PWM(18,50)
servo_angle = SERVO_MIDDLE_ANGLE
servo.start(servo_angle)

#GPIO.setup(4, GPIO.OUT)
#motor = GPIO.PWM(4,50)
#motor_speed = 0
#motor.start(motor_speed)

time.sleep(SLEEP_TIME_LONG)
print('Ready!')


try:
	while True:
		events = inputs.get_gamepad()
		for event in events:
			#if event.code in ["ABS_Y", "ABS_RX"]:
			#	print(event.code, round((event.state+0.5)/32767.5, 1))
			if event.code == "ABS_RX":
				servo_angle = steer(-round((event.state+0.5)/32767.5, 1)) 
			servo.ChangeDutyCycle(servo_angle)
			#if event.code == "ABS_Y":
				#motor_speed = blablabla
			#motor.ChangeDutyCycle(motor_speed)

except KeyboardInterrupt:
	servo.ChangeDutyCycle(SERVO_MIDDLE_ANGLE)
	time.sleep(SLEEP_TIME_SHORT)
	servo.stop()
	time.sleep(SLEEP_TIME_SHORT)
	GPIO.cleanup()
	sys.exit()
