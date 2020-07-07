from PIL import Image
from io import BytesIO
import numpy as np
from picamera import PiCamera
import tflite_runtime.interpreter as tflite


class Autopilot():

    def __init__(self, model_name, cam_res=None):

        # camera
        if cam_res is None:
            cam_res = [224, 224]
        self.camera = PiCamera()
        self.camera.resolution = tuple(cam_res)

        # model path
        self.model_path = f"models/{model_name}"

        # load model
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        _,  self.height, self.width, _ = self.input_details[0]['shape']
        self.output_shape = self.output_details[0]['shape'][1]

    def predict(self, output_dict):

        image = np.empty((self.height, self.width, 3), dtype=np.uint8)
        self.camera.capture(image, 'rgb')
        image = np.expand_dims(image, axis=0)

        # avoiding numpy (shape problems?)
        # stream = BytesIO()
        # self.camera.capture(stream, 'jpeg')
        # image = Image.open(stream).convert('RGB').resize((self.width, self.height), Image.ANTIALIAS)

        # image should be numpy ndarray with shape (1, height, width, 3)
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        if self.output_shape == 1:
            steering = output_data[0][0]
            speed = 0.5
        else:  # self.output_shape == 2:
            steering = output_data[0][0]
            speed = output_data[0][1]

        output_dict["ABS_RX"] = steering
        output_dict["ABS_Y"] = speed
        return output_dict

