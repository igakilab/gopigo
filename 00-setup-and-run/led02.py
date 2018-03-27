import easygopigo3
import time

pi = easygopigo3.EasyGoPiGo3()
white = (255,255,255) #8bit RGB value
pi.set_eye_color(white)
pi.open_eyes()
time.sleep(5)
pi.close_eyes()


