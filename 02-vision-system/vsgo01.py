import socket
import curses
import time
import select
import datetime
import easygopigo3
import copy
import numpy
import math

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
        # 1,13 are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        self.markers = {1:[],13:[]}
        
        self.updated = datetime.datetime.now()
        
    def read_vs_socket(self):
        read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
        if read_sockets:
            response = self.socket.recv(4096)
            self.vs_to_marker(response)

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
            if int(vs_marker[0]) in self.markers.keys():
                self.markers[int(vs_marker[0])] = vs_marker[1:]
                self.updated = datetime.datetime.now()

    # Angle (degree) for turning gopigo(obj1) toward obj2
    def calcAngle(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj2_pos - obj1_pos
        degree_to_obj2 = numpy.rad2deg(math.atan2(diff[1],diff[0]))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_to_obj2 = degree_to_obj2 - degree_of_obj1
        return obj1_to_obj2
    
    # this method returns a position info ahead by px value from the obj.
    def aheadPos(self,obj,px):
        shoot_pos = copy.deepcopy(obj)
        shoot_pos[0] = shoot_pos[0]+px*shoot_pos[2]
        shoot_pos[1] = shoot_pos[1]+px*shoot_pos[3]
        return shoot_pos

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)
        
    # change the value of gopigo_to_target angle into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle

    def move(self,stat):
        if stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "stop":
            self.pi.stop()
            
class status:
    def __init__(self):
        self.gpg_mode = "stop" #stop/turn/timeout
        self.gpg_turn_degree = 0

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system("150.89.234.226",7777)
    stat = status()
    gpgc = gopigo_control()
    
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

        draw_string_curses(stdscr,"gpg_mode:"+stat.gpg_mode,1)
        draw_string_curses(stdscr,"turn_degree:"+str(gpgc.calc_gopigo_degree(stat.gpg_turn_degree)),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            # if marker info is not updated in 1 second, gopigo will stop.
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gopigo_to_target_angle
        else:
            stat.gpg_mode = "stop"

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
    vs.socket.close()
