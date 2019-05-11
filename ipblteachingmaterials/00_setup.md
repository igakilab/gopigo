# Preparation
## Hardware/Software list
- Hardware
  - Laptop-PC * 1
  - USB Web camera * 1
  - Robot: Gopigo3 with Raspberry pi and pi camera * 1
    - OS of GoPiGo is already installed in SD Card
      - https://www.dexterindustries.com/howto/install-raspbian-for-robots-image-on-an-sd-card/
  - batteries * 8
    - each gopigo requires 8 batteries
  - USB power adapter for raspberry pi
  - LAN Cable
- Software
  - OS: Windows
    - Microsoft Office
    - visual studio code
    - vision system
    - UltraVNC
    - RLogin
    - Logicool WebCamera utility
  - OS: Raspbian for Robots(Gopigo)
    - Robot software: Gopigo3 python library
    - Image processing library: OpenCV

## Gopigo Setup
- Assemble GoPiGo
  - [Assemble Gopigo manual](https://www.dexterindustries.com/GoPiGo/get-started-with-the-gopigo3-raspberry-pi-robot/1-assemble-gopigo3/)
- Connect PiCamera
  - [Attach Picamera manual](https://www.dexterindustries.com/GoPiGo/get-started-with-the-gopigo3-raspberry-pi-robot/4-attach-the-camera-and-distance-sensor-to-the-raspberry-pi-robot/)
- Setup battery case and connect power plug to gopigo.
- Connect USB power adapter
  - you can use gopigo without usb power adapter.
- Power ON
  - Connecting USB power adapter or pushing the button over the micro-USB connector turns on the gopigo.
<img src="https://sites.google.com/site/ipbloit/2019/00/gopigoconnect.jpg" border="0" width="320" height="230">
- Connect PC and gopigo (in the front) with LAN cable
  - Change Wired Network Settings as follows
    - PC and gopigo must belong the same network segment.
<img src="https://sites.google.com/site/ipbloit/2019/00/wirednetworksettings.jpg" border="0" width="600">
- Access Raspbian for Robots with Internet Explorer
  - Start Internet Explorer, and access http://192.168.0.2/
<img src="https://sites.google.com/site/ipbloit/2019/00/novncenter.jpg" border="0" width="320">
  - Click VNC icon(Launch VNC)
  - input Password [robots1234]
  - You can access Raspbian OS view.
<img src="https://sites.google.com/site/ipbloit/2019/00/raspbian1.jpg" border="0" width="600">
- You can access Raspbian for Robots with UltraVNC.exe
  - Start UltraVNC Viewer
  - Input[``192.168.0.2:0``] and Connect.
<img src="https://sites.google.com/site/ipbloit/2019/00/ultravnc.jpg" border="0" width="320">
  - UltraVNC enables users to copy and paste text between windows pc and the raspbian.
  - I recommend to use wired connection(192.168.0.2) during development with UltraVNC.
- Execute DI Software updates
- Setup wireless network
  - Click Wifi Setup in the raspbian.
  - Click Scan button and select indicated SSID.
  - Confirm SSID and input password.
  - Add
  - Connect in the Current Status.
<img src="https://sites.google.com/site/ipbloit/2019/00/wifisetting.jpg" border="0" width="600">
  - You can also access Raspbian with wifi IP address
- Power OFF
  - Click Shutdown icon, and disconnect micro USB cable.
  - Push Power button.

## Software in Raspbian
### Command line terminal
- Click command line terminal icon in raspbian
<img src="https://sites.google.com/site/ipbloit/2019/00/commandline.jpg" border="0" width="600">
- You can copy and paste all commands in this education materials.
  - Right click copy and paste also can be available.
  - You cannot copy and paste between windows and raspbian through noVNC.
  - If you want to C&P any commands or source code, you should use UltraVNC.

### Text Editor and IDE
- You can use a geany editor in the raspbian.
- You can launch geany and open file by the following command in the raspbian.

```
$ geany [filename] &
```

- You can run python program on terminal or geany. You can run python program for just pushing ``F5`` on geany.
<a href="https://sites.google.com/site/ipbloit/2019/00/geany.jpg"><img src="/site/ipbloit/2019/00/geany.jpg" border="0" width="600"></a>

### Image Viewer
- You can view images with using gpicview.

```
$ gpicview [imagefilename]
```

<a href="https://sites.google.com/site/ipbloit/2019/00/gpicview.jpg"><img src="/site/ipbloit/2019/00/gpicview.jpg" border="0" width="600"></a>

# Try GoPiGo
- We can use python API library for GoPiGo control.In the following, let's study how to use such APIs and basic python programming.
  - https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html
-----
## Simple GoPiGo API
### Run 360 degree (run360_01.py)
- Access to the raspbian in the GoPiGo (Recommend to use UltraVNC).
- Launch Command Line Terminal.
- Input the following commands sequentially on the terminal.
  - these commands indicate making python program for GoPiGo Run.

```
$ mkdir ipbl
$ cd ipbl
$ geany run360_01.py &
```

- Type (or copy and paste) the following code and save it as ``run360_01.py``.
- In this program, the Gopigo goes straight until the motor turns 360 degrees.
  - One rotation of the motor indicates 360 degree.

```python
import easygopigo3

pi = easygopigo3.EasyGoPiGo3()
pi.drive_degrees(360,True) #Blocking method. Move 360 degree.
print("360 degree moved")
```

- Execute ``run360_01.py``
  - You have 2 options to execute python program. Choose it.
- Type python command on the command line terminal.

```
$ python run360_01.py
```

- or just hit **``F5``** key on the geany editor after saving the source code.

-----
### Stop gopigo (stop.py)
- This ``stop.py`` just stop gopigo. If you develop and execute wrong program, you should execute ``stop.py`` to stop the gopigo.

```
$ geany stop.py &
```

- Type (or copy and paste) the following code and save it as ``stop.py``.

```python
import easygopigo3

pi = easygopigo3.EasyGoPiGo3()
pi.stop()
print("stopped")
```

- Execute ``stop.py``
- You have 2 options to execute python program. Choose it.
- 1st one is using command line terminal as follows.

```
$ python stop.py
```

- or just hit **``F5``** key on the geany editor after saving the source code.

-----
### Speed control (run360_02.py)
- copy the ``run360_01.py`` as ``run360_02.py``

```
$ cp run360_01.py run360_02.py
```

- Insert the following code after the line of ``pi = easygopigo3.EasyGoPiGo3()`` in the ``run360_02.py``.

```python
pi.set_speed(50)
```

- Execute ``run360_02.py``
- You can see the gopigo move slowly.
- The default speed of the gopigo is 300 (Max value is 500 in this PBL).

-----
### Run and turn (run_turn01.py)
- Gopigo goes straight until the motor turns 360 degrees and turns 90 degrees to the right.
- Copy the run360_02.py as ``run_turn01.py``.
- Insert the following code after the line of ``pi.drive_degrees(360,True)``.

```
pi.turn_degrees(90,True)
```

### [***Exercise***] (run_turn02.py)
- In this program, gopigo goes straight until the motor turns 360 degrees and turns 90 degrees to the ***left***.

-----
### LED (led01.py)
- Type (or copy and paste) the following code and save it as ``led01.py``.

```python
import easygopigo3
import time

pi = easygopigo3.EasyGoPiGo3()
pi.open_eyes()
time.sleep(5)
pi.close_eyes()
```

- Execute ``led01.py``
- Gopigo's 2 leds is turned on for 5 seconds.

-----
### Change the color of LED(led02.py)
- Copy the ``led01.py`` as ``led02.py``
- Add the following code before ``pi.open_eyes`` in the ``led02.py``.

```python
white = (255,255,255) #8bit RGB value
pi.set_eye_color(white)
```

- Execute ``led02.py``
- The color of the gopigo's 2 leds are changed in white.

-----
### Use method for changing the color of LED (led03.py)
- Type (or copy and paste) the following code and save it as ``led03.py``.

```python
import easygopigo3
import time

def change_color(color):
    pi.set_eye_color(color)
    pi.open_eyes()
    time.sleep(5)

pi = easygopigo3.EasyGoPiGo3()
white = (255,255,255) #8bit RGB value
change_color(white)
pi.close_eyes()
```

- Execute ``led03.py``

-----
### [***Exercise***] (led04.py)
- In this program, first, gopigo glows white for 5 seconds, and then gopigo glows magenta(255,0,255) for 5 seconds.

### Other LED control APIs
- About LED control, you can use many methods as stated in the [gopigo3 API](https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html)
- ``set_left_eye_color(color),set_right_eye_color(color), open_left_eye(), open_right_eye(), close_left_eye(), close_right_eye()``.

-----
## Blocking Method and Non-Blocking Method
- In the [gopigo API docs](https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html), Blocking method will wait for the GoPiGo3 robot to finish moving.Non-Blocking method will exit immediately while the GoPiGo3 robot will continue moving.

-----
### Run and turn (run_turn03.py) (Non-Blocking)
- In this program, gopigo goes straight for 2 seconds and turn left for 2 seconds.
- The forward() method and the left() method are the non-blocking methods.
- Type (or copy and paste) the following code and save it as ``run_turn03.py``.

```python
import easygopigo3
import time

pi = easygopigo3.EasyGoPiGo3()
pi.set_speed(50)

print("non-blocking method")
pi.forward() #non-blocking method
time.sleep(2)
pi.left()
time.sleep(2)
pi.stop()
```

- Execute the ``run_turn03.py``
- Compare the ``run_turn03.py`` with the ``run_turn01.py``.
  - In the ``run_turn01.py``, the second argument of the drive_degree(360,True) method ``True`` means the method is the blocking method.
- Try to remove ``time.sleep(2)`` from ``run_turn03.py``

-----
### Key control (key_control01.py) (Non-Blocking)
- Control Gopigo with Key Input using curses library.
- ``w`` means forward, and ``x`` means stop.
- ``d`` means right and ``a`` means left.
- ``q`` means ``break`` the loop.
- Type (or copy and paste) the following code and save it as ``key_control01.py``.

```python
import easygopigo3
import curses

#Non blocking key control
#Curses setup
stdscr = curses.initscr()
stdscr.nodelay(1) #non-blocking mode
curses.noecho()

egpi = easygopigo3.EasyGoPiGo3()
egpi.set_speed(50)

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

- Execute ``key_control01.py``

-----
### [***Exercise***] (key_control02.py)
- Add ``back`` function into ``key_control01.py`` as ``key_control02.py``.
  - See [gopigo API](https://gopigo3.readthedocs.io/en/master/api-basic/easygopigo3.html)
- In ``key_control02.py`` , a user can back the gopigo with ``s`` key.

-----
## Use Python class
- Long code introduces many bugs. Complicated behaviors in the program should be consisted of many short code.
- Python class enables us to divide complicated long code into many short code.

-----
### Refactoring run and turn program with python class (run_turn04.py)
- Add gopigo_control class to the ``run_turn03.py`` as ``run_turn04.py``.
- Type (or copy and paste) the following code and save it as ``run_turn04.py``.

```python
import easygopigo3
import time

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
    
    def move(self):#Every class method has self as 1st argument.
        self.pi.forward() #non-blocking method
        time.sleep(2)
        self.pi.left()
        time.sleep(2)
        self.pi.stop()    

if __name__ == '__main__':
    gpg = gopigo_control()
    gpg.move()
```

- Execute ``run_turn04.py``

-----
### Simple Auto gopigo (go_back01.py) (Blocking)
- Gopigo goes straight until the motor turns 720 degrees and goes back until the motor turns 720 degrees.
- Copy the ``run_turn04.py`` as the ``go_back01.py``.
- Replace code in the `move()` method as follows.

```python
self.pi.drive_degrees(720,True) #Blocking
self.pi.drive_degrees(-720,True) #Blocking
```

- Execute ``go_back01.py``.

-----
### gopigo with encoders (go_back02.py) (Non-Blocking)
- Gopigo goes straight until the motor turns 720 degrees and goes back until the motor turns 720 degrees with non-blocking method.
- The following methods in this program are non-blocking.
  - set_speed(),forward(),backward(),stop(),reset_encoders(),target_reached(),read_encoders()
- Type (or copy and paste) the following code and save it as ``go_back02.py``.

```python
import easygopigo3

class gopigo_control:
    def __init__(self):
        self.pi = easygopigo3.EasyGoPiGo3()
        self.pi.set_speed(50)
        self.pi.reset_encoders() # reset value of the encoders
        
        self.left_motor1 = 720
        self.right_motor1 = 720
        self.left_motor2 = -720
        self.right_motor2 = -720
    
    def move(self):
        pass

if __name__ == '__main__':
    gpg = gopigo_control()
    
    gpg.pi.forward()
    while True:
        print(str(gpg.pi.read_encoders())) #Show encoder values
        if (gpg.pi.target_reached(gpg.left_motor1,gpg.right_motor1) == True):
            gpg.pi.reset_encoders()
            gpg.pi.backward()
        elif (gpg.pi.target_reached(gpg.left_motor2,gpg.right_motor2) == True):
            gpg.pi.stop()
            break;
```

- Execute ``go_back02.py``
- This program includes complicated logic in ``__main__``.

-----
### gopigo with status class (go_back03.py) (Non-Blocking)
- Insert the following ``check_encoders`` method into ``gopigo_control`` class.

```python
    def check_encoders(self,status):
        print(str(self.pi.read_encoders()))
        if (self.pi.target_reached(self.left_motor1,self.right_motor1) == True):
            self.pi.reset_encoders()
            status.drive_mode = "b"
        elif (gpg.pi.target_reached(gpg.left_motor2,gpg.right_motor2) == True):
            status.drive_mode = "s"
```

- Replace the ``move`` method in the ``gopigo_control`` class as follows.

```python
    def move(self,status):
        if(status.drive_mode=="f"):
            self.pi.forward()
        elif(status.drive_mode=="b"):
            self.pi.backward()
        elif(status.drive_mode=="s"):
            self.pi.stop()
```

- Add the following ``gopigo_status`` class after the ``gopigo_control`` class.

```python
class gopigo_status:
    def __init__(self):
        self.drive_mode = "f" # f/b/s-> forward,back,stop
```

- Replace the ``__main__`` method as follows.

```python
if __name__ == '__main__':
    gpg = gopigo_control()
    status = gopigo_status()
    
    while True:
        gpg.check_encoders(status)
        gpg.move(status)
```

-----
### [***Exercise***] gopigo draw the triangle (gopigo_triangle.py)
- Copy ``go_back03.py`` as ``gopigo_triangle.py``. Use only non-blocking method with status class.
1. Go straight. 
1. Turn 90 degrees to the right and go straight. 
1. Turn 135 degree to the right and go straight until gopigo returning start point.

### [***Exercise***] go and back repeatedly(go_back04.py) (non-blocking)
- Copy ``go_back03.py`` as ``go_back04.py`` and customize the source code with reference to ``key_control01.py``
1. Gopigo goes straight until the motor turns 720 degrees and it goes back until the motor turns 720 degrees with non-blocking methods.
1. Gopigo repeats forward and backward again and again.
1. User can stop the gopigo with `s` key, and user can break the program with `q` key.
1. If the user presses the `s` key while the gopigo is stopped, the gopigo moves again. 
1. 2 LEDs of the gopigo glows ``blue`` during going forward, and it glows ``red`` during going backward.
