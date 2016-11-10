#!/usr/bin/env python
# MIT License

import sys
import os

import rospy
from sensor_msgs.msg import Joy


def callback(data, args):
    stamp = data.header.stamp
    stamp = stamp.secs * 10**3 + stamp.nsecs / 10.0**6
    if data.buttons[6]:
        throttle = -1
    elif data.buttons[7]:
        throttle = 1
    else:
        throttle = 0
    steering = data.axes[0] 
    csv = args[0]
    stamp = '{0:.6f}'.format(stamp)
    print >> csv, stamp + ',' + str(throttle) + ',' + str(steering)

def listener(csv):
    rospy.init_node('record_commands')
    rospy.Subscriber('joy', Joy, callback, (csv,))
    rospy.spin()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        csvPath = sys.argv[1]
    else:
        csvPath = os.environ['usbDrive'] + '/' + 'commands.csv'
    with open(csvPath, 'w') as csv:
        listener(csv)

