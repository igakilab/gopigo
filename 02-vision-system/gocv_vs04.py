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
        self.target1_id = 13
        self.shooter_is_moved = False
        self.target1_is_moved = False
        self.shooter = [] #position and orientation
        self.target1 = []
        
    def client_start(self,gstat):
        self.socket.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(gstat,))
        handle_thread.start()

    def handler(self,gstat):
        while True:
            time.sleep(0.01)
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
            if read_sockets:
                response = self.socket.recv(4096)
                self.vs_to_marker(response)
            elif gstat.vs_mode == "quit":
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

class gopigo_control:
    def __init__(self,screen):
        self.screen = stdscr
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
        
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
    
    # Angle for turning gopigo(obj1) toward an orientation of the obj2
    def calcOrientation(self,obj1,obj2):
        degree_of_obj1_target = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_face_obj2 = degree_of_obj1_target - degree_of_obj1
        return obj1_face_obj2
        
    # change the value of gopigo_to_target into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle

    # my_gopigo and target have position and orientation information from vision system.
    # gopigo move to the target position
    def move(self,my_gopigo,target,updated_time):
        #print("gopigo"+str(my_gopigo))
        if len(my_gopigo)<4 or len(target)<4:
            return
            
        gopigo_to_target_angle = self.calc_gopigo_degree(self.calcAngle(my_gopigo,target))
        gopigo_to_target_px = self.calcDistance(my_gopigo,target)
        gopigo_face_target_angle = self.calc_gopigo_degree(self.calcOrientation(my_gopigo,target))

        self.screen.move(1,0)
        self.screen.clrtoeol()
        self.screen.addstr(1,0,"gopigo_to_target_angle:"+str(gopigo_to_target_angle))
        self.screen.move(2,0)
        self.screen.clrtoeol()
        self.screen.addstr(2,0,"gopigo_to_target_px:"+str(gopigo_to_target_px))
        self.screen.move(3,0)
        self.screen.clrtoeol()
        self.screen.addstr(3,0,"gopigo_face_target_angle:"+str(gopigo_face_target_angle))
        
        # if marker info is not updated in 0.5 seconds, gopigo will stop.
        if abs(gopigo_to_target_angle) > 10 and gopigo_to_target_px > 50 and (datetime.datetime.now() - updated_time).total_seconds()*1000 < 500:
            self.pi.turn_degrees(gopigo_to_target_angle,blocking=False)
        elif gopigo_to_target_px > 50:
            # 4.5 is dependent on the webcamera location of the vision system
            self.pi.drive_degrees(gopigo_to_target_px*4.5,blocking=False)
        elif gopigo_face_target_angle > 10:
            self.pi.turn_degrees(gopigo_face_target_angle,blocking=False)
        else:
            self.pi.stop()

class gopigo_status:
    def __init__(self):
        self.vs_mode = "run" #run/quit
        
if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system()
    gstat = gopigo_status()
    gpgc = gopigo_control(stdscr) # To print strings on the stdscr
    vs.client_start(gstat) #multi-thread(non-blocking) mode
    
    while True:
        if len(vs.target1) < 4:
            continue
        shoot_pos = copy.deepcopy(vs.target1)
        #200 indicates shoot_pos is 200 px in front of the target1
        shoot_pos[0] = shoot_pos[0]+200*shoot_pos[2]
        shoot_pos[1] = shoot_pos[1]+200*shoot_pos[3]
        gpgc.move(vs.shooter,shoot_pos,vs.updated)
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            gstat.vs_mode="quit"
            break

    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
