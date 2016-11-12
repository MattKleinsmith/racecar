#!/usr/bin/env bash

# Run this script from ~/.../racecar/jetson/data-acquisition

# Run master node
tmux new -d -s core 'roscore'
sleep 1
# Run Arduino node
tmux new -d -s ino 'rosrun rosserial_python serial_node.py $usb'
# Run raw joy node and processed joy node
tmux new -d -s joy 'roslaunch jetsoncar_teleop nyko_teleop.launch'
# Start camera
tmux new -d -s cam './record_images.sh'
# Run a node to record the raw joy topic
tmux new -d -s cmd 'rosrun record_commands record_commands.py'

tmux ls

function stopRecording {
	echo
    tmux send -t cam '^C' ENTER
	tmux send -t cmd '^C' ENTER
    sleep 1 
    tmux ls
}

function listenForSIGINT {
    while true; do
        sleep 3600
    done
}

trap stopRecording SIGINT
listenForSIGINT &
wait $! # This waits for listenForSIGINT to finish
