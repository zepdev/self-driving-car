import sys
import time
import json
import redis
import base64
import config
import logging
import datetime
from PIL import Image
from io import BytesIO
import RPi.GPIO as GPIO
from nanocamera import Camera


class Record():
    def __init__(self, triggers, echos, cam_res=None):
        # resolution has to be a multiple of 32 (32*7 =224)

        if cam_res is None:
            cam_res = [224, 224]
        self.TRIGGERS = triggers
        self.ECHOS = echos

        # Initialize pins
        GPIO.setmode(GPIO.BCM)
        for pin in self.TRIGGERS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        for pin in self.ECHOS:
            GPIO.setup(pin, GPIO.IN)

        self.camera = Camera(device_id=0, flip=0, width=cam_res[0], height=cam_res[1], fps=30)

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
    def _convert_time(current_time):
        # time is generated with datetime.datetime.now()
        iso = current_time.isoformat(sep="_")
        iso = '-'.join(iso.split(':'))
        iso = iso.replace('.', '-')
        # Example: 2020-04-14_12-44-41-296481
        return iso

    def record(self, out_dict):
        current_time = self._convert_time(datetime.datetime.now())
        
        # picture
        # TODO: change this back
        # np_image = self.camera.read()
        # img = Image.fromarray(np_image).convert('RGB')
        img = Image.open("models/test-pic.jpg")
        stream = BytesIO()
        img.save(stream, format='jpeg')
        pic_binary = base64.b64encode(stream.getvalue())
        pic_str = pic_binary.decode("utf-8")
        
        # gamepad
        out = {"ABS_RX": round((out_dict["ABS_RX"]+0.5)/32767.5, 1), "ABS_Y": -round((out_dict["ABS_Y"]+0.5)/32767.5, 1)}
                
        # distances
        dists = {}
        for i in range(len(self.TRIGGERS)):
            dists[f"dist_{i}"] = self._measure_distance(self.TRIGGERS[i], self.ECHOS[i])

        recordings = {"ts": current_time, "pic": pic_str, "dist": dists, "out": out}
        return recordings


if __name__ == "__main__":

    logging.info("Recording process is starting ... ")
    logging.debug("Warning: Debugging is enabled.")
    time.sleep(config.START_SLEEP_TIME)

    # Initialize redis
    db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

    # Instantiate Record class
    recording = Record(config.TRIGGERS, config.ECHOS)

    # Start
    logging.info("Recording process is ready!")
    time.sleep(config.MAIN_SLEEP_TIME)
    
    try:
        while True:

            # Get current output_dict
            pad = db.get(config.GAMEPAD)
            if pad is None:
                continue
            else:
                output_dict = json.loads(pad)

            # Record if requested
            if output_dict["BTN_TL"] == 1 and output_dict["BTN_TR"] == 1:
                recs = recording.record(output_dict)
                db.rpush(config.QUEUE_NAME, json.dumps(recs))
                logging.debug("Sent recordings to redis queue.")

            time.sleep(config.RECORD_SLEEP_TIME)

    except KeyboardInterrupt:
        time.sleep(config.MAIN_SLEEP_TIME)
        GPIO.cleanup()
        sys.exit()
