import socket
import threading
import curses
import time
import select
import easygopigo3
import numpy
import math
import datetime
import copy

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777
        self.socket_timeout = 0.05
        self.updated = datetime.datetime.now()
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        
        self.shooter_id = 1
        self.shooter = [] #position and orientation
        self.target1_id = 13
        self.target1 = []
        
    def client_start(self,stat):
        self.socket.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(stat,))
        handle_thread.start()

    def handler(self,stat):
        while True:
            time.sleep(0.01)
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
            if read_sockets:
                response = self.socket.recv(4096)
                self.vs_to_marker(response)
            elif stat.vs_mode == "quit":
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
                self.updated = datetime.datetime.now()
            elif int(vs_marker[0])==self.target1_id:
                self.target1 = vs_marker[1:]
                self.updated = datetime.datetime.now()
                #print("target1: "+str(self.target1))

    # Distance between obj1 and obj2
    def calcDistance(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj1_pos - obj2_pos
        distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
        return distance_px
    
    # Angle (degree) for turning gopigo(obj1) toward obj2
    def calcAngle(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj2_pos - obj1_pos
        degree_to_obj2 = numpy.rad2deg(math.atan2(diff[1],diff[0]))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_to_obj2 = degree_to_obj2 - degree_of_obj1
        return obj1_to_obj2
    
    # Gopigo(obj1) and obj2 face each other if gopigo rotates the result of this method(degree).
    def calcOrientation(self,obj1,obj2):
        degree_of_obj1_target = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_face_obj2 = degree_of_obj1_target - degree_of_obj1
        return obj1_face_obj2
    
    # px indicates this method returns a position info which is px in front of the obj.
    def aheadPos(self,obj,px):
        shoot_pos = copy.deepcopy(obj)
        shoot_pos[0] = shoot_pos[0]+px*shoot_pos[2]
        shoot_pos[1] = shoot_pos[1]+px*shoot_pos[3]
        return shoot_pos

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)
        
    # change the value of gopigo_to_target into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle

    # my_gopigo and target have position and orientation information from vision system.
    # gopigo move to the target position
    def move(self,stat):
        if stat.gpg_mode == "drive":
            self.pi.drive_degrees(stat.gpg_drive_degree,blocking=False)
        elif stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "stop":
            self.pi.stop()

class status:
    def __init__(self):
        self.vs_mode = "run" #run/quit
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

    vs = vision_system()
    stat = status()
    gpgc = gopigo_control()
    vs.client_start(stat) #multi-thread(non-blocking) mode
    
    while True:
        if len(vs.target1) < 4 or len(vs.shooter) < 4:
            continue
        shoot_pos = vs.aheadPos(vs.target1,200)
        gopigo_to_target_angle = vs.calcAngle(vs.shooter,shoot_pos)
        gopigo_to_target_px = vs.calcDistance(vs.shooter,shoot_pos)
        gopigo_face_target_angle = vs.calcOrientation(vs.shooter,shoot_pos)
        
        draw_string_curses(stdscr,"gpg_mode:"+stat.gpg_mode,1)
        draw_string_curses(stdscr,"drive_degree:"+str(stat.gpg_drive_degree),2)
        draw_string_curses(stdscr,"turn_degree:"+str(gpgc.calc_gopigo_degree(stat.gpg_turn_degree)),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"to_px:"+str(gopigo_to_target_px),5)
        draw_string_curses(stdscr,"face_angle:"+str(gopigo_face_target_angle),6)

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
        else:
            stat.gpg_mode = "stop"
            stat.gpg_drive_degree = stat.gpg_turn_degree = 0

        gpgc.move(stat)
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
