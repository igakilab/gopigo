import numpy 
import math

x1 = 300 #shooter
y1 = 300
x2 = 200 #target
y2 = 200

diffx = x2 - x1
diffy = y2 - y1

distance_between_obj1_and_obj2 = numpy.sqrt(diffx**2 + diffy**2)
print("distance_between_obj1_and_obj2:" + str(distance_between_obj1_and_obj2))
