import socket
import curses
import select

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
    def read_vs_socket(self):
        read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
        if read_sockets:
            response = self.socket.recv(4096)
            print(response)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system("150.89.234.226",7777)
    
    while True:
        vs.read_vs_socket()
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            break
            
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    vs.socket.close()
