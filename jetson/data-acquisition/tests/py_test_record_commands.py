import os
import re
import time
import thread

from plumbum.cmd import sdptool, rfcomm, sudo
import serial


def readThread(inPort, outPort, outFile, outError):
  while True:   
    line = inPort.readline()
    mstime = str(time.time() * 1000)
    if len(line) == 7: # Valid format: '000,000'
      print >> outPort, line
      print >> outFile, mstime + "," + line
    else:
      print >> outError, mstime + "," + line

phone = os.environ['phone']
bluetooth = '/dev/rfcomm0' # Connected to Android
services = sdptool['browse', phone]()
jetsonRemoteControlService = services.split('Jetson Remote Control')[-1]
regex = re.compile('Channel: ([0-9]+)')
channel = regex.search(jetsonRemoteControlService).group(1)
sudo[rfcomm['release', bluetooth]]
sudo[rfcomm['bind', bluetooth, phone, channel]]
bluetooth = serial.Serial(bluetooth, 921600, timeout=3) # Connected to Android
usb = serial.Serial('/dev/ttyACM0', 115200, timeout=3) # Connected to Arduino
cmd_log = open('commands.csv', 'w')
cmd_err = open(cmd_log + '.error', 'w')

thread.start_new_thread(readThread, (bluetooth, usb, cmd_log, cmd_err))
try:
  while True:
    pass
except KeyBoardInterrupt:
  inPort.close()
  outPort.close()
  outFile.close()
  outError.close()
