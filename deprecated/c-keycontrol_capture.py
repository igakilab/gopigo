import cv2
import picamera
import picamera.array
import io
import numpy
import easygopigo3
import time

WINNAME = "Keycontrol capture"
WIDTH = 640
HEIGHT = 480
camera = picamera.PiCamera(resolution=(WIDTH,HEIGHT),framerate=10)

# ref:http://picamera.readthedocs.io/en/release-1.12/recipes1.html#capturing-consistent-images
def init_camera():
    camera.iso = 100
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g

if __name__ == '__main__':
    egpi = easygopigo3.EasyGoPiGo3()
    egpi.set_speed(100) #0~1000 sitei
    cv2.namedWindow(WINNAME)
    init_camera()    
    
    while True:
        cap_stream = picamera.array.PiRGBArray(camera,size=(WIDTH,HEIGHT))
        camera.capture(cap_stream, format='bgr',use_video_port=True)
        image = cap_stream.array
        cv2.imshow(WINNAME, image)
        
        key = cv2.waitKey(10)%256
        if key == ord('q'):
            break
        elif key == ord('w'):
            egpi.forward()
        elif key == ord('s'):
            egpi.backward()
        elif key == ord('d'):
            egpi.right()
        elif key == ord('a'):
            egpi.left()
        elif key == ord('x'):
            egpi.stop()
        elif key == ord('p'):
            #use epoch(unix) milliseconds lower 9 digits
            filename = "capture" + str(int(time.time()*1000)-1519000000000) + ".jpg"
            cv2.imwrite(filename,image)
            print("captured")
