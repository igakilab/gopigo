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
        
    def client_start(self):
        self.socket.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(status,))
        handle_thread.start()

    def handler(self,status):
        while True:
            time.sleep(0.01)
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
            if read_sockets and status.vs_mode == "print":
                response = self.socket.recv(4096)
                print(response)
            elif status.vs_mode == "quit":
                self.socket.close()
                break

class status:
    def __init__(self):
        self.vs_mode = "noprint" #noprint/print/quit
        
if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system()
    status = status()
    vs.client_start() #multi-thread(non-blocking) mode
    
    while True:
        w = stdscr.getch() #non blocking, getch() returns int value
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
            
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
