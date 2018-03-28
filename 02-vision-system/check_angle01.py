import numpy 
import math

x1 = 300 #shooter
y1 = 300
orientationx1 = 1
orientationy1 = -1
x2 = 200 #target
y2 = 200

diffx = x2 - x1
diffy = y2 - y1

degree_to_obj2 = numpy.rad2deg(math.atan2(diffy,diffx))
degree_of_obj1 = numpy.rad2deg(math.atan2(orientationy1,orientationx1))
obj1_to_obj2 = degree_to_obj2 - degree_of_obj1
print("degree_to_obj2:" + str(degree_to_obj2))
print("degree_of_obj1:" + str(degree_of_obj1))
print("obj1_to_obj2:" + str(obj1_to_obj2))
