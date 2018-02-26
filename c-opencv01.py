import cv2
import picamera
import io
import numpy
from time import sleep

WINNAME = "OpenCV Sample 01"
WIDTH = 800
HEIGHT = 600
camera = picamera.PiCamera(resolution=(WIDTH,HEIGHT),framerate=10)

def init_camera():
    # Set ISO to the desired value
    camera.iso = 100
    # Wait for the automatic gain control to settle
    sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g

if __name__ == '__main__':
    init_camera()

    while True:
        imgStream = io.BytesIO() # Temporaly storage area
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = numpy.fromstring(imgStream.getvalue(), dtype=numpy.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        
        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow(WINNAME, cv2.resize(frame, (640,480)))

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
