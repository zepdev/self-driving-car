import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=2
camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)
ret, frame = cam.read()

cam.release()
cv2.destroyAllWindows()


# import cv2
import base64
from PIL import Image
from io import BytesIO
# from nanocamera import Camera
# import time
#
# camera = Camera(device_id=0, flip=0, width=224, height=224, fps=30)
# status = camera.isReady()
# print(status)
#
# while camera.isReady():
#     try:
#         # read the camera image
#         frame = camera.read()
#         # display the frame
#         cv2.imshow("Video Frame", frame)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break
#     except KeyboardInterrupt:
#         break
#
#
# np_image = camera.read()
# # decode
img = Image.fromarray(frame).convert('RGB') 
stream = BytesIO()
img.save('test.jpg')
img.save(stream, format='jpeg')
pic_binary = base64.b64encode(stream.getvalue())
pic_str = pic_binary.decode("utf-8")
#
# encode
pic_binary_2 = pic_str.encode("utf-8")
img = base64.b64decode(pic_binary_2)
# # close the camera instance
# camera.release()
#
# # remove camera object
# del camera

