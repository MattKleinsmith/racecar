import pdb
import sys
import subprocess

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
from time import time, sleep
from multiprocessing import Process, Pipe

from plumbum.cmd import sdptool, sudo, rfcomm
from serial import Serial, SerialException


def saveCommands(bluetooth, pipeIn, cmdWrite, cmdLog, cmdErr):
    bluetooth.close()
    bluetooth = open('cmdbluetooth.csv')
    print "Starting saveCommandsP"
    try:
        while True: 
            msg = bluetooth.read(8)
            if msg:
                if msg[-1] == '\n': # Valid format: '000,000\n'
                    sleep(0.001)
                    mstime = str(int(time() * 1000))
                    pipeIn.send(msg)
                    cmdWrite.write(msg)
                    cmdLog.write(mstime + "," + msg)
                else:
                    mstime = str(int(time() * 1000))
                    cmdErr.write(mstime + "," + msg)
    except (KeyboardInterrupt, SerialException) as error:
        print "\nsaveCommandsP received a KeyboardInterrupt/SerialException." 
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
        print "cmdErr closed"

def sendCommands(pipeOut, usb, handshake, endCommandsLog):
    print "Starting sendCommandsP\n"
    try:
        #freePass = True
        while True:
            sleep(0.001)
            cmd = pipeOut.recv()
            #msg = usb.read(1)
            #print msg
            #sendCommandsLog.write(msg)
            #if (msg and msg == handshake) or freePass:
            #if True:
                #sendCommandsLog.write("GOT HERE2\n")
                #sendCommandsLog.write("cmd len: " + str(len(cmd)) + "\n")
            sendCommandsLog.write(cmd)
            if len(cmd) == 8 and cmd[-1] == '\n':
                usb.write(cmd)
                    #freePass = False
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

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#

    pipeIn, pipeOut = Pipe()

    saveCommandsArgs = (bluetooth, pipeIn, cmdWrite, cmdLog, cmdErr)
    saveCommandsP = Process(target=saveCommands, args=saveCommandsArgs)
    saveCommandsP.start()
        
    sendCommandsArgs = (pipeOut, usb, handshake, sendCommandsLog)
    sendCommandsP = Process(target=sendCommands, args=sendCommandsArgs) 
    sendCommandsP.start() 
        
    try:
        saveCommandsP.join()
        sendCommandsP.join()
    except (KeyboardInterrupt, SerialException) as error:
        print "\nError in Main\n"
    finally:
        subprocess.call(['./ratioMsCmd.sh'])
