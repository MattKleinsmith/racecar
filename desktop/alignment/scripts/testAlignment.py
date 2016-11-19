import cv2
import h5py
import pandas as pd


PATH = '../data/'
ID = '2016-11-16--07-51-06'
FRAME_RATE = 30
START_MS = 15 * 1000
END_MS = (2 * 60 + 17) * 1000

TEXT_COORD = (130, 100)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 1
FONT_COLOR = (255, 255, 255)
THICKNESS = 2
LINE_TYPE = cv2.LINE_AA
WINDOW_TITLE = 'OpenCV'

cam_h5 = h5py.File(PATH + ID + '_cam.h5', 'r')
cam_dset = cam_h5['images']
cmd_h5 = h5py.File(PATH + ID + '_cmd.h5', 'r')
cmd_dset = cmd_h5['commands']

msPerFrame = 1000.0 / FRAME_RATE
firstFrameIndex = START_MS / msPerFrame
lastFrameIndex = END_MS / msPerFrame

frameIndex = firstFrame
while frameIndex != lastFrameIndex + 1:
    frame = cam_dset[frameIndex]
    command = cmd_dset[frameIndex]
    text = str(command[1])
    cv2.putText(frame, text, TEXT_COORD, FONT, FONT_SIZE, FONT_COLOR, THICKNESS, LINE_TYPE)
    cv2.imshow(WINDOW_TITLE, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frameIndex += 1
cam_h5.close()
cmd_h5.close()
