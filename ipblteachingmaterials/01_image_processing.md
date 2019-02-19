# Image Processing
## References
- [HSV Color Space](http://en.wikipedia.org/wiki/HSL_and_HSV)
- [Digital Image in OpenCV](https://docs.opencv.org/2.4/doc/tutorials/core/mat_the_basic_image_container/mat_the_basic_image_container.html#matthebasicimagecontainer)
- [Color Sample](https://www.color-sample.com/popular/jiscolor/en/)
- [Changing Color-space in OpenCV](https://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html)
- [Contour features in OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html#contour-features)

## Preparation
- Access to the raspbian through UltraVNC.
- Move into the ``ipbl`` directory.

```
$ cd ~/ipbl
```

-----
## Simple image manipulation (opencv01.py)
- Type (or copy and paste) the following code and save it as ``opencv01.py``.

```
$ geany opencv01.py &
```

```python
import cv2
import numpy
import sys

WINNAME = "OpenCV Sample 01"
WIDTH = 640
HEIGHT = 480

if __name__ == '__main__':
    cv2.namedWindow(WINNAME)
    img = numpy.zeros((HEIGHT, WIDTH, 3))
    for r in range(256):
        for g in range(256):
            for b in range(256):
                img[...] = (b/255.0, g/255.0, r/255.0)
                print(img)

                cv2.imshow(WINNAME, img)
                if cv2.waitKey(10) %256 == ord('q'):
                    sys.exit(1)
```

- Execute ``opencv01.py``
  - You have 2 options to execute python program. Choose it.
- Type the following python command on the command line terminal.

```
$ python opencv01.py
```

- or just hit **``F5``** key on the geany editor after saving the source code.
- You can see the color of the window ``OpenCV Sample 00`` is gradually changing.
- If you press ``q`` key on the window ``OpenCV Sample 00``, this program will stop.
  - ``cv2.waitKey(10)`` means key input method (non-blocking) in opencv library.
  - ``stdscr.getch()`` in curses library for key input is used on the command line terminal.

-----
## Camera capture (opencv02.py)
<a href="https://sites.google.com/site/ipbloit/2019/01/opencv02.jpg"><img src="/site/ipbloit/2019/01/opencv02.jpg" border="0" width="500"></a>
- Reference: [PiCamera API](http://picamera.readthedocs.io/en/release-1.12/recipes1.html#capturing-consistent-images)
- Type (or copy and paste) the following code and save it as ``opencv02.py``.

```python
import cv2
import picamera
import picamera.array
import time
#from fractions import Fraction

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
        
if __name__ == '__main__':
    gpgc = gopigo_control()

    while True:
        frame = gpgc.capture_frame()
        cv2.imshow("OpenCV Sample02",frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

- Execute ``opencv02.py``
- You can see the movie on the window ``OpenCV Sample02`` through UltraVNC.

-----
## Detect skin color region (opencv03.py)
<a href="https://sites.google.com/site/ipbloit/2019/01/opencv03.jpg"><img src="/site/ipbloit/2019/01/opencv03.jpg" border="0" width="500"></a>
- Copy ``opencv02.py`` as ``opencv03.py``.
- Add ``import numpy``
- Add ``cv_control`` class.

```python
class cv_control:
    def __init__(self):
        self.lower = []
        self.upper = []
    
    # set lower and upper filter. 
    def set_filter(self,base_hvalue):
        self.lower = numpy.array([base_hvalue-5, 80, 50], dtype = "uint8")
        self.upper = numpy.array([base_hvalue+5, 255, 230], dtype = "uint8")
    
    # detect_color(self,frame) detects color regions between self.lower and self.upper.        
    def detect_color(self,frame):
        image = numpy.copy(frame)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, self.lower, self.upper)
        kernel = numpy.ones((4,4),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        image[hueMat == 255] = (0, 255, 0) # Convert white to green
        cv2.imshow("OpenCV Sample03",image)
```

- Replace code in the ``__main__`` as follows.

```python
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()
    cvc.set_filter(10) # 10 is base_hvalue that means skin color.

    while True:
        frame = gpgc.capture_frame()
        cvc.detect_color(frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

- Execute ``opencv03.py``
- You can see the video in which skin color is replaced by green.

-----
## Detect contours of skin color region (opencv04.py)
<a href="https://sites.google.com/site/ipbloit/2019/01/opencv04.jpg"><img src="/site/ipbloit/2019/01/opencv04.jpg" border="0" width="500"></a>
- Copy ``opencv03.py`` as ``opencv04.py``.
- Replace ``detect_color(self,frame)`` method in the ``cv_control`` class

```python
    # detect_color(self,frame) detects color regions between self.lower and self.upper.        
    def detect_color(self,frame):
        image = numpy.copy(frame)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, self.lower, self.upper)
        kernel = numpy.ones((4,4),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        # Bitwise-AND mask for original image and hueMat
        res = cv2.bitwise_and(image,image, mask= hueMat)

        image[hueMat == 255] = (0, 255, 0)
        cv2.imshow("OpenCV Sample04-1",image)    
        
        #find contours
        contours, _ = cv2.findContours(hueMat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(res, contours, -1, (0,255,0), 3)#draw all contours in green
        cv2.imshow("OpenCV Sample04-2",res)
```

- Execute ``opencv04.py``

-----
## Detect the area and center position for each contour (opencv05.py)
<a href="https://sites.google.com/site/ipbloit/2019/01/opencv05.jpg"><img src="/site/ipbloit/2019/01/opencv05.jpg" border="0" width="800"></a>
- Copy ``opencv04.py`` as ``opencv05.py``.
- Delete ``detect_color`` method from ``cv_control`` class.
- Add ``extract_contours`` method and ``detect_contour_position`` method into the ``cv_control`` class.

```python
    # returns contours array
    def extract_contours(self,frame):
        image = numpy.copy(frame)
        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hueMat = cv2.inRange(hsv, self.lower, self.upper)
        kernel = numpy.ones((4,4),numpy.uint8)

        hueMat = cv2.erode(hueMat,kernel,iterations = 3)
        hueMat = cv2.dilate(hueMat,kernel,iterations = 6)
        hueMat = cv2.erode(hueMat,kernel,iterations = 3)

        # Bitwise-AND mask for original image and hueMat
        res = cv2.bitwise_and(image,image, mask= hueMat)

        #find contours
        contours, _ = cv2.findContours(hueMat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)#draw all contours in green
        cv2.imshow("OpenCV Sample05 contours",image)
        return contours
    
    # show each contour center position, width, height, and area
    def detect_contour_position(self,contours,frame):
        for cont in contours:
            x,y,w,h = cv2.boundingRect(cont) # encloses contour in a rectangle.
            cx = x + w/2
            cy = y + h/2
            area = cv2.contourArea(cont) # calculate contour area
            print("(cx,cy,wide,height,area)=(" + str(cx) + "," + str(cy) + "," + str(w) + "," + str(h) + "," + str(area) + ")")
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
            cv2.imshow("OpenCV Sample05 rect-contours",frame)

```

- Replace ``__main__`` method as follows.

```python
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()
    cvc.set_filter(10)

    while True:
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame)
        cvc.detect_contour_position(contours,frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

- Execute ``opencv05.py``

-----
## [***Exercise***] Print the center position, width, height, and area of the largest contour (opencv06.py).
- ``extract_contours`` returns all contours in the image.
- In this exercise, the program print only the largest contour from the contours.

-----
## Color Picker (color_picker.py)
- This program can help you to pick BGR value and HSV value from captured video window.
- Type (or copy and paste) the following code and save it as ``color_picker.py``.

```python
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
```

- Execute ``color_picker.py``
- Click the captured video window. BGR and HSV value around the clicked point are shown in command line terminal.
- Now you should take [H-5, 80,50] and [H+5, 255, 230] as lower bound and upper bound respectively as stated in 'How to find HSV values to track?' of [this document](http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html).

-----
## [***Exercise***] Detect the center position, width, height, and the area of all blue objects (opencv07.py)
- Make a program that detects and prints the center (x, y) and the size (width, height) of multiple blue objects.

-----
## [***Exercise***] Detect the color, center position, width, height, and the area of multiple red and green objects  (opencv08.py)
- Make a program that detects and prints the color(red or green), center (x, y), the size (width, height) and the area of all red objects and green objects.

# Image Processing on GoPiGo
## Capture the blue object (go_cv01.py)
<a href="https://sites.google.com/site/ipbloit/2019/01/go_cv01.jpg"><img src="/site/ipbloit/2019/01/go_cv01.jpg" border="0" width="800"></a>
- Copy ``opencv05.py`` as ``go_cv01.py`` 
- Store the five images(``blue1.jpg``~``blue5.jpg``) which include the largest (>= 10000 px) blue object. 
- Add the following ``gopigo_status`` class.

```python
class gopigo_status:
    def __init__(self):
        self.save_blue = False
        self.photo_num = 1
```

- Add the following ``photo(self,frame,status)`` method in the ``gopigo_control`` class

```python
    def photo(self,frame,status):
        if status.save_blue == True and status.photo_num <= 5:
            filename = "blue" + str(status.photo_num) + ".jpg"
            cv2.imwrite(filename,frame)
            status.save_blue = False
            status.photo_num = status.photo_num + 1
```

- Delete ``detect_contour_position(self,contours,frame)`` from the ``cv_control`` class.
- Add the following ``calculate_contour_position(self,contour)`` method and ``detect_largest_contour_position`` method in the ``cv_control`` class.

```python
    def calculate_contour_position(self, contour):
        x,y,w,h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour) # calculate contour area
        cx = x + w/2
        cy = y + h/2
        return x,y,cx,cy,w,h,area
    
    # show largest contour center position, width, height, and area
    def detect_largest_contour_position(self,contours,frame,status):
        max_contour = []
        max_area = 0
        for cont in contours:
            area = cv2.contourArea(cont) # calculate contour area
            if area > max_area:
                max_area = area
                max_contour = cont
        if max_area >= 10000:
            x,y,cx,cy,w,h,area = self.calculate_contour_position(max_contour)
            print("max(cx,cy,wide,height,area)=(" + str(cx) + "," + str(cy) + "," + str(w) + "," + str(h) + "," + str(area) + ")")
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
            status.save_blue = True
        cv2.imshow("go_cv01 rect-contour",frame)
```

- Replace the ``__main__`` method as follows.

```python
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()
    cvc.set_filter(??) # Check base h value for detecting blue objects with using color-picker.py
    status = gopigo_status()

    while True:
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame)
        cvc.detect_largest_contour_position(contours,frame,status)
        gpgc.photo(frame,status)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

-----
## Turn toward the blue (go_cv02.py)
- Copy ``go_cv01.py`` as ``go_cv02.py``
- Replace the following ``gopigo_status`` class.

```python
class gopigo_status:
    def __init__(self):
        self.drive_mode = "stop" # stop/left/right
```
- Add ``import easygopigo3``, and add the following lines into the ``__init__`` of the ``gopigo_control`` class.

```python
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
```

- Delete ``photo()`` method and add the following ``move()`` method in the ``gopigo_control`` class.

```python
    def move(self,status):
        print("move:" + status.drive_mode)
        if status.drive_mode == "stop":
            self.pi.stop()
        elif status.drive_mode == "right":
            self.pi.right()
        elif status.drive_mode == "left":
            self.pi.left()
```

- Replace the following ``detect_largest_contour_position()`` method in the ``cv_control`` class.

```python
    # show largest contour center position, width, height, and area
    def detect_largest_contour_position(self,contours,frame,status):
        max_contour = []
        max_area = 0
        for cont in contours:
            area = cv2.contourArea(cont) # calculate contour area
            if area > max_area:
                max_area = area
                max_contour = cont
        if max_area >= 10000:
            x,y,cx,cy,w,h,area = self.calculate_contour_position(max_contour)
            print("max(cx,cy,wide,height,area)=(" + str(cx) + "," + str(cy) + "," + str(w) + "," + str(h) + "," + str(area) + ")")
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)
            if cx < 200:
                status.drive_mode = "left"
            elif cx > 440:
                status.drive_mode = "right"
            else:
                status.drive_mode = "stop"
        else:
            status.drive_mode = "stop"
        cv2.imshow("go_cv02 rect-contour",frame)
```

- Replace the ``__main__`` method as follows.

```python
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()
    cvc.set_filter(??) # Check base h value for detecting blue objects with using color-picker.py
    status = gopigo_status()

    while True:
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame)
        cvc.detect_largest_contour_position(contours,frame,status)
        gpgc.move(status)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

- Execute ``go_cv02.py``
- Gopigo turns toward the largest blue object (cx always exists between 200px ~ 440px), continuouslly.
- If there is no blue object in the captured frame, gopigo stops.

## [***Exercise***] Go to the green (go_cv03.py)
- Gopigo turns toward the largest **green** object(cx always exists between 200px ~ 440px), continuouslly.
- If the area of the green object is smaller than 30000 px, gopigo goes forward.
- If the area of the green object is larger than 50000 px, gopigo goes backward.
― If there is no green object in the captured frame, gopigo stops.

## [***Exercise***] Capture the red (go_cv04.py)
- Store the ten images (``red1.jpg``~``red10.jpg``)
- Gopigo turns toward the largest **red** object(cx always exists between 200px ~ 440px), continuouslly.
- If the area of the red object is smaller than 30000 px, gopigo goes forward.
- If the area of the red object is larger than 50000 px, gopigo goes backward.
- If the area of the red object is between 30000 px and 50000 px, and cx of the object exists between 200 and 440, store the image as ``red?.jpg``.
- After capturing ten images, 2 LEDs of the gopigo glows red for 5 seconds.
― If there is no blue object in the captured frame, gopigo stops.
