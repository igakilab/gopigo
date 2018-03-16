import socket
import threading
import curses
import time
import select
import easygopigo3
import numpy
import math

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        
        self.shooter_id = 1
        self.target1_id = 13
        self.shooter = [] #position and orientation
        self.target1 = []
        
    def client_start(self):
        self.socket.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(status,))
        handle_thread.start()

    def handler(self,status):
        while True:
            time.sleep(0.01)
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
            if read_sockets:
                response = self.socket.recv(4096)
                self.vs_to_marker(response)
            elif status.vs_mode == "quit":
                self.socket.close()
                break

    # Convert vs info to marker list
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
                #print("shooter: "+str(self.shooter))
            elif int(vs_marker[0])==self.target1_id:
                self.target1 = vs_marker[1:]
                #print("target1: "+str(self.target1))

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)

    # my_gopigo and target have position and orientation information from vision system.
    def turn_to_target(self,my_gopigo,target):
        #print("gopigo"+str(my_gopigo))
        if len(my_gopigo)<4 or len(target)<4:
            return
        g_pos = numpy.array(my_gopigo[0:2])
        t_pos = numpy.array(target[0:2])
        diff = t_pos - g_pos
        degree_to_target = numpy.rad2deg(math.atan2(diff[1],diff[0]))
        degree_my_gopigo = numpy.rad2deg(math.atan2(my_gopigo[3],my_gopigo[2]))
        gopigo_to_target = degree_to_target - degree_my_gopigo
        
        # change the value of gopigo_to_target into the range of +-180 degree.
        if(gopigo_to_target > 180):
            gopigo_to_target = gopigo_to_target -360
        elif (gopigo_to_target < -180):
            gopigo_to_target = 360 + gopigo_to_target
        print("gopigo_to_target" + str(gopigo_to_target))
        
        if abs(gopigo_to_target) > 10:
            self.pi.turn_degrees(gopigo_to_target,blocking=False)
        else:
            self.pi.stop()

class status:
    def __init__(self):
        self.vs_mode = "run" #run/quit
        
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
        gpgc.turn_to_target(vs.shooter,vs.target1)
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            status.vs_mode="quit"
            break

    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
