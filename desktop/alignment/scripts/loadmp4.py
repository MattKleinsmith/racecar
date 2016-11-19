import cv2


FILENAME = "../data/2016-11-16--07-51-06.avi"
cap = cv2.VideoCapture(FILENAME)
while not cap.isOpened():
    cap = cv2.VideoCapture(FILENAME)
    print "Wait for the header"
    cv2.waitKey(5000)
print cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
cap.release()
