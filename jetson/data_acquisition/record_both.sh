#!/usr/bin/env bash

# Run this script from ~/.../racecar/jetson/data-acquisition

./setupRFCOMMport.sh
# Run master node
tmux new -d -s core 'roscore'
sleep 1
# Start camera
tmux new -d -s cam './record_images.sh'
# Run command regulator node
tmux new -d -s relay 'rosrun bluetoothcpp bluetoothNode'
# Run Arduino node
tmux new -d -s ino 'rosrun rosserial_python serial_node.py $usb'

tmux ls

function stopRecording {
	echo "\nStopping camera"
    tmux send -t cam '^C' ENTER
    sleep 1 
    tmux ls
}

trap stopRecording SIGINT

rosrun bluetooth bluetooth.py
