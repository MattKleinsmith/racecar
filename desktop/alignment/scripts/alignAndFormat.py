import cv2
import h5py
import pandas as pd
import numpy as np


def getClosestCommand(clock, commands):  
    commands['diffs'] = abs(commands['clock'] - clock)
    commandRow = commands.iloc[commands['diffs'].idxmin()]
    command = (commandRow['throttle'], commandRow['steering'])
    return command

def milliseconds(hours, minutes, seconds):
    hms = (hours, minutes, seconds)
    msInSec = 1000
    secVector = (3600, 60, 1)
    return np.dot(secVector, hms) * msInSec

PATH = '../data/'
ID = '2016-11-16--07-51-06'
START_MS = milliseconds(hours=0, minutes=0, seconds=15)
END_MS   = milliseconds(hours=0, minutes=2, seconds=17)
FRAME_RATE = 30
CAM_SUFFIX = '.mp4'
CMD_SUFFIX = '_commands.csv'
CLOCK_SUFFIX = '_cam_clock.txt'
CAM_H5_SUFFIX = '_cam'
CMD_H5_SUFFIX = '_cmd'
H5_SUFFIX = '.h5'

prefix = PATH + ID
camFilename = prefix + CAM_SUFFIX
cmdFilename = prefix + CMD_SUFFIX
with open(prefix + CLOCK_SUFFIX) as f:
    clock0 = int(f.readline().strip())
cap = cv2.VideoCapture(camFilename)
camH5 = h5py.File(prefix + CAM_H5_SUFFIX + H5_SUFFIX, 'w')
commands = pd.read_csv(cmdFilename, header=None)
cmdH5 = h5py.File(prefix + CMD_H5_SUFFIX + H5_SUFFIX, 'w')

commands.apply(pd.to_numeric)
commands.columns = ['clock', 'throttle', 'steering']

msPerFrame = 1000.0 / FRAME_RATE
firstFrameIndex = START_MS / msPerFrame
lastFrameIndex = END_MS / msPerFrame

ret, frame = cap.read()
height, width, nchannels = frame.shape
frameCount = (lastFrameIndex - firstFrameIndex) + 1
camDset = camH5.create_dataset('images',
                                 (frameCount, height, width, nchannels),
                                 dtype='uint8')
throttleCmds = cmdH5.create_dataset('throttle', (frameCount, 1))
steeringCmds = cmdH5.create_dataset('steering', (frameCount, 1))

cap.set(cv2.CAP_PROP_POS_FRAMES, firstFrameIndex)
clock = clock0 + START_MS
frameIndex = firstFrameIndex
while frameIndex != lastFrameIndex + 1:
    print str(frameIndex) + '/' + str(lastFrameIndex) + ' '*4 + str(int(clock))
    outputFrameIndex = frameIndex - firstFrameIndex
    ret, frame = cap.read()
    camDset[outputFrameIndex] = frame
    throttle, steering = getClosestCommand(clock, commands)
    throttleCmds[outputFrameIndex] = throttle
    steeringCmds[outputFrameIndex] = steering
    clock += msPerFrame
    frameIndex += 1
cap.release()
camH5.close()
cmdH5.close()
