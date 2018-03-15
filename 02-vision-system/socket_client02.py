import socket
import threading
import curses

class vision_system:
    def __init__(self):
        self.host = "150.89.234.226" #Vision System IP
        self.port = 7777

    def client_start(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        sock.connect((self.host,self.port)) # connect
        handle_thread = threading.Thread(target=self.handler, args=(sock,status,))
        handle_thread.start()

    def handler(self,sock,status):
        while True:
            if status.vs_mode == "print":
                response = sock.recv(4096)
                print("response = " + response)
            elif status.vs_mode == "quit":
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
    
    
