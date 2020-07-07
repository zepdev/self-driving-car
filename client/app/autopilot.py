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

        stream = BytesIO()
        self.camera.capture(stream, 'jpeg')
        image = Image.open(stream).convert('RGB').resize((self.width, self.height), Image.ANTIALIAS)
        image = np.array(image)
        image = image.astype(np.float32)
        image = np.expand_dims(image, axis=0)

        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()

        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        if self.output_shape == 2:
            speed = (output_data[0][1] + 1) * 0.5
            output_dict["ABS_Y"] = speed
        steering = output_data[0][0]
        output_dict["ABS_RX"] = steering

        return output_dict

