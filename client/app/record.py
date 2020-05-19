import time
import datetime
import base64
from io import BytesIO
import RPi.GPIO as GPIO
from picamera import PiCamera


class Record():
    def __init__(self, triggers, echos, cam_res=None):
        # resolution has to be a multiple of 32 (32*7 =224)
        if cam_res is None:
            cam_res = [224, 224]
        self.TRIGGERS = triggers
        self.ECHOS = echos
        
        self.camera = PiCamera()
        self.camera.resolution = tuple(cam_res)

        # Allow some time for the initialization
        time.sleep(2)
        
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

    @staticmethod
    def _convert_time(time):
        # time is generated with datetime.datetime.now()
        iso = time.isoformat(sep="_")
        iso = '-'.join(iso.split(':'))
        iso = iso.replace('.', '-')
        # Example: 2020-04-14_12-44-41-296481
        return iso

    def record(self, output_dict):
        recs = []
        current_time = self._convert_time(datetime.datetime.now())
        
        # picture
        stream = BytesIO()
        self.camera.capture(stream, 'jpeg')
        pic_binary = base64.b64encode(stream.getvalue())
        pic_str = pic_binary.decode("utf-8")
        
        # gamepad
        out = {"ABS_RX": round((output_dict["ABS_RX"]+0.5)/32767.5, 1), "ABS_Y": -round((output_dict["ABS_Y"]+0.5)/32767.5, 1)}
                
        # distances
        dists = {}
        for i in range(len(self.TRIGGERS)):
            dists["dist_{0}".format(i)] = self._measure_distance(self.TRIGGERS[i], self.ECHOS[i])

        recs.append({"ts": current_time, "pic": pic_str, "dist": dists, "out": out})
        return recs
