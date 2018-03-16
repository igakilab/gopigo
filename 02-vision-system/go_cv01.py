import socket
import threading
import curses
import easygopigo3
import picamera
import picamera.array
import time
import cv2

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777
        self.shooter_id = 1
        self.target1_id = 13
        self.shooter = [] #position and orientation
        self.target1 = []

    def client_start(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        sock.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(sock,status,))
        handle_thread.start()

    def handler(self,sock,status):
        while True:
            if status.vs_mode == "print":
                response = sock.recv(4096)
                self.vs_to_marker(response)
            elif status.vs_mode == "quit":
                break
    
    def vs_to_marker(self,response):
        r_lines = response.split('\r\n')
        for line in r_lines:
            if line =="": # delete last blank line
                break;
            vs_marker_str = line.split(' ') #split vsdata
            if(len(vs_marker_str)<5):
                break
            try:
                vs_marker = [float(vs_marker_str[0]),float(vs_marker_str[1]),float(vs_marker_str[2]),float(vs_marker_str[3]),float(vs_marker_str[4])]
            except ValueError:
                print("could not convert string to float in vs_marker convert")
                break
            if int(vs_marker[0])==self.shooter_id:
                self.shooter = vs_marker[1:]
                print("shooter: "+str(self.shooter))
            elif int(vs_marker[0])==self.target1_id:
                self.target1 = vs_marker[1:]
                print("target1: "+str(self.target1))

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)

        #Init PiCamera
        self.width = 640
        self.height = 480
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
        print("capture_frame")
        return frame
        
class status:
    def __init__(self):
        self.vs_mode = "noprint" #noprint/print/quit
        
if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()
    
    vs = vision_system()
    status = status()
    gpgc = gopigo_control()
    vs.client_start() #multi-thread(non-blocking) mode

    while True:
        frame = gpgc.capture_frame()
        cv2.imshow("go_cv01",frame)
        cv2.waitKey(1)
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            status.vs_mode="quit"
            break
        elif w==ord('p'):
            print("Change print mode")
            status.vs_mode="print"
        elif w==ord('n'):
            print("Change noprint mode")
            status.vs_mode="noprint"
            
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
