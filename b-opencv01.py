import cv2
import picamera
import io
import numpy as np

WINNAME = "OpenCV Sample 01-a"
WIDTH = 640
HEIGHT = 480

if __name__ == '__main__':
    cv2.namedWindow(WINNAME)
    camera = picamera.PiCamera()

    while True:
        camera.resolution = (800,600)
        imgStream = io.BytesIO() # Temporaly storage area
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = np.fromstring(imgStream.getvalue(), dtype=np.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow(WINNAME, cv2.resize(frame, (640,480)))

        key = cv2.waitKey(10)
        if key%256 == ord('q'):
            break
