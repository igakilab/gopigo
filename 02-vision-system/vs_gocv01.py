import socket
import cv2

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.client.connect((self.host,self.port)) # connect
        
        self.shooter_id = 1
        self.target1_id = 13
        self.shooter = [] #position and orientation
        self.target1 = []

    def receive(self,status):
        if status.vs_mode == "print":
            response = self.client.recv(4096)
            #self.vs_to_marker(response)
            print(response)

class status:
    def __init__(self):
        self.vs_mode = "noprint" #noprint/print/quit
        
if __name__ == "__main__":
    vs = vision_system()
    status = status()
    cv2.namedWindow("vs_gocv01")
    response = vs.client.recv(4096)
    print(response)
    w = cv2.waitKey(10)%256
    while True:
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
    
