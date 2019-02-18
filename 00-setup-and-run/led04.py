import easygopigo3
import time

def change_color(color):
    pi.set_eye_color(color)
    pi.open_eyes()
    time.sleep(5)

pi = easygopigo3.EasyGoPiGo3()
white = (255,255,255) #8bit RGB value
change_color(white)
change_color((255,0,255)) #magenta
pi.close_eyes()
