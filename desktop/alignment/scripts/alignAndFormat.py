import cv2
import h5py
import pandas as pd


def getClosestCommand(clock, commands):  
    commands['diffs'] = abs(commands['clock'] - clock)
    commandRow = commands.iloc[commands['diffs'].idxmin()]
    command = (commandRow['throttle'], commandRow['steering'])
    return command

PATH = '../data/'
ID = '2016-11-16--07-51-06'
START_MS = 15 * 1000
END_MS = (2 * 60 + 17) * 1000
FRAME_RATE = 30
CAM_SUFFIX = '.mp4'
CMD_SUFFIX = '_commands.csv'
CLOCK_SUFFIX = '_cam_clock.txt'
CAM_H5_SUFFIX = '_cam'
CMD_H5_SUFFIX = '_cmd'
H5_SUFFIX = '.h5'

prefix = PATH + ID
cam_filename = prefix + CAM_SUFFIX
cmd_filename = prefix + CMD_SUFFIX
with open(prefix + CLOCK_SUFFIX) as f:
    clock0 = int(f.readline().strip())
cap = cv2.VideoCapture(cam_filename)
cam_h5 = h5py.File(prefix + CAM_H5_SUFFIX + H5_SUFFIX, 'w')
commands = pd.read_csv(cmd_filename, header=None)
cmd_h5 = h5py.File(prefix + CMD_H5_SUFFIX + H5_SUFFIX, 'w')

commands.apply(pd.to_numeric)
commands.columns = ['clock', 'throttle', 'steering']

msPerFrame = 1000.0 / FRAME_RATE
firstFrameIndex = START_MS / msPerFrame
lastFrameIndex = END_MS / msPerFrame

ret, frame = cap.read()
height, width, nchannels = frame.shape
frameCount = (lastFrameIndex - firstFrameIndex) + 1
cam_dset = cam_h5.create_dataset('images',
                                 (frameCount, height, width, nchannels),
                                 dtype='uint8')
cmd_dset = cmd_h5.create_dataset('commands', (frameCount, 2))

cap.set(cv2.CAP_PROP_POS_FRAMES, firstFrameIndex)
clock = clock0 + START_MS
frameIndex = firstFrameIndex
while frameIndex != lastFrameIndex + 1:
    print str(frameIndex) + '/' + str(lastFrameIndex) + ' '*4 + str(int(clock))
    outputFrameIndex = frameIndex - firstFrameIndex
    ret, frame = cap.read()
    cam_dset[outputFrameIndex] = frame
    command = getClosestCommand(clock, commands)
    cmd_dset[outputFrameIndex] = command
    clock += msPerFrame
    frameIndex += 1
cap.release()
cam_h5.close()
cmd_h5.close()
