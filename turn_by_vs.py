import socket
import sys

#host = "169.254.179.215" #Vision System IP
host = "150.89.234.226" #Vision System IP
port = 7777
bufsize = 4096

def vs_to_marker(response):
    #print("response = " + response)
    r_lines = response.split('\r\n')
    for line in r_lines:
        if line =="": # delete blank line
            break;
        vs_marker = line.split(' ')
        print("res= "+str(vs_marker))
        vs_id = vs_marker[0]
        print("vs_id="+vs_id)

if __name__ == '__main__':
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        client.connect((host,port)) # connect
        while True:
            vs_to_marker(client.recv(bufsize))
            #print("response = " + response)
        
    except KeyboardInterrupt:
        print("done")
