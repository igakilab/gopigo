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
        
    def move(self,stat):
        if stat.gpg_mode == "drive":
            self.pi.drive_degrees(stat.gpg_drive_degree,blocking=False)
        elif stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "stop":
            self.pi.stop()

class status:
    def __init__(self):
        self.gpg_mode = "stop" #stop/turn/drive/timeout
        self.gpg_turn_degree = 0
        self.gpg_drive_degree = 0
        

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
    stat = status()
    
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
        dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)

        draw_string_curses(stdscr,"gpg.mode:"+str(stat.gpg_mode),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"distance_gopigo_target:"+str(dist_between_gopigo_and_target),5)
        
        # if marker info is not updated in 1 second, gopigo will stop.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10 and dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_to_target_angle)
            #gpgc.pi.turn_degrees(gpgc.calc_gopigo_degree(gopigo_to_target_angle),blocking=False)
        elif dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "drive"
            # 6.81 is calculated by covert_px_degree.py
            stat.gpg_drive_degree = dist_between_gopigo_and_target * 6.81
        else:
            stat.gpg_mode = "stop"
        gpgc.move(stat)

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
