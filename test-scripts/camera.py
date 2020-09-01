from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (224, 224)

camera.start_preview()
sleep(10)
camera.capture(f"/some/path/b{B_VALUE}/{ts}.jpg")
camera.stop_preview()
