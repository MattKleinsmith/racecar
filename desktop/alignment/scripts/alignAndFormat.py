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
FRAME_RATE = 30
START_MS = 15 * 1000
END_MS = (2 * 60 + 17) * 1000
CAM_FILENAME = PATH + ID + '.mp4'
CMD_FILENAME = PATH + ID + '_commands.csv'
with open(PATH + ID + '_cam_clock.txt') as f:
    CLOCK0 = int(f.readline().strip())

cap = cv2.VideoCapture(CAM_FILENAME)
cam_h5 = h5py.File(PATH + ID + '_cam.h5', 'w')
commands = pd.read_csv(CMD_FILENAME, header=None)
cmd_h5 = h5py.File(PATH + ID + '_cmd.h5', 'w')

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
clock = CLOCK0 + START_MS
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
