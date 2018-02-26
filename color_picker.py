import numpy
import cv2
import picamera
import io

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
                
camera = picamera.PiCamera()
cv2.namedWindow('camera capture')
cv2.setMouseCallback( 'camera capture', mouse_event )

while True:
    camera.resolution = (800,600)
    imgStream = io.BytesIO() # Temporaly storage area
    camera.capture(imgStream, format='jpeg') #capture as jpeg format image
    data = numpy.fromstring(imgStream.getvalue(), dtype=numpy.uint8) # translate numpy
    frame = cv2.imdecode(data, 1) #data to image
    cv2.imshow('camera capture', frame)
	
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
	
cv2.destroyAllWindows()
