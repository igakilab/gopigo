# Mini Exercise
## Objectives
- In this mini exercise, only SIIT students develop gopigo robot programs.
  - OIT students can not touch the keyboard.
  - OIT students should teach SIIT students based on this mini exercise materials and pre-study materials.
- Each team has 2 gopigo robots and use them.

## Preparation
- Connect between gopigo and note PC through a LAN cable.
  - Access with Internet explorer.
  - Access with UltraVNC.
- Connect between gopigo and note PC with WiFi.
  - Check IP address of each gopigo for wifi connection.
  - Access with Internet explorer or UltraVNC.
- **[Teaching Point!]** OIT students explain the differences between LAN and wifi, anb between Internet explorer and UltraVNC.

## Preparation in the raspbian
### Command line terminal
- Click command line terminal icon in raspbian
<a href="https://sites.google.com/site/ipbloit/2019/00/commandline.jpg"><img src="https://sites.google.com/site/ipbloit/2019/00/commandline.jpg" border="0" width="600"></a>
- You can copy and paste all commands in this education materials.
  - Right click copy and paste also can be available.
  - You cannot copy and paste between windows and raspbian through Internet explorer.
  - If you want to C&P any commands or source code, you should use UltraVNC.

### Text Editor and IDE
- You can use a geany editor in the raspbian.
- You can launch geany and open file by the following command in the raspbian.

```
$ geany [filename] &
```

- You can run python program on terminal or geany. You can run python program for just pushing ``F5`` on geany.
<a href="https://sites.google.com/site/ipbloit/2019/00/geany.jpg"><img src="https://sites.google.com/site/ipbloit/2019/00/geany.jpg" border="0" width="600"></a>

### Image Viewer
- You can view images with using gpicview.

```
$ gpicview [imagefilename]
```

<a href="https://sites.google.com/site/ipbloit/2019/00/gpicview.jpg"><img src="https://sites.google.com/site/ipbloit/2019/00/gpicview.jpg" border="0" width="600"></a>


# Gopigo control
- First, create pbl directory in the `$HOME`.

```
$ mkdir ipblmain
$ cd ipblmain
```

## Key control (gopigo_key01.py)
- Control Gopigo with Key Input using curses library.
  - ``w`` means forward, and ``x`` means stop.
  - ``d`` means right and ``a`` means left.
  - ``q`` means ``break`` the loop.
- [Curses](https://docs.python.org/3.6/howto/curses.html#curses-programming-with-python) library supplies keyboard-handling facility for text-based terminals.
- Type (or copy and paste) the following code and save it as ``gopigo_key01.py``.
- **[Teaching Point!]** OIT students explain the detail of the following source code, how to use the editor `geany`, and how to execute `*.py`.

```python
import easygopigo3
import curses

#Curses setup
stdscr = curses.initscr()
stdscr.nodelay(1) #non-blocking mode
curses.noecho()

egpi = easygopigo3.EasyGoPiGo3()

while True:
    w = stdscr.getch() #non blocking, getch() returns int value
    if w!=-1:#Print Inputted key value
        stdscr.move(1,0)
        stdscr.clrtoeol()
        stdscr.addstr(1,0,str(w))
    if w==ord('w'):
        egpi.forward()
    elif w==ord('d'):
        egpi.right()
    elif w==ord('a'):
        egpi.left()
    elif w==ord('x'):
        egpi.stop()
    elif w==ord('q'):
        egpi.stop()
        break
        
#Clean up curses.
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
```

- Execute `gopigo_key01.py`

## Speed Control
- Add `egpi.set_speed(50)` after `egpi = easygopigo3.EasyGoPiGo3()` in the ``gopigo_key01.py``.
- `set_speed()` sets the speed of the Gopigo as shown in the [Gopigo API Doc](https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html#easygopigo3.EasyGoPiGo3.set_speed).
- In our PBL, you should set a value of the speed between **0~500**.
  - Note:Though you can set any positive value as the speed value, too big value may damage the gopigo.

## Blocking method, Non-Blocking method
- In the [gopigo API docs](https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html), Blocking method will wait for the GoPiGo3 robot to finish moving.Non-Blocking method will exit immediately while the GoPiGo3 robot will continue moving.
- Copy `gopigo_key01.py` as `gopigo_key02.py`.
- Replace the `while` block into the following code snippets.
- **[Teaching Point!]** OIT students explain the detail of the following source code. Especially OIT students should teach differences between forward() and drive_degrees, and right() and turn_degrees in the view point of blocking and non-blocking methods.

```python
while True:
    w = stdscr.getch() #non blocking, getch() returns int value
    if w!=-1:#Print Inputted key value
        stdscr.move(1,0)
        stdscr.clrtoeol()
        stdscr.addstr(1,0,str(w))
    if w==ord('w'):
        egpi.drive_degrees(360,True) #Blocking method. Move 360 degree.
    elif w==ord('d'):
        egpi.turn_degrees(90,True)
    elif w==ord('a'):
        egpi.turn_degrees(-90,True)
    elif w==ord('x'):
        egpi.stop()
    elif w==ord('q'):
        egpi.stop()
        break
```
## LED control
- Copy `gopigo_key01.py` as `gopigo_key03.py`.
- Add the following function into the `gopigo_key03.py`.
- If you push the `b` key, led of the gopigo blinks in blue.
- If you push the `y` key, led of the gopigo blinks in yellow.
- If you push the `g` key, led of the gopigo blinks in green.
- You refer to the `led01~03.py` in the [pre-study materials](https://sites.google.com/site/ipbloit/2019/00).
- **[Teaching Point]** OIT students should teach how to control led of the gopigo.
- In this PBL, you can use these leds freely for decorating gopigo.

# Gopigo and OpenCV
## Use picamera
- Type (or copy and paste) the following code and save it as ``gopigo_key04.py``
- You can control gopigo and pycamera with keyboard.
- You can use this program for **mini game**.
  - In order to get higher score, you should customize this program with the following multiple opencv functions.

```python
import easygopigo3

import cv2
import picamera
import picamera.array
import time
############################################################
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

###########################################################

gpgc = gopigo_control()
egpi = easygopigo3.EasyGoPiGo3()
egpi.set_speed(500)

n = 0

while True:
    frame = gpgc.capture_frame()
    cv2.imshow("Camera",frame)

    w = cv2.waitKey(1) % 256

    if w==ord('w'):
        egpi.forward()
    elif w==ord('d'):
        egpi.right()
    elif w==ord('a'):
        egpi.left()
    elif w==ord('s'):
        egpi.backward()
    elif w==ord('p'): # Turn off the program
        egpi.stop()
        break
    elif w == ord('1'): # Save sequential images at current directory
        cv2.imwrite('files{0}.jpg'.format(n),frame)
        n = n + 1
```

## Detect Skin Color with OpenCV(color_detect01.py)
- Type (or copy and paste) the following code and save it as ``color_detect01.py``.
- This program detects your skin color, and draw rectangle surrounding detected objects.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 
  - How to use python class.
  - How to use picamera (especially about initial setting).
  - How to detect skin color and contours.

```python
import cv2
import picamera
import picamera.array
import time
import numpy
#from fractions import Fraction

class cv_control:
    def __init__(self):
        self.lower = []
        self.upper = []
    
    # set lower and upper filter. 
    def set_filter(self,base_hvalue):
        self.lower = numpy.array([base_hvalue-5, 80, 50], dtype = "uint8")
        self.upper = numpy.array([base_hvalue+5, 255, 250], dtype = "uint8")
            
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


class gopigo_control:
    # Init various camera parameter.
    # Finally, every parameter should be fixed to reasonable values.
    def __init__(self):
        self.width = 640
        self.height = 480
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 200
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
    cvc = cv_control()
    cvc.set_filter(10) # 10 is base_hvalue that means skin color.

    while True:
        frame = gpgc.capture_frame()
        cvc.detect_color(frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

## Detect Colored Objects with color_picker.py
- Modify `color_detect01.py` to detect red/blue/yellow/green targets.
  - Identify base H value (for HSV upper/lower filter) with using `color_picker.py` in [pre-study material about opencv](https://sites.google.com/site/ipbloit/2019/01).
  - **[Teaching Point]** How to use `color_picker.py`.

## Detect the area and center position for each contour (color_detect02.py)
- Modify `color_detect01.py` to detect the area and the center position for each colored object (a blue or yellow or green target).

<a href="https://sites.google.com/site/ipbloit/2019/01/opencv05.jpg"><img src="https://sites.google.com/site/ipbloit/2019/01/opencv05.jpg" border="0" width="800"></a>
- Copy ``color_detect01.py`` as ``color_detect02.py``.
- Delete ``detect_color`` method from ``cv_control`` class.
- Add ``extract_contours`` method and ``detect_contour_position`` method into the ``cv_control`` class.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 

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
  - Identify the base H value, beforehand.

```python
if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()
    cvc.set_filter(???)

    while True:
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame)
        cvc.detect_contour_position(contours,frame)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```


## Turn toward the blue target with opencv(toward_target01.py).
- Gopigo turns toward the largest blue object (cx always exists between 200px ~ 440px), continuouslly.
- If there is no blue object in the captured frame, gopigo stops.
- Type (or copy and paste) the following code and save it as ``toward_target01.py``.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 


```python
import cv2
import picamera
import picamera.array
import time
import numpy
import easygopigo3

class cv_control:
    def __init__(self):
        self.lower = []
        self.upper = []
    
    # set lower and upper filter. 
    def set_filter(self,base_hvalue):
        self.lower = numpy.array([base_hvalue-5, 80, 50], dtype = "uint8")
        self.upper = numpy.array([base_hvalue+5, 255, 250], dtype = "uint8")
    
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
        cv2.imshow("go_cv02 contours",image)
        return contours
    
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
            if cx < 200:
                status.drive_mode = "left"
            elif cx > 440:
                status.drive_mode = "right"
            else:
                status.drive_mode = "stop"
        else:
            status.drive_mode = "stop"
        cv2.imshow("go_cv02 rect-contour",frame)

class gopigo_control:
    # Init various camera parameter.
    # Finally, every parameter should be fixed to reasonable values.
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
        self.width = 640
        self.height = 480
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 200
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
        
    def move(self,status):
        print("move:" + status.drive_mode)
        if status.drive_mode == "stop":
            self.pi.stop()
        elif status.drive_mode == "right":
            self.pi.right()
        elif status.drive_mode == "left":
            self.pi.left()

class gopigo_status:
    def __init__(self):
        self.drive_mode = "stop" # stop/left/right

if __name__ == '__main__':
    gpgc = gopigo_control()
    cvc = cv_control()
    cvc.set_filter(110)
    status = gopigo_status()

    while True:
        frame = gpgc.capture_frame()
        contours = cvc.extract_contours(frame)
        cvc.detect_largest_contour_position(contours,frame,status)
        gpgc.move(status)

        if cv2.waitKey(10)%256 == ord('q'):
            break
```

# Gopigo and Vision system
## preperation
- Connect between note PC and the USB web camera.
  - **[Teaching Point]** oit students should teach what is the vision system.
  - **[Teaching Point]** oit students should teach how to run vision system based on the [pre-study material about vision system](https://sites.google.com/site/ipbloit/2019/02).
- Check IP address of the vision system (note pc).
- Paste the vs-marker on gopigo.
  - vs-marker no.1 is for shooter.
  - vs-marker no.6 is for guard.

## Shows vs-marker pos and orientation info transmitted from vision system(vsinfo01.py)
- This program prints the parsed vs-marker information stored in the vs.markers dict.

<a href="https://sites.google.com/site/ipbloit/2019/02/vs01.jpg"><img src="https://sites.google.com/site/ipbloit/2019/02/vs01.jpg" border="0" width="800"></a>

- You can see the information of detected vs-marker on the command line terminal in the raspbian.
  - e.x. ``0 93.5 223.0 0.09053574604251853 -0.9958932064677039
  - the previous information means marker.getID() + " " + location.getX() + " " + location.getY() + " " + orientationX.getX() + " " + orientationY.getY()
  - As shown in the previous figure, information about vsmarker id, location and orientation for each marker is presented by the vision system.

- Type (or copy and paste) the following code and save it as ``vsinfo01.py``.
  - Add the checked IP address of the vision system.
  - `self.markers` in the `vision_system` class requires vs-marker id on `?`
- **[Teaching Point!]** OIT students explain the detail of the following source code. 
  - vs-marker's info should be declared in detail. 
  - How to set the vs-marker id into `self.markers` variable in the `__init__` method of vision_system class.
- After executing `vsinfo01.py`, write down the pos and orientation information for each marker.

```python
import socket
import curses
import time
import select

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
        # ?,? are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        self.markers = {?:[],?:[]}

    def read_vs_socket(self):
        read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
        if read_sockets:
            response = self.socket.recv(4096)
            self.vs_to_marker(response)

    # Convert vs info to marker list
    def vs_to_marker(self,response):
        r_lines = response.split('\r\n')
        for line in r_lines:
            if line =="": # delete last blank line
                break;
            vs_marker_str = line.split(' ') #split vsdata
            if(len(vs_marker_str)<5):
                break
            try:
                vs_marker = [float(vs_marker_str[0]),float(vs_marker_str[1]),float(vs_marker_str[2]),float(vs_marker_str[3]),float(vs_marker_str[4])]
            except ValueError:
                print("could not convert string to float in vs_marker convert")
                break
            if int(vs_marker[0]) in self.markers.keys():
                self.markers[int(vs_marker[0])] = vs_marker[1:]

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system("???.???.???.???",7777)
    
    while True:
        vs.read_vs_socket()
        draw_string_curses(stdscr,str(vs.markers),2)
        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            break
            
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    vs.socket.close()
```

## Calculate the angle for obj1(gopigo) to turn toward obj2(target) (angle01.py)

- This program calculates angle (degree) from obj1 to obj2 as shown in the following figure.

<a href="https://sites.google.com/site/ipbloit/2019/02/vs02.jpg"><img src="https://sites.google.com/site/ipbloit/2019/02/vs02.jpg" border="0" width="800"></a>

- Type (or copy and paste) the following code and save it as ``angle01.py``.
  - Assign the actual vs-marker pos and orientation information into the following code.
- **[Teaching Point!]** OIT students explain the detail of the following source code and the previous figure.

```python
import numpy 
import math

x1 = ??? #gopigo.x
y1 = ??? #gopigo.y
orientationx1 = ??? #gopigo_orientation.x
orientationy1 = ??? #gopigo_orientation.y
x2 = ??? #target.x
y2 = ??? #target.y

diffx = x2 - x1
diffy = y2 - y1

degree_to_obj2 = numpy.rad2deg(math.atan2(diffy,diffx))
degree_of_obj1 = numpy.rad2deg(math.atan2(orientationy1,orientationx1))
obj1_to_obj2 = degree_to_obj2 - degree_of_obj1
print("degree_to_obj2:" + str(degree_to_obj2))
print("degree_of_obj1:" + str(degree_of_obj1))
print("obj1_to_obj2:" + str(obj1_to_obj2))
```

## Calculate distance from obj1 to obj2(distance.py)
- This program calculates distance between obj1 and obj2.

<a href="https://sites.google.com/site/ipbloit/2019/02/vs03.jpg"><img src="https://sites.google.com/site/ipbloit/2019/02/vs03.jpg" border="0" width="800"></a>

- Type (or copy and paste) the following code and save it as ``distance.py``.
  - Assign the actual vs-marker pos and orientation information into the following code.
- **[Teaching Point!]** OIT students explain the detail of the following source code and the previous figure.

```python
import numpy 
import math

x1 = ??? #gopigo.x
y1 = ??? #gopigo.y
x2 = ??? #target.x
y2 = ??? #target.y
orientationx2 = ??? #target_orientation.x
orientationy2 = ??? #target_orientation.y
x2 = x2 + 100 * orientationx2 #  a position info ahead by 100 px value from the target.
y2 = y2 + 100 * orientationy2

diffx = x2 - x1
diffy = y2 - y1

distance_between_obj1_and_obj2 = numpy.sqrt(diffx**2 + diffy**2)
print("distance_between_obj1_and_obj2:" + str(distance_between_obj1_and_obj2))
```

## Convert px value into gopigo’s drive degree(px_to_degree.py)

- gopigo's drive_degree() requires degree of the motor.
  - https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html#easygopigo3.EasyGoPiGo3.drive_degrees
- Vision system offers only px value for each marker from 640 * 480 images captured by web camera.
- In order to combine vision system and gopigo, you must convert px value into gopigo's drive degree value.
- Type (or copy and paste) the following code and save it as ``px_to_degree.py``.
- **[Teaching Point!]** OIT students explain the detail of the following source code. Especially meaning of the program output should be declared in detail.

```python
import socket
import time
import select
import easygopigo3
import numpy
import copy
import vision_system as vs
import datetime

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)

if __name__ == "__main__":

    vs = vs.vision_system("???.???.???.???",7777)
    gpgc = gopigo_control()

    gpgc.pi.reset_encoders()
    degree = 180
    
    #read marker information
    while True:
        vs.read_vs_socket()
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length >= len(vs.markers) * 4:
            break
    
    # gopigo_pos before drive_degrees
    pre_gpg = copy.deepcopy(vs.markers[1])
    print("forward(pre):"+str(degree)+"deg,"+str(pre_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))
    
    gpgc.pi.drive_degrees(degree,blocking=True) #Blocking method
    time.sleep(4)

   #read marker information
    while True:
        vs.read_vs_socket()
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 < 100:
            break
    
    # gopigo_pos after drive_degrees
    post_gpg = copy.deepcopy(vs.markers[1])
    print("forward(post):"+str(degree)+"deg,"+str(post_gpg)+":encoders:"+str(gpgc.pi.read_encoders()))

    # Calc diff between pre and post
    diff = numpy.array(pre_gpg) - numpy.array(post_gpg)
    distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
    
    # Calc distance(px value) per degree
    print("distance_px="+str(distance_px))
    print("px per degree is:"+str(degree/distance_px))
```

## Gopigo approaches to the target(vision_system.py and toward_target02.py)
- Gopigo approaches to a target with vision_system.py and toward_target02.py.
- First, type or copy and paste the following code, and save it as `vision_system.py`.
  - If you already have `vision_system.py` in your directory, overwrite it.
  - Select one target, and insert the vs-marker id of the target and your gopigo in `vision_system` class.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 

```python
import socket
import select
import datetime
import time
import copy
import numpy
import math

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
        # ??,?? are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        # You can add the marker info dict. 
        # e.x.{1:[],6:[],8:[]}
        self.markers = {??:[],??:[]}
        
        self.updated = datetime.datetime.now()
        
    def read_vs_socket(self):
        read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
        if read_sockets:
            response = self.socket.recv(4096)
            self.vs_to_marker(response)

    # Convert vs info to marker list
    def vs_to_marker(self,response):
        r_lines = response.split('\r\n')
        for line in r_lines:
            if line =="": # delete last blank line
                break;
            vs_marker_str = line.split(' ') #split vsdata
            if(len(vs_marker_str)<5):
                break
            try:
                vs_marker = [float(vs_marker_str[0]),float(vs_marker_str[1]),float(vs_marker_str[2]),float(vs_marker_str[3]),float(vs_marker_str[4])]
            except ValueError:
                print("could not convert string to float in vs_marker convert")
                break
            if int(vs_marker[0]) in self.markers.keys():
                self.markers[int(vs_marker[0])] = vs_marker[1:]
                self.updated = datetime.datetime.now()

    # Angle (degree) for turning gopigo(obj1) toward obj2
    def calcAngle(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj2_pos - obj1_pos
        degree_to_obj2 = numpy.rad2deg(math.atan2(diff[1],diff[0]))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_to_obj2 = degree_to_obj2 - degree_of_obj1
        return obj1_to_obj2
    
    # this method returns a position info ahead by px value from the obj.
    def aheadPos(self,obj,px):
        shoot_pos = copy.deepcopy(obj)
        shoot_pos[0] = shoot_pos[0]+px*shoot_pos[2]
        shoot_pos[1] = shoot_pos[1]+px*shoot_pos[3]
        return shoot_pos
        
    # Distance between obj1 and obj2
    def calcDistance(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj1_pos - obj2_pos
        distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
        return distance_px
```

- Type or copy and paste the following code, save it as `toward_target02.py`, and execute it.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 
  - How to use the output of `px_to_degree.py`.


```python
import curses
import time
import datetime
import easygopigo3
import numpy
import vision_system as vs

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)
        
    # change the value of gopigo_to_target angle into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle
        
    def move(self,stat):
        if stat.gpg_mode == "drive":
            self.pi.drive_degrees(stat.gpg_drive_degree,blocking=False)
        elif stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "stop":
            self.pi.stop()

class status:
    def __init__(self):
        self.gpg_mode = "stop" #stop/turn/drive/timeout
        self.gpg_turn_degree = 0
        self.gpg_drive_degree = 0
        

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vs.vision_system("???.???.???.???",7777)
    gpgc = gopigo_control()
    stat = status()
    
    while True:
        vs.read_vs_socket()
        
        # each marker has 4 values (x,y, orientationx, orientationy)
        # If at least one marker does not have enough values, "continue".
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length < len(vs.markers) * 4:
            continue
        
        shoot_pos = vs.aheadPos(vs.markers[??],200)
        gopigo_to_target_angle = vs.calcAngle(vs.markers[1],shoot_pos)
        dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)

        draw_string_curses(stdscr,"gpg.mode:"+str(stat.gpg_mode),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"distance_gopigo_target:"+str(dist_between_gopigo_and_target),5)
        
        # if marker info is not updated in 1 second, gopigo will stop.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10 and dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_to_target_angle)
        elif dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "drive"
            # ??? is calculated by px_to_degree.py
            stat.gpg_drive_degree = dist_between_gopigo_and_target * ???
        else:
            stat.gpg_mode = "stop"
        gpgc.move(stat)

        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            break

    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    vs.socket.close()
```

## Calculate the angle for obj1(gopigo) to face the front of the obj2(target) (angle02.py)
- This program calculates angle for obj1(gopigo) to face the front of the obj2(target) as shown in the following figure.

<a href="https://sites.google.com/site/ipbloit/2019/02/vs04.jpg"><img src="https://sites.google.com/site/ipbloit/2019/02/vs04.jpg" border="0" width="800"></a>

- Type (or copy and paste) the following code and save it as angle02.py.
  - Assign the actual vs-marker pos and orientation information into the following code.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 


```python
import numpy 
import math

obj1 = [???,???,???,???] #[gopigo.x,gopigo.y,gopigo_orientation.x,gopigo_orientation.y]
obj2 = [???,???,???,???] # [target.x,target.y,target_orientation.x,target_orientation.y]

opposite_orientation_of_obj2 = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
obj1_face_obj2 = opposite_orientation_of_obj2 - degree_of_obj1
print("opposite_orientation_of_obj2:" + str(opposite_orientation_of_obj2))
print("degree_of_obj1:" + str(degree_of_obj1))
print("obj1_face_obj2:" + str(obj1_face_obj2))
```

- Execute ``angle02.py``

## Gopigo approaches and faces the front of the target(toward_target03.py)
- Add the following code into the ``vision_system`` class in the ``vision_system.py``
- **[Teaching Point!]** OIT students explain the detail of the following source code. 


```python
    # Gopigo(obj1) and obj2 face each other if gopigo rotates based on the result of this method(degree).
    def calc_face_angle(self,obj1,obj2):
        opposite_orientation_of_obj2 = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_face_obj2 = opposite_orientation_of_obj2 - degree_of_obj1
        return obj1_face_obj2
```

- Copy ``toward_target02.py`` as ``toward_target03.py``
- Add ``gopigo_face_target_angle = vs.calc_face_angle(vs.markers[1],shoot_pos)`` after ``dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)``
- Add the following ``elif`` before ``else:``.

```python
        elif abs(gopigo_face_target_angle) > 10:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_face_target_angle)
```

- Execute ``toward_target03.py``.

## Gopigo approaches and detects contours of the target(toward_target04.py)
- Type (or copy and paste) the following code and save it as toward_target04.py.
- **[Teaching Point!]** OIT students explain the detail of the following source code. 


<a href="https://sites.google.com/site/ipbloit/2019/02/contours.jpg"><img src="https://sites.google.com/site/ipbloit/2019/02/contours.jpg" border="0" width="800"></a>

```python
import curses
import time
import datetime
import easygopigo3
import numpy
import vision_system as vs
import picamera
import picamera.array
import cv2

class cv_control:
    def __init__(self):
        # key is an base h value of the color(e.x. 10 means skin color)
        # value indicates lower(0,1,2) and upper(3,4,5) hsv values
        self.lower = []
        self.upper = []
    
    def set_filter(self,base_hvalue):
        self.lower = numpy.array([base_hvalue-5, 80, 50], dtype = "uint8")
        self.upper = numpy.array([base_hvalue+5, 255, 250], dtype = "uint8")
    
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
        cv2.imshow("get contours",image)
        return contours
    

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(100)
        self.width = 640
        self.height = 480
        self.camera = picamera.PiCamera(resolution=(self.width,self.height),framerate=10)
        self.camera.iso = 200
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g
        
    # change the value of gopigo_to_target angle into the range of +-180 degree.
    def calc_gopigo_degree(self,angle):
        if(angle > 180):
            angle = angle -360
        elif (angle < -180):
            angle = 360 + angle
        return angle
        
    def move(self,stat,frame):
        if stat.gpg_mode == "drive":
            self.pi.drive_degrees(stat.gpg_drive_degree,blocking=False)
        elif stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "capture":
            self.pi.stop()
            time.sleep(1)
            cv2.imwrite("capture.jpg",frame)
            stat.gpg_mode = "stop"
        elif stat.gpg_mode == "stop":
            self.pi.stop()

    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame

class status:
    def __init__(self):
        self.gpg_mode = "stop" #stop/turn/drive/timeout
        self.gpg_turn_degree = 0
        self.gpg_drive_degree = 0
        

def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vs.vision_system("???.???.???.???",7777)
    gpgc = gopigo_control()
    stat = status()
    cvc = cv_control()
    cvc.set_filter(170) # set lower and upper filter. base_hvalue "170" indicates "red".
    
    while True:
        vs.read_vs_socket()
        
        # each marker has 4 values (x,y, orientationx, orientationy)
        # If at least one marker does not have enough values, "continue".
        marker_length = 0
        for m in vs.markers.values():
           marker_length += len(m) 
        if marker_length < len(vs.markers) * 4:
            continue
        
        shoot_pos = vs.aheadPos(vs.markers[13],200)
        gopigo_to_target_angle = vs.calcAngle(vs.markers[1],shoot_pos)
        dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)
        gopigo_face_target_angle = vs.calc_face_angle(vs.markers[1],shoot_pos)
        
        draw_string_curses(stdscr,"gpg.mode:"+str(stat.gpg_mode),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"distance_gopigo_target:"+str(dist_between_gopigo_and_target),5)
        draw_string_curses(stdscr,"face_angle:"+str(gopigo_face_target_angle),6)
        
        frame = gpgc.capture_frame()
        cv2.imshow("Captured Image",frame)
        contours = cvc.extract_contours(frame)
        cv2.waitKey(1) #imshow requires waitKey()
        
        # if marker info is not updated in 1 second, gopigo will do nothing.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 500:
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10 and dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_to_target_angle)
            #gpgc.pi.turn_degrees(gpgc.calc_gopigo_degree(gopigo_to_target_angle),blocking=False)
        elif dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "drive"
            # ????? is calculated by px_to_degree.py
            stat.gpg_drive_degree = dist_between_gopigo_and_target * ?????
        elif abs(gopigo_face_target_angle) > 10:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_face_target_angle)
        elif stat.gpg_mode == "stop":
            pass
        else:
            stat.gpg_mode = "capture"
        gpgc.move(stat,frame)

        w = stdscr.getch() #non blocking, getch() returns int value
        if w==ord('q'):
            print("end")
            break

    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    vs.socket.close()
```

- You have got every knowledge and technique to develop gopigo robot program.
- Next, check [the minigame rule](https://sites.google.com/site/ipbloit/2019/04).
- Let's develop gopigo robots for mini game.
- Have fun!


