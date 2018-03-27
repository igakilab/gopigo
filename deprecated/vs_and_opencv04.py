import socket
import sys
import picamera
import picamera.array
import time
import cv2
import numpy
import easygopigo3
import math

#host = "169.254.179.215" #Vision System IP
host = "150.89.234.226" #Vision System IP
port = 7777
bufsize = 4096

class cv_control:
    def __init__(self):
        #self.width = 800
        #self.height = 600
        
        # H value (in HSV) for detected color
        self.red1_h_low = 170
        self.red1_h_up = 180
        self.red2_h_low = 0
        self.red2_h_up = 10

    def detect_color(self,frame,h_value_low,h_value_up):
        lower = numpy.array([h_value_low, 100, 0], dtype = "uint8")
        upper = numpy.array([h_value_up, 255, 255], dtype = "uint8")
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
        cv2.drawContours(res, contours, -1, (255,0,0), 3)#draw all contours in blue

        for cont in contours:
            M = cv2.moments(cont)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cont)
            print("(cx,cy,w,h)=(" + str(cx) + "," + str(cy) + "," + str(w) + "," + str(h) + ")")
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5) #draw in red

        cv2.imshow('frame',frame)
        #cv2.imshow('mask',hueMat)
        #cv2.imshow('res',res)

class vision_system:
    def __init__(self):
        
        #Init vs-Marker info
        self.shooter_id = 1 #vs-Marker ID
        self.target1_id = 13 #vs-Marker ID
        self.sht_list = []
        self.tgt1_list = []

    # Check whether detected marker is moved or not.
    def is_moved(self,vs_marker1,vs_marker2):
        if(len(vs_marker1)<4 or len(vs_marker2)<4):
            return True
        m1 = numpy.array(vs_marker1)
        m2 = numpy.array(vs_marker2)
        diff = m2 - m1
        distance = numpy.sqrt(diff[0]**2 + diff[1]**2)
        
        m1_ort_deg = numpy.rad2deg(math.atan2(m1[3],m1[2]))
        m2_ort_deg = numpy.rad2deg(math.atan2(m2[3],m2[2]))
        #print("m1:"+str(m1_ort_deg))
        #print("m2:"+str(m2_ort_deg))
        # Compare orientation between m1 and m2
        m1_to_m2 = abs(abs(m1_ort_deg)-abs(m2_ort_deg))
        #print("m1 to m2:"+str(m1_to_m2))
        if(distance >=20 or m1_to_m2 >= 5): # if marker is moved (over 20px or 5 degree), return True
            return True
        else:
            return False
            
    def vs_to_marker(self,status,response):
        r_lines = response.split('\r\n')
        for line in r_lines:
            if line =="": # delete last blank line
                break;
            vs_marker_str = line.split(' ') #split vsdata
            
            if(len(vs_marker_str)<5):
                break
            #print(str(vs_marker_str))
            try:
                vs_marker = [float(vs_marker_str[0]),float(vs_marker_str[1]),float(vs_marker_str[2]),float(vs_marker_str[3]),float(vs_marker_str[4])]
            except ValueError:
                print("could not convert string to float in vs_marker convert")
                break
            if(int(vs_marker[0])==self.shooter_id and self.is_moved(self.sht_list,vs_marker[1:])):
                self.sht_list = vs_marker[1:]
                status.gopigo_pos = vs_marker[1:3]
                status.gopigo_orientation = vs_marker[3:]
                print("shooter: "+str(status.gopigo_pos))
            elif(int(vs_marker[0])==self.target1_id and self.is_moved(self.tgt1_list,vs_marker[1:])):
                self.tgt1_list = vs_marker[1:]
                status.target_pos = vs_marker[1:3]
                status.target_orientation = vs_marker[3:]
                print("target1: "+str(self.tgt1_list))

class gopigo_status:
    def __init__(self):
        self.gopigo_pos = []
        self.gopigo_orientation = []
        self.target_pos = []
        self.target_orientation = []
        self.target_marker_id = 13
        self.reached = False
    
        
class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)

        #Init PiCamera
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

    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame
    
    def capture_image(self):
        #use epoch(unix) milliseconds lower 9 digits
        filename = "capture" + str(int(time.time()*1000)-1519000000000) + ".jpg"
        cv2.imwrite(filename,self.capture_frame())
        print("captured")

    def move(self,status):
        if(len(status.target_pos)<2 or len(status.gopigo_pos)<2):
            return
        elif status.reached:
            return
        diff = numpy.array(status.target_pos) - numpy.array(status.gopigo_pos)
        deg_to_target = numpy.rad2deg(math.atan2(diff[1],diff[0])) # degree to target from gopigo
        # current gopigo direction
        gopigo_deg = numpy.rad2deg(math.atan2(status.gopigo_orientation[1],status.gopigo_orientation[0]))
        # gopigo rotate degree
        rotate = deg_to_target - gopigo_deg
        
        if(rotate > 180):
            rotate = rotate - 360
        elif(rotate < -180):
            rotate = 360 + rotate
        print("rotate:"+str(rotate))
        
        if(abs(rotate)<=5):
            status.reached = True
            self.capture_image()
        else:
            self.pi.turn_degrees(rotate,False) #Non-block
        

if __name__ == '__main__':
    cvc = cv_control()
    vs = vision_system()
    gpgc = gopigo_control()
    status = gopigo_status()
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
    client.connect((host,port)) # connect
    while True:
        vs.vs_to_marker(status,client.recv(bufsize))
        frame = gpgc.capture_frame()
        cvc.detect_color(frame,cvc.red1_h_low,cvc.red1_h_up)
        cvc.detect_color(frame,cvc.red2_h_low,cvc.red2_h_up)
        gpgc.move(status)
        
        key = cv2.waitKey(10)%256
        if key == ord('q'):
            break
        
