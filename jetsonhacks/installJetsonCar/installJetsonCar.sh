#!/bin/sh
# Install the Jetson Car support files
# This includes the code for the Arduino Car interface
# The packages needed for installing ROS on an Arduino
# Joystick support for the Nyko game controller
# This repository
# git clone https://github.com/jetsonhacks/installJetsonCar.git

# The original code was for the Jetson TK1, which is on Ubuntu 14.04.
# This code is for Jetson TX1, which is on Ubuntu 16.04.

cd ../..
repo=$PWD
arduino=$repo/arduino
jetsonhacks=$repo/jetsonhacks

# Make the jetsonbot catkin workspace
./setupCatkinWorkspace.sh jetsoncar
cd $jetsonhacks/jetsoncar
sudo apt-get install arduino
sudo apt-get install ros-kinetic-joy -y
cd src
cp -r $jetsonhacks/jetsoncar_teleop jetsoncar_teleop
#git clone https://github.com/jetsonhacks/jetsoncar_teleop.git
cd ..
catkin_make

# Copy Arduino code 
cd $jetsonhacks/installJetsonCar
cp -r Arduino\ Firmware/* $arduino 
sudo apt-get install ros-kinetic-rosserial-arduino ros-kinetic-rosserial ros-kinetic-angles -y
cd ~/sketchbook/libraries
rm -rf ros_lib
source $jetsonhacks/jetsoncar/devel/setup.bash
# The following raises an error about tf messages. This is unimportant for this
# application. The error is likely related to switching from indigo to kinetic.
rosrun rosserial_arduino make_libraries.py ~/sketchbook/libraries
cd $origWD

