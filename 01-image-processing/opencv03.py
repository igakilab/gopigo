import cv2
import picamera
import picamera.array
import time
import numpy
#from fractions import Fraction

class cv_control:
    def __init__(self):
        self.color_hbase = 10
        self.lower = []
        self.upper = []
    
    # set lower and upper filter. 
    def update_filter(self,hbase):
        self.lower = numpy.array([self.color_hbase-10, 100, 100], dtype = "uint8")
        self.upper = numpy.array([self.color_hbase+10, 255, 255], dtype = "uint8")
    
    # Show image on the window named "winname"
    def show_image(self,winname,image):
        cv2.imshow(winname,image)

    # detect_color(self,frame) detects color regions between self.lower and self.upper.        
    def detect_color(self,frame):
        self.update_filter(self.color_hbase)
        image = numpy.copy(frame)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, self.lower, self.upper)
        kernel = numpy.ones((4,4),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        image[hueMat == 255] = (0, 255, 0)
        self.show_image("OpenCV Sample03",image)
        

class gopigo_control:
    # Init various camera parameter.
    # Finally, every parameter should be fixed to reasonable values.
    def __init__(self):
        self.width = 640
        self.height = 480
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 100
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        #self.camera.shutter_speed = 35000
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g
        #self.camera.awb_gains = (Fraction(375,256),Fraction(245,128))
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
        cvc.detect_color(frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
