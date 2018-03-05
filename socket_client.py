import socket

#host = "169.254.179.215" #Vision System IP
host = "150.89.234.226" #Vision System IP
port = 7777

try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
    client.connect((host,port)) # connect
    while True:
        response = client.recv(4096)
        print("response = " + response)
except KeyboardInterrupt:
    print("done")
