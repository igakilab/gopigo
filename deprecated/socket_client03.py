import socket
import threading
import curses
import time
import select

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

    def handler(self,gstat):
        while True:
            time.sleep(0.01)
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
            if read_sockets and gstat.vs_mode == "print":
                response = self.socket.recv(4096)
                self.vs_to_marker(response)
            elif gstat.vs_mode == "quit":
                self.socket.close()
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
                print("shooter: "+str(self.shooter))
            elif int(vs_marker[0])==self.target1_id:
                self.target1 = vs_marker[1:]
                print("target1: "+str(self.target1))

class gopigo_status:
    def __init__(self):
        self.vs_mode = "noprint" #noprint/print/quit
        
if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system()
    gstat = gopigo_status()
    vs.client_start(gstat) #multi-thread(non-blocking) mode
    
    while True:
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            gstat.vs_mode="quit"
            break
        elif w==ord('p'):
            print("Change print mode")
            gstat.vs_mode="print"
        elif w==ord('n'):
            print("Change noprint mode")
            gstat.vs_mode="noprint"
            
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
