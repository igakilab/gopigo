import socket

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((self.host,self.port)) # connect

if __name__ == "__main__":
    vs = vision_system()
    while True:
        response = vs.socket.recv(4096)
        print(response)
