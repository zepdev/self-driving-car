import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

sleep_time_short = 0.5
sleep_time_long = 2

#range: 3.5 - 11
MIN_ANGLE = 5.5
MAX_ANGLE = 8.5

def stear(x):
	"""
	
	:param x: float between 0 and 1
	"""
	
	angle = MIN_ANGLE + x*(MAX_ANGLE-MIN_ANGLE)
	return angle


led = GPIO.PWM(18,50)
led.start(7) #middle
time.sleep(sleep_time_long)


for t in range(0, 11):
	p = stear(float(t%2))
	if t%10 == 0:
		print(p)
	led.ChangeDutyCycle(p)
	time.sleep(sleep_time_long)

led.ChangeDutyCycle(7)
time.sleep(sleep_time_short)

led.stop()
time.sleep(sleep_time_short)
GPIO.cleanup()
