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
        
    def check_encoders(self,status):
        print(str(self.pi.read_encoders()))
        if (self.pi.target_reached(self.left_motor1,self.right_motor1) == True):
            self.pi.reset_encoders()
            status.drive_mode = "b"
        elif (gpg.pi.target_reached(gpg.left_motor2,gpg.right_motor2) == True):
            status.drive_mode = "s"
            
    def move(self,status):
        if(status.drive_mode=="f"):
            self.pi.forward()
        elif(status.drive_mode=="b"):
            self.pi.backward()
        elif(status.drive_mode=="s"):
            self.pi.stop()

class gopigo_status:
    def __init__(self):
        self.drive_mode = "f" # f/b/s-> forward,back,stop
        
if __name__ == '__main__':
    gpg = gopigo_control()
    status = gopigo_status()
    
    while True:
        gpg.check_encoders(status)
        gpg.move(status)
            
