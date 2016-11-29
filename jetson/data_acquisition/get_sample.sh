gst-launch-1.0 \
    nvcamerasrc ! \
    'video/x-raw(memory:NVMM),
    width=320,
    height=160,
    format=I420,
    framerate=24/1' ! \
    nvvidconv flip-method=2 ! \
    'video/x-raw,
    format=BGRx' ! \
    videoconvert ! \
    'video/x-raw, \
    format=BGR' ! \
    filesink location=sample.mp4 -ev
