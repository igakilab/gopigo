import cv2
import picamera
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
    # Set ISO to the desired value
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
    egpi.set_speed(50) #0~1000 sitei
    cv2.namedWindow(WINNAME)
    init_camera()    
    
    while True:
        imgStream = io.BytesIO() # Temporaly storage area
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = numpy.fromstring(imgStream.getvalue(), dtype=numpy.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        
        cv2.imshow(WINNAME, frame)
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
            cv2.imwrite(filename,frame)
            print("captured")
