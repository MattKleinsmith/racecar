import cv2
import h5py


FILENAME = "../data/2016-11-16--07-51-06.mp4"
cap = cv2.VideoCapture(FILENAME)
while not cap.isOpened():
    cap = cv2.VideoCapture(FILENAME)
    cv2.waitKey(5000)
    print "Wait for the header"
print cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
print cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

try:
    while True:
        ret, frame = cap.read()
        print ret
        if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
            break
        try:
            cv2.imshow('frame', frame)
        except cv2.error as e:
            print e
            break
except Exception as e:
    print e
cap.release()
