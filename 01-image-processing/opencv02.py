import cv2
import picamera
import picamera.array
import time

class cv_control:
    def __init__(self):
        pass
    
    # Show image on the window named "winname"
    def show_image(self,winname,image):
        cv2.imshow(winname,image)

class gopigo_control:
    # Init various camera parameter.
    # Finally, every parameter should be fixed to reasonable values.
    def __init__(self):
        self.width = 640
        self.height = 480
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 100
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g
        
    # capture a frame from picamera
    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame
        
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()

    while True:
        frame = gpgc.capture_frame()
        cvc.show_image("OpenCV Sample02",frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
