#!/usr/bin/env python

import os
import re
from time import time

from plumbum.cmd import sdptool, sudo, rfcomm
from serial import Serial, SerialException

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String


def talker(bluetooth, cmdLog, cmdErr):
    pub = rospy.Publisher('commands', Twist, queue_size=10)
    rospy.init_node('bluetooth')
    try:
        while True: 
            msg = bluetooth.read(8)
            if msg:
                mstime = str(int(time() * 1000))
                if msg[-1] == '\n': # Valid format: '000,000\n'
                    # Log
                    cmdLog.write(mstime + "," + msg)
                    # Parse 
                    throttle = int(msg[:3])
                    steering = int(msg[4:7])
                    # Format 
                    twist = Twist()
                    twist.linear.x = throttle
                    twist.angular.z = steering
                    # Send
                    pub.publish(twist)
                else:
                    cmdErr.write(mstime + "," + msg)
    except Exception as e:
        print e
    except KeyboardInterrupt:
        print "KeyboardInterrupt" 
    finally:
        print "Closing bluetooth, cmdLog, and cmdErr"
        bluetooth.close()
        print "bluetooth closed"
        cmdLog.close()
        print "cmdLog closed"
        cmdErr.close()
        print "cmdErr closed"

if __name__ == '__main__':

    phone = os.environ['phone']
    services = sdptool['browse', phone]()
    jetsonRemoteControlService = services.split('Jetson Remote Control')[-1]
    regex = re.compile('Channel: ([0-9]+)')
    channel = regex.search(jetsonRemoteControlService).group(1)
    bluetoothDevice = os.environ['bluetooth'] # Connected to Android: e.g. /dev/rfcomm0
    sudo[rfcomm['release', bluetoothDevice]]()
    sudo[rfcomm['bind', bluetoothDevice, phone, channel]]()
    bluetooth = Serial(bluetoothDevice, 921600) # Connected to Android
    cmdFilename = 'commands.csv'
    cmdLog = open(cmdFilename + '.log', 'w')
    cmdErr = open(cmdFilename + '.error', 'w')

    talker(bluetooth, cmdLog, cmdErr)
