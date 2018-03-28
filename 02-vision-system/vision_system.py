import socket
import select
import datetime
import time
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
        
    # Distance between obj1 and obj2
    def calcDistance(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj1_pos - obj2_pos
        distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
        return distance_px
