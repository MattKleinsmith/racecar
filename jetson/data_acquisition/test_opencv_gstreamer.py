import numpy as np
import cv2

cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)24/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
#"nvcamerasrc sensor-id=0 ! \
#                        'video/x-raw(memory:NVMM),width=320,height=160,framerate=30/1,format=NV12' ! \
#                        nvvidconv flip-method=2 ! \
#                        omxh264enc ! \
#                        qtmux ! \
#                        appsink")
try:
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Display the resulting frame
        if ret:
            print frame
except KeyboardInterrupt: 
    # When everything done, release the capture
    cap.release()
