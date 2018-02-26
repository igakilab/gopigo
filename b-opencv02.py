import cv2
import picamera
import io
import numpy as np

WINNAME = "OpenCV Sample 01-a"
WIDTH = 640
HEIGHT = 480
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

if __name__ == '__main__':
    cv2.namedWindow(WINNAME)
    camera = picamera.PiCamera()

    while True:
        camera.resolution = (800,600)
        imgStream = io.BytesIO() # Temporaly storage area
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = np.fromstring(imgStream.getvalue(), dtype=np.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        
        image = np.copy(frame)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((3,3),np.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        image[hueMat == 255] = (0, 255, 0)
        cv2.imshow(WINNAME, image)

        key = cv2.waitKey(10)
        if key%256 == ord('q'):
            break
