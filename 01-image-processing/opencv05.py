import cv2
import picamera
import picamera.array
import time
import numpy
#from fractions import Fraction

class cv_control:
    def __init__(self):
        self.color_hbase = 10 # skin color
        self.lower = []
        self.upper = []
    
    # set lower and upper filter. 
    def update_filter(self,hbase):
        self.lower = numpy.array([self.color_hbase-10, 100, 100], dtype = "uint8")
        self.upper = numpy.array([self.color_hbase+10, 255, 255], dtype = "uint8")
    
    # returns contours array
    def extract_contours(self,frame):
        self.update_filter(self.color_hbase)
        image = numpy.copy(frame)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, self.lower, self.upper)
        kernel = numpy.ones((4,4),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        # Bitwise-AND mask for original image and hueMat
        res = cv2.bitwise_and(image,image, mask= hueMat)

        #find contours
        contours, _ = cv2.findContours(hueMat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)#draw all contours in green
        cv2.imshow("OpenCV Sample05 contours",image)
        return contours
    
    # show each contour center position, width, height, and area
    def detect_contour_position(self,contours,frame):
        for cont in contours:
            x,y,w,h = cv2.boundingRect(cont) # encloses contour in a rectangle.
            cx = x + w/2
            cy = y + h/2
            area = cv2.contourArea(cont) # calculate contour area
            print("(cx,cy,wide,height,area)=(" + str(cx) + "," + str(cy) + "," + str(w) + "," + str(h) + "," + str(area) + ")")
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
            cv2.imshow("OpenCV Sample05 rect-contours",frame)

class gopigo_control:
    # Init various camera parameter.
    # Finally, every parameter should be fixed to reasonable values.
    def __init__(self):
        self.width = 640
        self.height = 480
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 200
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g
        print("shutter:"+str(self.camera.shutter_speed)+" awb_gains:"+str(g))
        
    # capture a frame from picamera
    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame
        
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()

    while True:
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame)
        cvc.detect_contour_position(contours,frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
