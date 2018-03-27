import easygopigo3
import curses

#Non blocking key control
if __name__ == '__main__':
    #Curses setup
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.noecho()
    
    egpi = easygopigo3.EasyGoPiGo3()
    egpi.set_speed(50)
    
    while True:
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
