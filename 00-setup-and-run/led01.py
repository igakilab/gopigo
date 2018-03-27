import easygopigo3
import time

pi = easygopigo3.EasyGoPiGo3()
pi.open_eyes()
time.sleep(5)
pi.close_eyes()


