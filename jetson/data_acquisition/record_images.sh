datetime=$(date +"%Y-%m-%d--%H-%M-%S")
echo $datetime > $cameraDatetime
date +%s%3N > $usbDrive/${datetime}_cam_clock.txt
gst-launch-1.0 \
    nvcamerasrc ! \
    'video/x-raw(memory:NVMM),
    width=(int)320,
    height=(int)160,
    format=(string)I420,
    framerate=(fraction)24/1' ! \
    nvvidconv flip-method=2 ! \
    'video/x-raw,
    format=(string)BGRx' ! \
    videoconvert ! \
    'video/x-raw, \
    format=(string)BGR' ! \
    filesink location=$usbDrive/$datetime.mp4 -ev
