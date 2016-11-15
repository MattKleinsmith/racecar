datetime=$(date +"%Y-%m-%d--%H-%M-%S")
echo $datetime > $cameraDatetime
date +%s%3N > $usbDrive/${datetime}_cam_clock.txt
gst-launch-1.0 \
    nvcamerasrc sensor-id=0 ! \
    'video/x-raw(memory:NVMM),width=320,height=160,framerate=30/1,format=NV12' ! \
    nvvidconv flip-method=2 ! \
    omxh264enc ! \
    qtmux ! \
    filesink location=$usbDrive/$datetime.mp4 -ev
