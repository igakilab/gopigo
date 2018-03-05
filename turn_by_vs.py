import socket
import sys

#host = "169.254.179.215" #Vision System IP
host = "150.89.234.226" #Vision System IP
port = 7777
bufsize = 4096

class Marker:
    def __init__(self):
        self.shooter = 1
        self.target1 = 13
        self.sht_list = []
        self.tgt1_list = []
    
    def vs_to_marker(self,response):
        r_lines = response.split('\r\n')
        for line in r_lines:
            if line =="": # delete blank line
                break;
            vs_marker = line.split(' ') #split vs data
            #print("res= "+str(vs_marker))
            if(int(vs_marker[0])==self.shooter):
                self.sht_list = vs_marker[1:]
            elif(int(vs_marker[0])==self.target1):
                self.tgt1_list = vs_marker[1:]
        
            #if(len(self.sht_list)!=0 and len(self.tgt1_list)!=0):
                #print("shooter: " + str(self.sht_list))
                #print("target1: " + str(self.tgt1_list))
    
    def get_shooter_target(self):
        return self.sht_list, self.tgt1_list

class GPG_Control:
    def __init__(self):
        pass
        
    def turn_to_target(self,shooter,target):
        print("shooter= "+str(shooter))
        print("target= "+str(target))

    
if __name__ == '__main__':
    markers = Marker()
    gpgc = GPG_Control()
    
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        client.connect((host,port)) # connect
        while True:
            markers.vs_to_marker(client.recv(bufsize))
            shooter,target = markers.get_shooter_target()
            gpgc.turn_to_target(shooter, target)
            
        
    except KeyboardInterrupt:
        print("done")
