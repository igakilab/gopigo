import easygopigo3
import time

if __name__ == '__main__':
    egpi = easygopigo3.EasyGoPiGo3()
    egpi.reset_encoders()
    
    lmotor = 360
    rmotor = -360
    
    #egpi.forward() #non blocking
    #egpi.turn_degrees(360) #non blocking right
    #egpi.turn_degrees(-360) #non blocking left
    egpi.drive_cm(50) # blocking
    while egpi.target_reached(lmotor,rmotor)==False:
        print(egpi.target_reached(lmotor,rmotor))
        print(egpi.read_encoders())
        time.sleep(0.01)
    egpi.stop()
    
    
