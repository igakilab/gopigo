import socket
import threading
import time
import select
import easygopigo3
import numpy
import copy

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
        
    def client_start(self,gstat):
        self.socket.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(gstat,))
        handle_thread.start()

    def handler(self,status):
        while True:
            time.sleep(0.01)
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
            if read_sockets:
                #print("marker updated")
                response = self.socket.recv(4096)
                self.vs_to_marker(response)
                
            if status.vs_mode == False:
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
    

class gopigo_status:
    def __init__(self):
        self.vs_mode = True #T/F
        
if __name__ == "__main__":

    vs = vision_system()
    gpgc = gopigo_control()
    gstat = gopigo_status()
    vs.client_start(gstat) #multi-thread(non-blocking) mode
    time.sleep(2)
    gpgc.pi.reset_encoders()
    degree = 180
    
    # gopigo_pos before drive_degrees
    pre_gpg = copy.deepcopy(vs.shooter)
    print("forward(pre):"+str(degree)+"deg,"+str(pre_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))
    
    gpgc.pi.drive_degrees(degree,blocking=True) #Blocking method
    #gpgc.pi.turn_degrees(degree,blocking=True)
    time.sleep(1)
    
    # gopigo_pos after drive_degrees
    post_gpg = copy.deepcopy(vs.shooter)
    print("forward(post):"+str(degree)+"deg,"+str(post_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))

    # Calc diff between pre and post
    diff = numpy.array(pre_gpg) - numpy.array(post_gpg)
    distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
    
    # Calc distance(px value) per degree
    print("distance_px="+str(distance_px))
    gstat.vs_mode = False
    
    
