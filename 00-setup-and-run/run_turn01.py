import easygopigo3

pi = easygopigo3.EasyGoPiGo3()
pi.set_speed(50)
pi.drive_degrees(360,True) #Blocking method. Move 360 degree.
pi.turn_degrees(90,True)
print("forward 360 degrees, and turn right 90 degrees")
