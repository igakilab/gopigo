import cv2
import picamera
import picamera.array
import time
import numpy

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
        print("shutter:"+str(self.camera.shutter_speed)+" awb_gains:"+str(g))
        
    # capture a frame from picamera
    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame

def mouse_event(event, x, y, flg, prm):
    if event==cv2.EVENT_LBUTTONDOWN:
        img = numpy.ones((128, 128, 3), numpy.uint8)
        avbgr = numpy.array([(numpy.uint8)(numpy.average(frame[y-2:y+2, x-2:x+2,0])),
            (numpy.uint8)(numpy.average(frame[y-2:y+2, x-2:x+2,1])),
            (numpy.uint8)(numpy.average(frame[y-2:y+2, x-2:x+2,2]))])
        img[:,:,0] = img[:,:,0] * avbgr[0]
        img[:,:,1] = img[:,:,1] * avbgr[1]
        img[:,:,2] = img[:,:,2] * avbgr[2]
        
        cv2.imshow('average color', img)
        print('bgr: '+str(img[1,1,:]))
        avhsv = cv2.cvtColor(numpy.array([[avbgr]], numpy.uint8), cv2.COLOR_BGR2HSV)
        print('hsv: '+str(avhsv[0,0,:]))
        
if __name__ == '__main__':
    cv2.namedWindow('camera capture')
    cv2.setMouseCallback( 'camera capture', mouse_event )
    gpgc = gopigo_control()

    while True:
        frame = gpgc.capture_frame()
        cv2.imshow('camera capture', frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
