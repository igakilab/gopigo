import easygopigo3
import time

pi = easygopigo3.EasyGoPiGo3()
pi.set_speed(50)
print("non-blocking method")

pi.forward #non-blocking method
time.sleep(2)
pi.left()
time.sleep(2)
pi.stop()

