import cv2
import numpy
from numpy.random import randint
import picamera
import io

WINNAME = "OpenCV Sample 04"
WIDTH = 800
HEIGHT = 600

#pickup color hsv value:109 214 117
lower = numpy.array([100, 100, 100], dtype = "uint8")
upper = numpy.array([120, 255, 255], dtype = "uint8")

#blue color
#lower = numpy.array([110, 100, 100], dtype = "uint8")
#upper = numpy.array([130, 255, 255], dtype = "uint8")

#skin color
#lower = numpy.array([0, 48, 80], dtype = "uint8")
#upper = numpy.array([20, 255, 255], dtype = "uint8")

if __name__ == '__main__':
    camera = picamera.PiCamera()

    while True:
        camera.resolution = (WIDTH,HEIGHT)
        imgStream = io.BytesIO() # Temporaly storage area
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = numpy.fromstring(imgStream.getvalue(), dtype=numpy.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only skin colors
        hueMat = cv2.inRange(hsv, lower, upper)
        kernel = numpy.ones((5,5),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= hueMat)
        contours, hierarchy = cv2.findContours(hueMat, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        color = [randint(256) for _ in range(3)]
        cv2.drawContours(res, contours, -1, color, 3)#draw all contours

        for cont in contours:
            M = cv2.moments(cont)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("(cx,cy)=(" + str(cx) + "," + str(cy) + ")")
            x,y,w,h = cv2.boundingRect(cont)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5)
            #cv2.circle(frame, (cx,cy),w,(0,0,255),10)

        cv2.imshow('frame',frame)
        cv2.imshow('mask',hueMat)
        cv2.imshow('res',res)

        key = cv2.waitKey(10)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
qqqqqqq
