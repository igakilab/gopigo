import easygopigo3

pi = easygopigo3.EasyGoPiGo3()
pi.set_speed(50)
pi.drive_degrees(360,True) #Blocking method. Move 360 degree.
print('360 degree moved')
