import time
import easygopigo3
pi = easygopigo3.EasyGoPiGo3()

pi.drive_cm(10) #Blocking method. Move 10cm.
print('10cm Moved')
