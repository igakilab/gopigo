import socket
import threading
import time
import select
import easygopigo3
import numpy
import copy
import vision_system as vs

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)

if __name__ == "__main__":

    vs = vs.vision_system()
    gpgc = gopigo_control()
    time.sleep(2)

    gpgc.pi.reset_encoders()
    degree = 180
    
    # gopigo_pos before drive_degrees
    pre_gpg = copy.deepcopy(vs.shooter)
    print("forward(pre):"+str(degree)+"deg,"+str(pre_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))
    
    gpgc.pi.drive_degrees(degree,blocking=True) #Blocking method
    #gpgc.pi.turn_degrees(degree,blocking=True)
    time.sleep(2)
    
    # gopigo_pos after drive_degrees
    post_gpg = copy.deepcopy(vs.shooter)
    print("forward(post):"+str(degree)+"deg,"+str(post_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))

    # Calc diff between pre and post
    diff = numpy.array(pre_gpg) - numpy.array(post_gpg)
    distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
    
    # Calc distance(px value) per degree
    print("distance_px="+str(distance_px))
    
    
