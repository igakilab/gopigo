import cv2

WINNAME = "OpenCV Sample 01-a"
WIDTH = 640
HEIGHT = 480

if __name__ == '__main__':
    cv2.namedWindow(WINNAME)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit(1)

    while True:
        _, frame = cap.read()
        frame.resize((HEIGHT, WIDTH, 3))
        cv2.imshow(WINNAME, frame)

        key = cv2.waitKey(5)
        print(key)
        if key%256 == ord('q'):
            break
