import curses
import time
import easygopigo3
import numpy
import math
import datetime
import copy
import picamera
import picamera.array
import cv2
import vision_system as vs

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)
        
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
        
    # change the value of gopigo_to_target into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle

    def move(self,stat,frame):
        if stat.gpg_mode == "drive":
            self.pi.drive_degrees(stat.gpg_drive_degree,blocking=False)
        elif stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "capture":
            self.pi.stop()
            filename = "vs06"+ str(stat.photo_num) + ".jpg"
            cv2.imwrite(filename,frame)
            stat.photo_num = stat.photo_num + 1
        elif stat.gpg_mode == "stop":
            self.pi.stop()
            
    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame

class cv_control:
    def __init__(self):
        # key is an base h value of the color(e.x. 10 means skin color)
        # value indicates lower(0,1,2) and upper(3,4,5) hsv values
        self.color_dict = {10:numpy.array([0,100,100,20,255,255],dtype = "uint8")} 
    
    def extract_contours(self,frame,base_color):
        image = numpy.copy(frame)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #hueMat = cv2.inRange(hsv, self.lower, self.upper)
        hueMat = cv2.inRange(hsv, self.color_dict[base_color][0:3], self.color_dict[base_color][3:])
        kernel = numpy.ones((4,4),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        # Bitwise-AND mask for original image and hueMat
        res = cv2.bitwise_and(image,image, mask= hueMat)

        #find contours
        contours, _ = cv2.findContours(hueMat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)#draw all contours in green
        cv2.imshow("get contours",image)
        cv2.waitKey(1)
        return contours

class status:
    def __init__(self):
        self.vs_mode = "run" #run/quit
        self.gpg_mode = "stop" #stop/turn/drive/timeout
        self.gpg_turn_degree = 0
        self.gpg_drive_degree = 0
        self.photo_num = 0

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vs.vision_system("150.89.234.226",7777)
    stat = status()
    gpgc = gopigo_control()
    cvc = cv_control()
    vs.client_start(stat) #multi-thread(non-blocking) mode
    
    while True:
        
        # each marker has 4 values (x,y, orientationx, orientationy)
        # If at least one marker does not have enough values, "continue".
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length < len(vs.markers) * 4:
            continue
        
        shoot_pos = vs.aheadPos(vs.markers[13],200)
        gopigo_to_target_angle = vs.calcAngle(vs.markers[1],shoot_pos)
        gopigo_to_target_px = vs.calcDistance(vs.markers[1],shoot_pos)
        gopigo_face_target_angle = vs.calcOrientation(vs.markers[1],shoot_pos)

        draw_string_curses(stdscr,"gpg_mode:"+stat.gpg_mode,1)
        draw_string_curses(stdscr,"drive_degree:"+str(stat.gpg_drive_degree),2)
        draw_string_curses(stdscr,"turn_degree:"+str(gpgc.calc_gopigo_degree(stat.gpg_turn_degree)),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"to_px:"+str(gopigo_to_target_px),5)
        draw_string_curses(stdscr,"face_angle:"+str(gopigo_face_target_angle),6)
        
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame,10)

        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            # if marker info is not updated in 1 second, gopigo will stop.
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10 and gopigo_to_target_px > 50:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gopigo_to_target_angle
        elif gopigo_to_target_px > 50:
            # 4.7 is dependent on the webcamera location of the vision system
            stat.gpg_mode = "drive"
            stat.gpg_drive_degree = gopigo_to_target_px*4.7
        elif abs(gopigo_face_target_angle) > 10:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gopigo_face_target_angle
        elif stat.gpg_mode == "capture":
            stat.gpg_mode = "stop"
            stat.gpg_drive_degree = stat.gpg_turn_degree = 0
        elif stat.photo_num < 2:
            stat.gpg_mode = "capture"
        else:
            stat.gpg_mode = "stop"

        gpgc.move(stat,frame)
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            stat.vs_mode="quit"
            break

    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
