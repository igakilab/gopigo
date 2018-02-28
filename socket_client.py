import socket

host = "169.254.179.215" #Vision System IP
port = 7777

try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
    client.connect((host,port)) # connect
    while True:
        response = client.recv(1024)
        print("response = " + response)
except KeyboardInterrupt:
    print("done")
