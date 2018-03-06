import time
import picamera
import picamera.array
import cv2
import numpy
from numpy.random import randint

class Camera_Control:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 100
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g
        
    
    def capture_image(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        image = cap_stream.array
        #cv2.imshow(self.winname, image)
        #self.detect_red(image)
        return image
    
class CV_Control:
    def __init__(self):
        self.red_lower = numpy.array([170, 100, 50], dtype = "uint8")
        self.red_upper = numpy.array([190, 255, 255], dtype = "uint8")
    
    def detect_red(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only skin colors
        hueMat = cv2.inRange(hsv, self.red_lower, self.red_upper)
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


if __name__ == '__main__':
    camerac = Camera_Control()
    cvc = CV_Control()
    
    while True:
        cvc.detect_red(camerac.capture_image())
        
        key = cv2.waitKey(10)%256
        if key == ord('q'):
            break
