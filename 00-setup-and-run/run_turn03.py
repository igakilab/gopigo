import easygopigo3
import time

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
    
    def move(self):
        self.pi.forward() #non-blocking method
        time.sleep(2)
        self.pi.left()
        time.sleep(2)
        self.pi.stop()    

if __name__ == '__main__':
    gpg = gopigo_control()
    gpg.move()
