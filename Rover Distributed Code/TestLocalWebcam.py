import cv2
import imutils

vid = cv2.VideoCapture(1)

while vid.isOpened():
    while True:
        ret, frame = vid.read()
        cv2.imshow('Webcam View', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()
