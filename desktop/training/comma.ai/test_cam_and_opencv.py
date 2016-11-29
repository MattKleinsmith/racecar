#!/usr/bin/env python
import json
import time

import cv2
from keras.models import model_from_json


#cap = cv2.VideoCapture("""
#    nvcamerasrc sensor-id=0 !
#    'video/x-raw(memory:NVMM),width=320,height=160,framerate=30/1,format=NV12' !
#    nvvidconv flip-method=2 !
#    omxh264enc !
#    qtmux !
#    appsink""")
cap = cv2.VideoCapture("""
    nvcamerasrc !
    video/x-raw(memory:NVMM),
    width=(int)320,
    height=(int)160,
    format=(string)I420,
    framerate=(fraction)24/1 !
    nvvidconv flip-method=2 !
    video/x-raw,
    format=(string)BGRx !
    videoconvert !
    video/x-raw,
    format=(string)BGR !
    appsink""")
modelFilename = "./outputs/steering_model/steering_angle.json"
with open(modelFilename, 'r') as jfile:
    model = model_from_json(json.load(jfile))
model.compile("sgd", "mse")
weights_file = modelFilename.replace('json', 'keras')
model.load_weights(weights_file)
try:
    ret = True
    while ret: 
        start = time.time()
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        predicted_steers = model.predict(frame[None, :, :, :])[0][0] - 100
        print predicted_steers
except Exception or KeyboardInterrupt:
    print "#"*70
    print "exception"
    cap.release()
cap.release()
