import time
import getch
import picamera

camera = picamera.PiCamera()
#camera.start_preview()
w = getch.getch()
while w!='e':
    camera.resolution = (1024,768)
    camera.capture('cap.jpg')
    print("captured")
    w=getch.getch()
