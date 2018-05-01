# Preparation
## Set up USB camera
- Connect USB camera to PC.
- Change the setting about auto focus of the USB camera as the following image.

<a href="https://sites.google.com/site/ipbloit/2018/02/logicool.jpg"><img src="/site/ipbloit/2018/02/logicool.jpg" border="0" width="800"></a>

## eclipse setting
- Launch eclipse
  - Execute ``C:\eclipse\eclipse.exe``
- Import Project
  - In [Import] Window, select [General->Projects from Folder or Archive] and click [Next] Button.
  - In [Import Projects from File System or Archive] window, select ``vision system.zip``, unckeck ``[vision system.zip_expanded]``, and click [Finish] as follows.

<a href="https://sites.google.com/site/ipbloit/2018/02/eclipse_import.jpg"><img src="/site/ipbloit/2018/02/eclipse_import.jpg" border="0" width="800"></a>

  - It's OK, if ``vision system`` is added in the package explorer.
- Configure vm parameters
  - Right click `src\DetectMarkerServer.java`->[Run As]->[Run Configurations].
  - In [Run Configurations] window, select [Arguments] Tab, and input `-Xss64m -Xms64m -Xmx64m` in the [VM arguments] as follows.

<a href="https://sites.google.com/site/ipbloit/2018/02/eclipse_run_configurations.jpg"><img src="/site/ipbloit/2018/02/eclipse_run_configurations.jpg" border="0" width="800"></a>

## Launch vision system
- In the [Run Configurations], click [Run] button, or Right click `src\DetectMarkerServer.java`->[Run As]->[Java Application].
- It's OK, if vs-marker is adequately detected.

## Trouble Shooting
### Camera does not work
- Confirm ``src\capture\DSJCapture.java`` L30.
- If your PC has only one USB camera, the following number should be ``0``.
- ``this(listener, 2);//Camera No.`` 

### vs-marker detection is unstable
- Confirm ``src\marker\MarkerDetector.java`` L20,L21
- The following parameters indicate detected vs-marker's px size (min to max).
- You should change the parameters according to the captured size of the vs-markers.

```java
	private static final int MIN_MARKER_SIZE = 15;
	private static final int MAX_MARKER_SIZE = 60;
```

# Try vision system
## Check IP of the vision system
- Connect PC (the vision system is running) to wifi.
- Launch command prompt on windows.
- Type ``ipconfig`` on command prompt (windows), and check **IPv4 address** of ``Wireless LAN adapter``.
  - [``xxx.xxx.xxx.xxx``]

## Use Socket (socket_client01.py)
- Type (or copy and paste) the following code and save it as ``socket_client01.py``.
  - Assign the checked IP address to the ``host`` variable.

```python
import socket
import select

host = "???.???.???.???" #Vision System IP
port = 7777
socket_timeout = 0.05
try:
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
    socket.connect((host,port)) # connect
    
    while True:
        read_sockets, write_sockets, error_sockets = select.select([socket], [], [], socket_timeout)
        if read_sockets:
            response = socket.recv(4096)
            print("response = " + response)
except KeyboardInterrupt:
    print("done")
    socket.close()
```

- Execute ``socket_client01.py``.
<a href="https://sites.google.com/site/ipbloit/2018/02/vs01.jpg"><img src="/site/ipbloit/2018/02/vs01.jpg" border="0" width="800"></a>
- You can see the information of detected vs-marker on the command line terminal in the raspbian.
  - e.x. ``response = 0 93.5 223.0 0.09053574604251853 -0.9958932064677039
  -the previous information means marker.getID() + " " + location.getX() + " " + location.getY() + " " + orientationX.getX() + " " + orientationY.getY()
  - As shown in the previous figure, information about vsmarker id, location and orientation for each marker is presented by the vision system.
- In order to stop the client, Push ``Ctr+C`` on the terminal.

## socket client using Curses and vision system class (socket_client02.py)
- Type (or copy and paste) the following code and save it as ``socket_client02.py``.

```python
import socket
import curses
import select

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
    def read_vs_socket(self):
        read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [], self.socket_timeout)
        if read_sockets:
            response = self.socket.recv(4096)
            print(response)

if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vision_system("???.???.???.???",7777)
    
    while True:
        vs.read_vs_socket()
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

-----
## Parse response messages transmitted from vision system(socket_client03.py)
- Copy ``socket_client02.py`` as ``socket_client03.py``.
- Add ``import time``
- Add the following definition about vs-markers in the ``__init__`` method.

```python
        # 1,13 are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        self.markers = {1:[],13:[]}
```

- Replace ``print(response)`` into ``self.vs_to_marker(response)`` in the ``read_vs_socket`` method.

- Add the following method in the ``vision_system`` class.

```python
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
```

- Add the following ``global`` method.

```python
def draw_string_curses(screen,msg,pos):
    screen.move(pos,0)
    screen.clrtoeol()
    screen.addstr(pos,0,msg)
```
- Add ``draw_string_curses(stdscr,str(vs.markers),2)`` after ``vs.read_vs_socket()``

- Execute ``socket_client03.py``
- You can see the parsed vs-marker information in the vs.markers dict.


# Vision system and gopigo
## Calculate the angle for obj1(gopigo) to turn toward obj2(target) (check_angle01.py)
- Type (or copy and paste) the following code and save it as ``check_angle01.py``.

```python
import numpy 
import math

x1 = 300 #shooter
y1 = 300
orientationx1 = 1
orientationy1 = -1
x2 = 200 #target
y2 = 200

diffx = x2 - x1
diffy = y2 - y1

degree_to_obj2 = numpy.rad2deg(math.atan2(diffy,diffx))
degree_of_obj1 = numpy.rad2deg(math.atan2(orientationy1,orientationx1))
obj1_to_obj2 = degree_to_obj2 - degree_of_obj1
print("degree_to_obj2:" + str(degree_to_obj2))
print("degree_of_obj1:" + str(degree_of_obj1))
print("obj1_to_obj2:" + str(obj1_to_obj2))
```

- Execute ``check_angle01.py``
- This program calculates angle (degree) from obj1 to obj2 as shown in the following figure.

<a href="https://sites.google.com/site/ipbloit/2018/02/vs02.jpg"><img src="/site/ipbloit/2018/02/vs02.jpg" border="0" width="800"></a>

## Gopigo turns to the target(vsgo01.py)
- Type (or copy and paste) the following code and save it as ``vsgo01.py``.

```python
import socket
import curses
import time
import select
import datetime
import easygopigo3
import copy
import numpy
import math

class vision_system:
    def __init__(self,host,port):
        self.socket_timeout = 0.05
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
        self.socket.connect((host,port)) # connect
        
        # 1,13 are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        self.markers = {1:[],13:[]}
        
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
    gpgc = gopigo_control()
    
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

        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        
        # if marker info is not updated in 1 second, gopigo do nothing.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            pass
        elif abs(gopigo_to_target_angle) > 10:
            gpgc.pi.turn_degrees(gpgc.calc_gopigo_degree(gopigo_to_target_angle),blocking=False)
        else:
            gpgc.pi.stop()

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

- Execute ``vsgo01.py``.
- Gopigo turns to the target (ahead by 200px of target vs-marker) continuously.

## Gopigo turns to the target with external vision_system class (vsgo02.py)
- Type (or copy and paste) the following code and save it as ``vision_system.py``.

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
        
        # 1,13 are vs-marker id
        # each marker has 4 values (x,y,orientationx,orientationy)
        self.markers = {1:[],13:[]}
        
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
```

- Copy ``vsgo01.py`` as ``vsgo02.py``.
- Delete ``vision_system`` class from the ``vsgo02.py``
- Add ``import vision_system as vs`` into the ``vsgo02.py``.
- Replace ``vs = vision_system("???.???.???.???",7777)`` in the ``__main__`` with ``vs = vs.vision_system("???.???.???.???",7777)``. 
- Execute ``vsgo02.py``.

-----
## Calculate distance from obj1 to obj2(calc_distance.py)
- Type (or copy and paste) the following code and save it as ``calc_distance.py``.

```python
import numpy 
import math

x1 = 300 #shooter
y1 = 300
x2 = 200 #target
y2 = 200

diffx = x2 - x1
diffy = y2 - y1

distance_between_obj1_and_obj2 = numpy.sqrt(diffx**2 + diffy**2)
print("distance_between_obj1_and_obj2:" + str(distance_between_obj1_and_obj2))
```

- Execute ``calc_distance.py``
- This program calculates distance between obj1 and obj2.

<a href="https://sites.google.com/site/ipbloit/2018/02/vs03.jpg"><img src="/site/ipbloit/2018/02/vs03.jpg" border="0" width="800"></a>

-----
## Convert px value into gopigo's drive degree(convert_px_degree.py)
- gopigo's drive_degree() requires degree of the motor.
  - http://gopigo3.readthedocs.io/en/latest/api-basic.html#easygopigo3.EasyGoPiGo3.drive_degrees
- Vision system offers only px value for each marker from 640 * 480 images captured by web camera.
- In order to combine vision system and gopigo, you must convert px value into gopigo's drive degree value.
- Type (or copy and paste) the following code and save it as ``convert_px_degree.py``.

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


## Gopigo approaches to the target(vsgo03.py)
- Use status class.
- Add the following code into the ``vision_system`` class in the ``vision_system.py``

```python
    # Distance between obj1 and obj2
    def calcDistance(self,obj1,obj2):
        obj1_pos = numpy.array(obj1[0:2])
        obj2_pos = numpy.array(obj2[0:2])
        diff = obj1_pos - obj2_pos
        distance_px = numpy.sqrt(diff[0]**2 + diff[1]**2)
        return distance_px
```

- Copy ``vsgo02.py`` as ``vsgo03.py``
- Add the following ``status`` class in the vsgo03.py.

```python
class status:
    def __init__(self):
        self.gpg_mode = "stop" #stop/turn/drive/timeout
        self.gpg_turn_degree = 0
        self.gpg_drive_degree = 0
```

- Add the following ``move()`` method in the ``gopigo_control`` class.

```python
    def move(self,stat):
        if stat.gpg_mode == "drive":
            self.pi.drive_degrees(stat.gpg_drive_degree,blocking=False)
        elif stat.gpg_mode == "turn":
            self.pi.turn_degrees(self.calc_gopigo_degree(stat.gpg_turn_degree),blocking=False)
        elif stat.gpg_mode == "stop":
            self.pi.stop()
```

- Replace the ``__main__`` as follows.

```python
if __name__ == "__main__":
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1) #non-blocking mode
    curses.noecho()

    vs = vs.vision_system("150.89.234.226",7777)
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
        
        shoot_pos = vs.aheadPos(vs.markers[13],200)
        gopigo_to_target_angle = vs.calcAngle(vs.markers[1],shoot_pos)
        dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)

        draw_string_curses(stdscr,"gpg.mode:"+str(stat.gpg_mode),3)
        draw_string_curses(stdscr,"to_angle:"+str(gopigo_to_target_angle),4)
        draw_string_curses(stdscr,"distance_gopigo_target:"+str(dist_between_gopigo_and_target),5)
        
        # if marker info is not updated in 1 second, gopigo will do nothing.
        if (datetime.datetime.now() - vs.updated).total_seconds()*1000 > 1000:
            stat.gpg_mode = "timeout"
        elif abs(gopigo_to_target_angle) > 10 and dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gpgc.calc_gopigo_degree(gopigo_to_target_angle)
        elif dist_between_gopigo_and_target > 30:
            stat.gpg_mode = "drive"
            # ?.?? is calculated by covert_px_degree.py
            stat.gpg_drive_degree = dist_between_gopigo_and_target * ?.??
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

- Execute ``vsgo03.py``
- Gopigo turns and approaches to the target (ahead by 200px)

-----
## ***Exercise*** (vsgo04.py)
- Use three vs-markers, gopigo, target, and start place.
- Improve ``vsgo03.py``.
- In this program, first, gopigo turns and approaches to the target. Next, gopigo returns to the start place, and glows the LEDs blue.

-----
## Calculate the angle for obj1(gopigo) to face the front of the obj2(target) (check_angle02.py)

- Type (or copy and paste) the following code and save it as check_angle02.py.

```python
import numpy 
import math

#x1 = 200 #shooter
#y1 = 200
#orientationx1 = -1
#orientationy1 = -1
obj1 = [200,200,-1,-1]
#x2 = 200 #target
#y2 = 200
#orientationx1 = 0
#orientationy1 = 1
obj2 = [200,200,0,1]

opposite_orientation_of_obj2 = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
obj1_face_obj2 = opposite_orientation_of_obj2 - degree_of_obj1
print("opposite_orientation_of_obj2:" + str(opposite_orientation_of_obj2))
print("degree_of_obj1:" + str(degree_of_obj1))
print("obj1_face_obj2:" + str(obj1_face_obj2))
```

- Execute ``check_angle02.py``
- This program calculates angle for obj1(gopigo) to face the front of the obj2(target) as shown in the following figure.

<a href="https://sites.google.com/site/ipbloit/2018/02/vs04.jpg"><img src="/site/ipbloit/2018/02/vs04.jpg" border="0" width="800"></a>

-----
## Gopigo approaches and faces the front of the target(vsgo05.py)
- Add the following code into the ``vision_system`` class in the ``vision_system.py``

```python
    # Gopigo(obj1) and obj2 face each other if gopigo rotates based on the result of this method(degree).
    def calc_face_angle(self,obj1,obj2):
        opposite_orientation_of_obj2 = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
        degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
        obj1_face_obj2 = opposite_orientation_of_obj2 - degree_of_obj1
        return obj1_face_obj2
```

- Copy ``vsgo03.py`` as ``vsgo05.py``
- Add ``gopigo_face_target_angle = vs.calc_face_angle(vs.markers[1],shoot_pos)`` after ``dist_between_gopigo_and_target = vs.calcDistance(vs.markers[1],shoot_pos)``
- Add the following ``elif`` before ``else:``.

```python
        elif abs(gopigo_face_target_angle) > 10:
            stat.gpg_mode = "turn"
            stat.gpg_turn_degree = gopigo_face_target_angle
```

- Execute ``vsgo05.py``.

# Vision system, gopigo, and opencv
## Gopigo shoots the target (vsgocv01.py)
- Copy ``vsgo05.py`` as ``vsgocv01.py``.
- Add the following import statements.

```python
import picamera
import picamera.array
import cv2
```

- Add the following picamera settings in the ``__init__`` method in the ``gopigo_control`` class.

```python
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
```

- Replace the ``move()`` method as follows.

```python
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
```

- Insert the following ``capture_frame()`` method in the ``gopigo_control`` class.

```python
    def capture_frame(self):
        cap_stream = picamera.array.PiRGBArray(self.camera,size=(self.width,self.height))
        self.camera.capture(cap_stream, format='bgr',use_video_port=True)
        frame = cap_stream.array
        return frame
```

- Insert the following code snippet after the ``frame = gpgc.capture_frame()``

```python
        cv2.imshow("Captured Image",frame)
        cv2.waitKey(1) #imshow requires waitKey()
```

- Replace the ``else`` statement in the ``__main__`` as follows.

```python
        elif stat.gpg_mode == "stop":
            pass
        else:
            stat.gpg_mode = "capture"
```

- Execute ``vsgocv01.py``.
- Gopigo will rotate, approach and face the front of the target.
- When Gopigo faces the target, it shoots the target and saves the image named ``capture.jpg``.

## Gopigo shows contours of the target(vsgocv02.py)
<a href="https://sites.google.com/site/ipbloit/2018/02/contours.jpg"><img src="/site/ipbloit/2018/02/contours.jpg" border="0" width="800"></a>

- Copy ``vsgocv01.py`` as ``vsgocv02.py``
- Add the following ``cv_control`` class in the ``vsgocv02.py``.

```python
class cv_control:
    def __init__(self):
        # key is an base h value of the color(e.x. 10 means skin color)
        # value indicates lower(0,1,2) and upper(3,4,5) hsv values
        self.lower = []
        self.upper = []
    
    def set_filter(self,base_hvalue):
        self.lower = numpy.array([base_hvalue-10, 100, 100], dtype = "uint8")
        self.upper = numpy.array([base_hvalue+10, 255, 255], dtype = "uint8")
    
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
```

- Add the following code snippet after ``stat = status()`` in the ``__main__``

```python
    cvc = cv_control()
    cvc.set_filter(170) # set lower and upper filter. base_hvalue "170" indicates "red".
```

- Add the following statement before ``cv2.waitKey(1)``

```python
contours = cvc.extract_contours(frame)
```

- Execute ``vsgocv02.py``.

## [***Exercise***] Shoot the green target in the center of the image.(vsgocv03.py)
- Gopigo will rotate, approach and face the front of the **green** target.
- If the cx of the green target exists between 200px ~ 440px and the area of the target is over 10000 px, gopigo shoots the target and save the image named ``green.jpg``.

## [***Final Exercise***] Shoot the green and the blue targets.(vsgocv04.py) 
- Prepare 2 targets(blue and green) and 1 vs-marker at start place.
- First, Gopigo will rotate, approach, face and shoot the **green** target.
- Gopigo will shoot and save the image of the green target.
  - cx of the target exists between 200px~440px
  - area of the target is over 10000px.
  - image is named ``cap_01.jpg``
- Gopigo will return to the start place.
- Next, gopigo will shoot the **blue** target like the green target, and save the image named ``cap_02.jpg``.
- Gopigo glows the LEDs blue while gopigo is heading to the blue target and glows the LEDs green while gopigo is heading to the green target.
- Finally, gopigo will return to the start place.
