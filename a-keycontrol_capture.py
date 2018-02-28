import getch # Key input library
import easygopigo3
import picamera
import cv2
import curses
import io
import numpy

WINNAME = "keycontrol_capture"
WIDTH=640
HEIGHT=480

if __name__ == '__main__':
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.noecho()

    cv2.namedWindow(WINNAME)
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH,HEIGHT)
    imgStream = io.BytesIO()
    
    egpi = easygopigo3.EasyGoPiGo3()
    egpi.set_speed(50) #0~1000 sitei

    while True:
        camera.capture(imgStream, format='jpeg') #capture as jpeg format image
        data = numpy.fromstring(imgStream.getvalue(), dtype=numpy.uint8) # translate numpy
        frame = cv2.imdecode(data, 1) #data to image
        cv2.imshow(WINNAME, frame)
        
        w = stdscr.getch() #non blocking, returns int value
        if w!=-1:#Print Inputted key value
            stdscr.move(1,0)
            stdscr.clrtoeol()
            stdscr.addstr(1,0,str(w))
        if w==ord('w'):
            egpi.forward()
        elif w==ord('s'):
            egpi.backward()
        elif w==ord('d'):
            egpi.right()
        elif w==ord('a'):
            egpi.left()
        elif w==ord('x'):
            egpi.stop()
        elif w==ord('q'):
            break
    #Clean up curses.
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
