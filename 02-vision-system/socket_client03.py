import socket
import curses
import time
import select

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
        # 1,13 are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        self.markers = {1:[],13:[]}

    def read_vs_socket(self):
        read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
        if read_sockets:
            response = self.socket.recv(4096)
            self.vs_to_marker(response)

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
            if int(vs_marker[0]) in self.markers.keys():
                self.markers[int(vs_marker[0])] = vs_marker[1:]

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system("150.89.234.226",7777)
    
    while True:
        vs.read_vs_socket()
        draw_string_curses(stdscr,str(vs.markers),2)
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
