datetime=$(date +"%Y-%m-%d--%H-%M-%S")
exthdd="/media/ubuntu/WDTB/"
echo $datetime > /tmp/camera_datetime.txt
echo $exthdd > /tmp/external_hard_drive.txt
pathprefix=${exthdd}${datetime}
date +%s%3N > ${pathprefix}_cam_clock.txt
gst-launch-1.0 nvcamerasrc num-buffers=600 sensor-id=0 ! 'video/x-raw(memory:NVMM),width=320, height=160, framerate=30/1, format=NV12' ! nvvidconv flip-method=2 ! omxh264enc ! qtmux ! filesink location=${pathprefix}.mp4 -ev
