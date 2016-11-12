#!/bin/bash

# Run this script from ~/.../racecar/jetson/data-acquisition

# Run master node
roscore &
# Run Arduino node
rosrun rosserial_python serial_node.py $usb &
# Run raw joy node and processed joy node
roslaunch jetsoncar_teleop nyko_teleop.launch &
# Start camera
./record_images.sh &
record_images_PID=$!
# Run a node to record the raw joy topic
rosrun record_commands record_commands.py &
record_commands_PID=$!

function stop_recording {
    kill -SIGINT record_images_PID
    kill -SIGINT record_commands_PID
}

trap stop_recording SIGINT
