import easygopigo3
import time
import curses

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
        self.pi.reset_encoders() #rest value of the encoders
        self.left_motor1 = 720
        self.right_motor1 = 720
        self.left_motor2 = -720
        self.right_motor2 = -720
        
    def check_encoders(self,status):
        print(str(self.pi.read_encoders()))
        if (self.pi.target_reached(self.left_motor1,self.right_motor1) == True):
            self.pi.reset_encoders()
            status.drive_mode = "b"
        elif (gpg.pi.target_reached(gpg.left_motor2,gpg.right_motor2) == True):
            status.drive_mode = "f"
            
    def move(self,status):
        if(status.drive_mode=="f" and not status.stop_input):
            self.pi.forward()
        elif(status.drive_mode=="b" and not status.stop_input):
            self.pi.backward()
        elif(status.drive_mode=="s" or status.stop_input):
            self.pi.stop()

class gopigo_status:
    def __init__(self):
        self.drive_mode = "f" # f/b/s-> forward,back,stop
        self.stop_input = False # is s key input or not
        
if __name__ == '__main__':
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()
    
    gpg = gopigo_control()
    status = gopigo_status()
    
    while True:
        w = stdscr.getch() #non blocking, getch() returns int value
        gpg.check_encoders(status)
        gpg.move(status)
        if w==ord("s"):
            if status.stop_input == True:
                status.stop_input = False
            else:
                status.stop_input = True
        elif w==ord("q"):
            break
        
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
            
