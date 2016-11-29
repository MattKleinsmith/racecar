#!/usr/bin/env python
import argparse
import numpy as np
import cv2
import json
from keras.models import model_from_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Path viewer')
    parser.add_argument('model', type=str, help='Path to model definition json. Model weights should be on the same path.')
    args = parser.parse_args()

    with open(args.model, 'r') as jfile:
        model = model_from_json(json.load(jfile))
    model.compile("sgd", "mse")
    weights_file = args.model.replace('json', 'keras')
    model.load_weights(weights_file)

    cap = cv2.VideoCapture("""
    nvcamerasrc sensor-id=0 !
    'video/x-raw(memory:NVMM),width=320,height=160,framerate=30/1,format=NV12' !
    nvvidconv flip-method=2 !
    omxh264enc !
    qtmux !
    appsink""")
#    cap = cv2.VideoCapture("""
#    nvcamerasrc !
#    video/x-raw(memory:NVMM),
#    width=(int)2592,
#    height=(int)1458,
#    format=(string)I420,
#    framerate=(fraction)30/1 !
#    nvvidconv flip-method=2 !
#    video/x-raw,
#    format=(string)BGRx !
#    videoconvert !
#    video/x-raw,
#    format=(string)BGR !
#    appsink""")
    import time
    try:
        ret = True
        while ret: 
            start = time.time()
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #        frame = cv2.resize(frame, (320, 160))
    #        print time.time() - start 
    #        predicted_steers = model.predict(frame[None, :, :, :])[0][0] - 100
    #        print predicted_steers
    except KeyboardInterrupt:
        cap.release()
    cap.release()
