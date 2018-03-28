import numpy 
import math

x1 = 300 #shooter
y1 = 300
x2 = 200 #target
y2 = 200

diffx = x2 - x1
diffy = y2 - y1

distance_from_obj1_to_obj2 = numpy.sqrt(diffx**2 + diffy**2)
print("distance_from_obj1_to_obj2:" + str(distance_from_obj1_to_obj2))
