import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 20
PIN_ECHO = 18

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)
time.sleep(0.5)

try:
	while True:
		GPIO.output(PIN_TRIGGER, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRIGGER, GPIO.LOW)

		while GPIO.input(PIN_ECHO) == 0:
			pulse_start_time = time.time()
		while GPIO.input(PIN_ECHO) == 1:
			pulse_end_time = time.time()
			
		pulse_duration = pulse_end_time - pulse_start_time

		distance = round(pulse_duration * 17150, 2)

		print("Distance: {} cm".format(distance))
		time.sleep(0.5)
except:
	GPIO.cleanup()
