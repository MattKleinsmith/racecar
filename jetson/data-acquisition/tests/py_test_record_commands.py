import pdb
import sys

class ForkedPdb(pdb.Pdb):
  """A Pdb subclass that may be used
  from a forked multiprocessing child
  """
  def interaction(self, *args, **kwargs):
    _stdin = sys.stdin
    try:
      sys.stdin = file('/dev/stdin')
      pdb.Pdb.interaction(self, *args, **kwargs)
    finally:
      sys.stdin = _stdin

import os
import re
import time
from multiprocessing import Process, Queue

from plumbum.cmd import sdptool, sudo, rfcomm
from serial import Serial, SerialException


def saveCommands(bluetooth, queue, cmdWrite, cmdLog, cmdErr):
  print "Starting saveCommandsP"
  try:
    while True: 
      msg = bluetooth.read(8)
      if msg:
        mstime = str(int(time.time() * 1000))
        if msg[-1] == '\n': # Valid format: '000,000\n'
          queue.put(msg)
          cmdWrite.write(msg)
          cmdLog.write(mstime + "," + msg)
        else:
          cmdErr.write(mstime + "," + msg)
  except (KeyboardInterrupt, SerialException) as error:
    print "saveCommandsP received a KeyboardInterrupt/SerialException." 
    print error
  finally:
    print "Closing bluetooth, cmdWrite, cmdLog, and cmdErr"
    bluetooth.close()
    print "bluetooth closed"
    cmdWrite.close()
    print "cmdWrite closed"
    cmdLog.close()
    print "cmdLog closed"
    cmdErr.close()
    print "cmdErr closed\n"

def sendCommands(usb, handshake, queue, sendCommandsLog):
  print "Starting sendCommandsP\n"
  print "6"
  print queue
  try:
    freePass = True
    while True:
      cmd = queue.get()
      print "7"
      print queue
      msg = usb.read(1)
      print queue
      print msg
      sendCommandsLog.write(msg)
      if (msg and msg == handshake) or freePass:
        print "###########queue: "
        print queue
        print "###########"
        sendCommandsLog.write("GOT HERE2\n")
        sendCommandsLog.write("cmd len: " + str(len(cmd)) + "\n")
        sendCommandsLog.write(cmd)
        if len(cmd) == 8 and cmd[-1] == '\n':
          usb.write(cmd)
          freePass = False
  except KeyboardInterrupt:
    print "\nsendCommandsP received a KeyboardInterrupt."
  finally:
    usb.write('061,050\n') # Stop car 
    print "Stopping car"
    print "Closing sendCommandsLog and usb"
    sendCommandsLog.close() 
    print "sendCommandsLog closed"
    usb.close()
    print "usb closed\n"

if __name__ == '__main__':

  phone = os.environ['phone']
  services = sdptool['browse', phone]()
  jetsonRemoteControlService = services.split('Jetson Remote Control')[-1]
  regex = re.compile('Channel: ([0-9]+)')
  channel = regex.search(jetsonRemoteControlService).group(1)
  rfcommPort = '/dev/rfcomm0' # Connected to Android
  sudo[rfcomm['release', rfcommPort]]()
  sudo[rfcomm['bind', rfcommPort, phone, channel]]()
  bluetooth = Serial(rfcommPort, 921600) # Connected to Android
  cmdFilename = 'commands.csv'
  cmdWrite = open(cmdFilename, 'w')
  cmdLog = open(cmdFilename + '.log', 'w')
  cmdErr = open(cmdFilename + '.error', 'w')
  usb = Serial('/dev/ttyACM1', 115200) # Connected to Arduino
  usb.close()
  usb.open()
  handshake = "~"
  sendCommandsLog = open('sendCommandsLog', 'w')

  #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#

  queue = Queue()

  saveCommandsArgs = (bluetooth, queue, cmdWrite, cmdLog, cmdErr)
  saveCommandsP = Process(target=saveCommands, args=saveCommandsArgs)
  saveCommandsP.start()
  print "1"
  print queue
  sendCommandsArgs = (usb, queue, handshake, sendCommandsLog)
  sendCommandsP = Process(target=sendCommands, args=sendCommandsArgs) 
  print "2"
  print queue
  sendCommandsP.start() 
  print "3"
  print queue

  try:
    saveCommandsP.join()
    print "4"
    print queue
    sendCommandsP.join()
    print "5"
    print queue
  except (KeyboardInterrupt, SerialException) as error:
    print "\nError in Main\n"
