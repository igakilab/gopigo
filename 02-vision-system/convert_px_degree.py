import socket
import time
import select
import easygopigo3
import numpy
import copy
import vision_system as vs
import datetime

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)

if __name__ == "__main__":

    vs = vs.vision_system("150.89.234.226",7777)
    gpgc = gopigo_control()

    gpgc.pi.reset_encoders()
    degree = 180
    
    #read marker information
    while True:
        vs.read_vs_socket()
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length >= len(vs.markers) * 4:
            break
    
    # gopigo_pos before drive_degrees
    pre_gpg = copy.deepcopy(vs.markers[1])
    print("forward(pre):"+str(degree)+"deg,"+str(pre_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))
    
    gpgc.pi.drive_degrees(degree,blocking=True) #Blocking method
    #gpgc.pi.turn_degrees(degree,blocking=True)
    time.sleep(4)

   #read marker information
    while True:
        vs.read_vs_socket()
        #print(str(vs.markers))
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 < 100:
            break
    
    # gopigo_pos after drive_degrees
    post_gpg = copy.deepcopy(vs.markers[1])
    print("forward(post):"+str(degree)+"deg,"+str(post_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))

    # Calc diff between pre and post
    diff = numpy.array(pre_gpg) - numpy.array(post_gpg)
    distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
    
    # Calc distance(px value) per degree
    print("distance_px="+str(distance_px))
    print("px per degree is:"+str(degree/distance_px))
    
    
