import socket
import select

host = "150.89.234.226" #Vision System IP
port = 7777
socket_timeout = 0.05
try:
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
    socket.connect((host,port)) # connect
    
    while True:
        read_sockets, write_sockets, error_sockets = select.select([socket], [], [], socket_timeout)
        if read_sockets:
            response = socket.recv(4096)
            print("response = " + response)
except KeyboardInterrupt:
    print("done")
    socket.close()
