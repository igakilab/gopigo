import cv2
import numpy
import sys

WINNAME = "OpenCV Sample 01"
WIDTH = 640
HEIGHT = 480

if __name__ == '__main__':
    cv2.namedWindow(WINNAME)
    img = numpy.zeros((HEIGHT, WIDTH, 3))
    for r in range(256):
        for g in range(256):
            for b in range(256):
                img[...] = (b/255.0, g/255.0, r/255.0)
                print(img)

                cv2.imshow(WINNAME, img)
                if cv2.waitKey(10) %256 == ord('q'):
                    sys.exit(1)
