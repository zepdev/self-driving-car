import sys
import json
import time
import redis
import config
import logging
import numpy as np
import RPi.GPIO as GPIO
from drive import Motor, Drive
from nanocamera import Camera
import tflite_runtime.interpreter as tflite


class Autopilot():

    def __init__(self, model_path, cam_res=None):

        # camera
        if cam_res is None:
            cam_res = [224, 224]
        self.camera = Camera(device_id=0, flip=0, width=cam_res[0], height=cam_res[1], fps=30)

        # load model
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        _,  self.height, self.width, _ = self.input_details[0]['shape']
        self.output_shape = self.output_details[0]['shape'][1]

    def predict(self, output_dict):

        #stream = BytesIO()
        #self.camera.capture(stream, 'jpeg')
        #image = Image.open(stream).convert('RGB').resize((self.width, self.height), Image.ANTIALIAS)
        #image = np.array(image)
        image = self.camera.read()
        image = image.astype(np.float32)
        image = np.expand_dims(image, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        if self.output_shape == 2:
            speed = (output_data[0][1] + 1) * 0.5
            output_dict["ABS_Y"] = speed
        else:  # self.output_shape == 1
            output_dict["ABS_Y"] = 0.5
        steering = output_data[0][0]
        output_dict["ABS_RX"] = steering

        return output_dict


if __name__ == "__main__":

    logging.info("Autopilot process is starting ... ")
    logging.debug("Warning: Debugging is enabled.")

    # Initialize redis
    db = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.DB_ID)

    # Instantiate autopilot
    autopilot = Autopilot(model_path=config.model_path)

    # Instantiate motor and driving class
    GPIO.setmode(GPIO.BCM)  # BCM = GPIO PIN-numbering (NOT BOARD-Numbering)
    motor = Motor(config.PWM_PIN, config.EN_PIN, config.DIR_PIN, config.FLT_PIN)
    driving = Drive(config.SERVO_PIN, config.servo_angles, motor, config.MAX_SPEED)

    # Start
    time.sleep(config.START_SLEEP_TIME)
    logging.info("Autopilot process is ready!")

    try:
        while True:

            # Get current output_dict
            pad = db.get(config.GAMEPAD)
            if pad is None:
                continue
            else:
                output_dict = json.loads(pad)

            # Drive autonomously if requested
            if output_dict["BTN_EAST"] == 1:
                print("hello")
                time.sleep(0.5)
                # output_dict = autopilot.predict(output_dict)
                # driving.drive(output_dict)

            # stop script
            if output_dict["BTN_NORTH"] == 1:
                time.sleep(config.MAIN_SLEEP_TIME)
                sys.exit(0)

    except KeyboardInterrupt:
        time.sleep(config.MAIN_SLEEP_TIME)
        GPIO.cleanup()
        sys.exit(0)
