#!/bin/bash
# Install the Jetson Car support files
# This includes the code for the Arduino Car interface
# The packages needed for installing ROS on an Arduino
# Joystick support for the Nyko game controller
# This repository
# git clone https://github.com/jetsonhacks/installJetsonCar.git

# The original code was for the Jetson TK1, which is on Ubuntu 14.04.
# This code is for Jetson TX1, which is on Ubuntu 16.04.

# Run this script from the installJetsonCar folder.
cd ../..
repo=$PWD
jetsonhacks=$repo/jetsonhacks
installJetsonCar=$jetsonhacks/installJetsonCar
jetsoncar_teleop=$jetsonhacks/jetsoncar_teleop
racecarCatkin=~/catkin_workspaces/racecar
arduino=~/sketchbook/

# Make the jetsonbot catkin workspace
$installJetsonCar/setupCatkinWorkspace.sh $racecarCatkin
cd $racecarCatkin
sudo apt-get install arduino
sudo apt-get install ros-kinetic-joy -y
cd src
cp -r $jetsoncar_teleop jetsoncar_teleop
#git clone https://github.com/jetsonhacks/jetsoncar_teleop.git
cd ..
catkin_make

# Copy Arduino code 
cd $installJetsonCar
cp -r Arduino\ Firmware/* $arduino 
sudo apt-get install ros-kinetic-rosserial-arduino ros-kinetic-rosserial ros-kinetic-angles -y
cd ~/sketchbook/libraries
rm -rf ros_lib
source $racecarCatkin/devel/setup.bash
# The following raises an error about tf messages. This is unimportant for this
# application. The error is likely related to switching from indigo to kinetic.
rosrun rosserial_arduino make_libraries.py ~/sketchbook/libraries
cd $installJetsonCar
