import time
import getch
import picamera

w = getch.getch()
while w!='e':
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        #camera.start_preview()
        camera.capture('cap.jpg')
        print("captured")
    w=getch.getch()
