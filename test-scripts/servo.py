import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

sleep_time_short = 0.5
sleep_time_long = 2

#range: 3.5 - 11
MIN_ANGLE = 4.5
MAX_ANGLE = 9

def stear(x):
	"""
	
	:param x: float between 0 and 1
	"""
	
	angle = MIN_ANGLE + x*(MAX_ANGLE-MIN_ANGLE)
	return angle


led = GPIO.PWM(12,50)
led.start(7) #middle
time.sleep(sleep_time_short)
led.ChangeDutyCycle(9)
time.sleep(sleep_time_short)
led.ChangeDutyCycle(4.5)
time.sleep(sleep_time_short)
led.ChangeDutyCycle(7)
time.sleep(sleep_time_short)

led.stop()
time.sleep(sleep_time_short)
GPIO.cleanup()
