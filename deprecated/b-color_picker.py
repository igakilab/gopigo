import cv2
import picamera
import picamera.array
import io
import numpy
import easygopigo3
import time

WINNAME = "Keycontrol capture"
WIDTH = 800
HEIGHT = 600
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
    init_camera()    
    
    while True:
        cap_stream = picamera.array.PiRGBArray(camera,size=(WIDTH,HEIGHT))
        camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        cv2.imshow('camera capture', frame)
        
        key = cv2.waitKey(10)%256
        if key == ord('q'):
            break
