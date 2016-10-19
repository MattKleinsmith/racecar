export datetime=$(date +"%Y-%m-%d--%H-%M-%S")
echo $datetime > /tmp/camera_datetime.txt
date +%s%3N > /media/ubuntu/WD\ TB/$datetime$(echo _cam_clock).txt
gst-launch-1.0 nvcamerasrc num-buffers=400 sensor-id=0 ! 'video/x-raw(memory:NVMM),width=320, height=160, framerate=30/1, format=NV12' ! nvvidconv flip-method=2 ! omxh264enc ! qtmux ! filesink location=/media/ubuntu/WD\ TB/$datetime$(echo _cam).mp4 -ev
