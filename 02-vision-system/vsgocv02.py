import curses
import time
import datetime
import easygopigo3
import numpy
import vision_system as vs
import picamera
import picamera.array
import cv2

class cv_control:
    def __init__(self):
        # key is an base h value of the color(e.x. 10 means skin color)
        # value indicates lower(0,1,2) and upper(3,4,5) hsv values
        self.lower = []
        self.upper = []
    
    def set_filter(self,base_hvalue):
        self.lower = numpy.array([base_hvalue-10, 100, 100], dtype = "uint8")
        self.upper = numpy.array([base_hvalue+10, 255, 255], dtype = "uint8")
    
    def extract_contours(self,frame):
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
        cv2.imshow("get contours",image)
        return contours
    

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
        
    # change the value of gopigo_to_target angle into the range of +-180 degree.
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
            time.sleep(1)
            cv2.imwrite("capture.jpg",frame)
            stat.gpg_mode = "stop"
        elif stat.gpg_mode == "stop":
            self.pi.stop()

    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame

class status:
    def __init__(self):
        self.gpg_mode = "stop" #stop/turn/drive/timeout
        self.gpg_turn_degree = 0
        self.gpg_drive_degree = 0
        

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
    gpgc = gopigo_control()
    stat = status()
    cvc = cv_control()
    cvc.set_filter(10)
    
    while True:
        vs.read_vs_socket()
        
        # each marker has 4 values (x,y, orientationx, orientationy)
        # If at least one marker does not have enough values, "continue".
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length < len(vs.markers) * 4:
            continue
        
        shoot_pos = vs.aheadPos(vs.markers[13],200)
        gopigo_to_target_angle = vs.calcAngle(vs.markers[1],shoot_pos)
        dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)
        gopigo_face_target_angle = vs.calc_face_angle(vs.markers[1],shoot_pos)
        
        draw_string_curses(stdscr,"gpg.mode:"+str(stat.gpg_mode),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"distance_gopigo_target:"+str(dist_between_gopigo_and_target),5)
        draw_string_curses(stdscr,"face_angle:"+str(gopigo_face_target_angle),6)
        
        frame = gpgc.capture_frame()
        cv2.imshow("Captured Image",frame)
        contours = cvc.extract_contours(frame)
        cv2.waitKey(1) #imshow requires waitKey()
        
        # if marker info is not updated in 1 second, gopigo will do nothing.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 500:
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10 and dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_to_target_angle)
            #gpgc.pi.turn_degrees(gpgc.calc_gopigo_degree(gopigo_to_target_angle),blocking=False)
        elif dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "drive"
            # 6.81 is calculated by covert_px_degree.py
            stat.gpg_drive_degree = dist_between_gopigo_and_target * 6.81
        elif abs(gopigo_face_target_angle) > 10:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gopigo_face_target_angle
        elif stat.gpg_mode == "stop":
            pass
        else:
            stat.gpg_mode = "capture"
        gpgc.move(stat,frame)

        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            break

    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    vs.socket.close()
