import numpy
import cv2

img = cv2.imread("cap.jpg",0) # gray scale
cv2.imwrite("cap_gray.jpg",img)
