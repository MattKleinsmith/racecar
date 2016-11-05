import os
import re
import time
import thread

from plumbum.cmd import sdptool, sudo, rfcomm
import serial
from serial import SerialException


def saveCommands(bluetooth, cmdWrite, cmdLog, cmdErr):
  while True: 
    msg = bluetooth.read(8)
    if msg:
      mstime = str(int(time.time() * 1000))
      if msg[-1] == '\n': # Valid format: '000,000\n'
        cmdWrite.write(msg)
        cmdWrite.flush()
        cmdLog.write(mstime + "," + msg)
      else:
        cmdErr.write(mstime + "," + msg)

def saveArduinoLog(usb, inoLogWrite):
  while True:
    msg = usb.read(1)
    print '[' + msg + ']'
    if msg:
      inoLogWrite.write(msg)
      inoLogWrite.flush()

def sendCommands(inoLogRead, handshake, cmdRead, usb, sendCommandsLog):
  while True:
    #msg = inoLogRead.read(1)
    msg = usb.read(1)
    sendCommandsLog.write(msg)
    if msg and msg == handshake:
      cmd = cmdRead.read(8)
      sendCommandsLog.write("GOT HERE2\n")
      sendCommandsLog.write("cmd len: " + str(len(cmd)) + "\n")
      sendCommandsLog.write(cmd)
      if len(cmd) == 8 and cmd[-1] == '\n':
        usb.write(cmd)

phone = os.environ['phone']
services = sdptool['browse', phone]()
jetsonRemoteControlService = services.split('Jetson Remote Control')[-1]
regex = re.compile('Channel: ([0-9]+)')
channel = regex.search(jetsonRemoteControlService).group(1)
rfcommPort = '/dev/rfcomm0' # Connected to Android
sudo[rfcomm['release', rfcommPort]]()
sudo[rfcomm['bind', rfcommPort, phone, channel]]()
bluetooth = serial.Serial(rfcommPort, 921600) # Connected to Android
cmdFilename = 'commands.csv'
cmdWrite = open(cmdFilename, 'w')
cmdLog = open(cmdFilename + '.log', 'w')
cmdErr = open(cmdFilename + '.error', 'w')
cmdRead = open(cmdFilename, 'r')
usb = serial.Serial('/dev/ttyACM1', 115200) # Connected to Arduino
usb.close()
usb.open()
inoLogFilename = 'arduinoLog'
inoLogWrite = open(inoLogFilename, 'w')
inoLogRead = open(inoLogFilename, 'r')
handshake = "~"
sendCommandsLog = open('sendCommandsLog', 'w')

#thread.start_new_thread(saveArduinoLog, (usb, inoLogWrite))
thread.start_new_thread(saveCommands, (bluetooth, cmdWrite, cmdLog, cmdErr))
try:
  sendCommands(inoLogRead, handshake, cmdRead, usb, sendCommandsLog)
except (KeyboardInterrupt, SerialException) as err:
  usb.write('061,050\n') # Stop car
  print 'test' + ('#' * 80)
  print err
  bluetooth.close()
  cmdWrite.close()
  cmdLog.close()
  cmdErr.close()
  cmdRead.close()
  usb.close()
  inoLogWrite.close()
  inoLogRead.close()
  sendCommandsLog.close()
