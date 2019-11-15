import RPi.GPIO as GPIO
import time
import datetime
import inputs
import json
from picamera import PiCamera

class Record():
	
	def __init__(self, triggers, echos):
		
		self.nbr_dists = len(triggers)

		self.TRIGGERS = triggers
		self.ECHOS = echos
		
		self.camera = PiCamera()
		self.camera.resolution = (224, 224)
		
	@staticmethod
	def _measure_distance(trigger, echo):
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
	
	
	def record(self, output_dict):
		ts = datetime.datetime.now()
		
		#picture
		self.camera.capture("pictures/self_driving={0}/{1}.jpg".format(output_dict["BTN_EAST"], ts))
		
		#outputs
		out = {"ABS_RX": round((output_dict["ABS_RX"]+0.5)/32767.5, 1), "ABS_Y": -round((output_dict["ABS_Y"]+0.5)/32767.5, 1)}
		with open("output/{}.json".format(ts), "w") as f:
			json.dump(out, f)
			
		#distances
		dists = {}
		for i in self.nbr_dists:
			dists["distance_{}".format(i): self._measure_distance(self.TRIGGERS[i], self.ECHOS[i])]

		
		dists = {"distance_1": distance_1, "distance_2": distance_2, "distance_3": distance_3}
		with open("distance/{}.json".format(ts), "w") as f:
			json.dump(dists, f)
