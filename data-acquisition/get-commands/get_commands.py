import thread
import serial
import time
import sys


EXT_DRIVE = "/media/ubuntu/WD TB/"
DATETIME_FILE = "/tmp/camera_datetime.txt"
with open(DATETIME_FILE) as f:
    DATETIME = f.read().splitlines()[0]
SINK = EXT_DRIVE + DATETIME + "_log.csv"
JCLK0_FILE = EXT_DRIVE + DATETIME + "_jclk0.txt"
PORT = '/dev/rfcomm0'
BAUDRATE = 921600  # Why this number?
TIMEOUT = 1  # Why this number?
port = serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
def readThread(port):
    sys.stdout = open(SINK, "w")
    sys.stdout.write("aclk,throttle,steering\n")  # dataframe header
    jclk0 = int(time.time() * 1000)  # milliseconds
    with open(JCLK0_FILE, "w") as f:
        print >> f, str(jclk0)  # Write Jetson system clock time
    while True: # CPU-expensive
        sys.stdout.write(port.read(1024))
thread.start_new_thread(readThread, (port,))
while True:
    pass
    #TODO: Check for a STOP command. We won't be able to CTRL-C our way out.
