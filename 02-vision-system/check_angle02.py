import numpy 
import math

#x1 = 200 #shooter
#y1 = 200
#orientationx1 = -1
#orientationy1 = -1
obj1 = [200,200,-1,-1]
#x2 = 200 #target
#y2 = 200
#orientationx1 = 0
#orientationy1 = 1
obj2 = [200,200,0,1]

opposite_orientation_of_obj2 = numpy.rad2deg(math.atan2(obj2[3]*-1,obj2[2]*-1))
degree_of_obj1 = numpy.rad2deg(math.atan2(obj1[3],obj1[2]))
obj1_face_obj2 = opposite_orientation_of_obj2 - degree_of_obj1
print("opposite_orientation_of_obj2:" + str(opposite_orientation_of_obj2))
print("degree_of_obj1:" + str(degree_of_obj1))
print("obj1_face_obj2:" + str(obj1_face_obj2))
