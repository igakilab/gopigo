import curses
import time
import datetime
import easygopigo3
import numpy
import vision_system as vs

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)
        
    # change the value of gopigo_to_target angle into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vs.vision_system("150.89.234.226",7777)
    gpgc = gopigo_control()
    
    while True:
        vs.read_vs_socket()
        
        # each marker has 4 values (x,y, orientationx, orientationy)
        # If at least one marker does not have enough values, "continue".
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length < len(vs.markers) * 4:
            continue
        
        shoot_pos = vs.aheadPos(vs.markers[13],200)
        gopigo_to_target_angle = vs.calcAngle(vs.markers[1],shoot_pos)

        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        
        # if marker info is not updated in 1 second, gopigo will stop.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            pass
        elif abs(gopigo_to_target_angle) > 10:
            gpgc.pi.turn_degrees(gpgc.calc_gopigo_degree(gopigo_to_target_angle),blocking=False)
        else:
            gpgc.pi.stop()

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
