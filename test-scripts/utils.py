import RPi.GPIO as GPIO
import time

def measure_distance(trigger, echo):
	GPIO.output(trigger, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(trigger, GPIO.LOW)

	while GPIO.input(echo) == 0:
		pulse_start_time = time.time()
	while GPIO.input(echo) == 1:
		pulse_end_time = time.time()
			
	pulse_duration = pulse_end_time - pulse_start_time

	distance = round(pulse_duration * 17150, 2)

	return distance
