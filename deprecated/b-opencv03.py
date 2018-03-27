import cv2
import picamera
import io
import numpy
from numpy.random import randint

WINNAME = "OpenCV Sample 03"
WIDTH = 640
HEIGHT = 480
lower = numpy.array([0, 48, 80], dtype = "uint8")
upper = numpy.array([20, 255, 255], dtype = "uint8")

if __name__ == '__main__':
    cv2.namedWindow(WINNAME)
    camera = picamera.PiCamera()

    while True:
        camera.resolution = (800,600)
        imgStream = io.BytesIO() # Temporaly storage area
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = numpy.fromstring(imgStream.getvalue(), dtype=numpy.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        
        image = numpy.copy(frame)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, lower, upper)
        kernel = numpy.ones((5,5),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        image[hueMat == 255] = (0, 255, 0)

        contours, hierarchy = cv2.findContours(hueMat, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        #draw all contours with random boarder colors
        color = [randint(256) for _ in range(3)]
        cv2.drawContours(image, contours, -1, color, 3)

        cv2.imshow(WINNAME, image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
