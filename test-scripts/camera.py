import cv2  # important: need cv2-version >= 3.3.1
import time
import base64
from PIL import Image
from io import BytesIO
dispW=224
dispH=224
flip=2
camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1'\
         + ' ! nvvidconv flip-method=' + str(flip) + ' ! video/x-raw, width=' + str(dispW) + ', height=' + str(dispH) +\
         ', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

for i in range(3):
    # read single picture
    ret, frame = cam.read()
    cv2.imwrite(f"test_{i}.jpg", frame)
    if not ret:
        print("Error")
    #img = Image.fromarray(frame).convert('RGB')
    #img.save(f'test{i}.jpg')
    #time.sleep(2)


# decode
img = Image.fromarray(frame).convert('RGB') 
stream = BytesIO()
img.save('test.jpg')
img.save(stream, format='jpeg')
pic_binary = base64.b64encode(stream.getvalue())
pic_str = pic_binary.decode("utf-8")

# encode
pic_binary_2 = pic_str.encode("utf-8")
img = base64.b64decode(pic_binary_2)


cam.release()
cv2.destroyAllWindows()
