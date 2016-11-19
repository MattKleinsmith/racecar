import cv2
import h5py


PATH = '../data/'
ID = '2016-11-16--07-51-06'
CAM_H5_SUFFIX = '_cam'
CMD_H5_SUFFIX = '_cmd'
H5_SUFFIX = '.h5'

TEXT_COORD = (130, 100)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE = 1
FONT_COLOR = (255, 255, 255)
THICKNESS = 2
LINE_TYPE = cv2.LINE_AA
WINDOW_TITLE = 'OpenCV'

prefix = PATH + ID
cam_h5 = h5py.File(prefix + CAM_H5_SUFFIX + H5_SUFFIX, 'r')
cam_dset = cam_h5['images']
cmd_h5 = h5py.File(prefix + CMD_H5_SUFFIX + H5_SUFFIX, 'r')
cmd_dset = cmd_h5['commands']

for frameIndex in xrange(len(cam_dset)):
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
