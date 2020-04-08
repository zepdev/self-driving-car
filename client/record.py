import time
import json
import datetime
import RPi.GPIO as GPIO
from picamera import PiCamera


class Record():
	
	def __init__(self, triggers, echos, rec_path, cam_res=(224, 224)):
		
		self.nbr_dists = len(triggers)

		self.TRIGGERS = triggers
		self.ECHOS = echos
		
		self.camera = PiCamera()
		self.camera.resolution = cam_res

		self.rec_path = rec_path
		
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
		
		# picture
		self.camera.capture("{0}/pictures/{1}.jpg".format(self.rec_path, ts))
		
		# outputs
		out = {"ABS_RX": round((output_dict["ABS_RX"]+0.5)/32767.5, 1), "ABS_Y": -round((output_dict["ABS_Y"]+0.5)/32767.5, 1)}
		with open("{0}/outputs/{1}.json".format(self.rec_path, ts), "w") as f:
			json.dump(out, f)
			
		# distances
		dists = {}
		for i in range(self.nbr_dists):
			dists["dist_{}".format(i)] = self._measure_distance(self.TRIGGERS[i], self.ECHOS[i])

		with open("{0}/distances/{1}.json".format(self.rec_path, ts), "w") as f:
			json.dump(dists, f)
