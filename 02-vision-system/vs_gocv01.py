import socket
import cv2
import select

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777
        self.sock_timeout = 0.05
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.client.connect((self.host,self.port)) # connect
        
        self.shooter_id = 1
        self.target1_id = 13
        self.shooter = [] #position and orientation
        self.target1 = []

class status:
    def __init__(self):
        self.vs_mode = "noprint" #noprint/print/quit
        
if __name__ == "__main__":
    vs = vision_system()
    status = status()
    cv2.namedWindow("vs_gocv01")
    
    try:
        while True:
            # Recv marker data
            read_sockets, write_sockets, error_sockets = select.select([vs.client], [], [], vs.sock_timeout)
            if read_sockets:
                response = vs.client.recv(4096)
                print(response)
    except KeyboardInterrupt:
        vs.client.close()
