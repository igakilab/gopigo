import easygopigo3
import time

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
        self.pi.reset_encoders() #rest value of the encoders
        
        self.left_motor1 = 720
        self.right_motor1 = 720
        self.left_motor2 = -720
        self.right_motor2 = -720
    
    def move(self):
        pass

if __name__ == '__main__':
    gpg = gopigo_control()
    
    gpg.pi.forward()
    while True:
        print(str(gpg.pi.read_encoders()))
        if (gpg.pi.target_reached(gpg.left_motor1,gpg.right_motor1) == True):
            gpg.pi.reset_encoders()
            gpg.pi.backward()
        elif (gpg.pi.target_reached(gpg.left_motor2,gpg.right_motor2) == True):
            gpg.pi.stop()
            break;
