#!/bin/bash

# Only run this script from the root directory of the git repo

# Install Arduino and ROS packages
# sudo apt-get update
sudo apt-get install -y \
                arduino \
                ros-kinetic-joy \
                ros-kinetic-rosserial-arduino \
                ros-kinetic-rosserial \
                ros-kinetic-angles

# Set directory variables:
repo=$PWD
jetsonhacks=$repo/jetsonhacks
installJetsonCar=$jetsonhacks/installJetsonCar
dataAcquisition=$repo/jetson/data_acquisition

# Make a catkin workspace for this project
racecarCatkin=~/catkin_workspaces/racecar
$installJetsonCar/setupCatkinWorkspace.sh $racecarCatkin
cd $racecarCatkin

# Install the bluetooth ROS package (custom)
bluetoothcpp=$dataAcquisition/bluetoothcpp
cp -r $bluetoothcpp src
bluetooth=$dataAcquisition/bluetooth
cp -r $bluetooth src

# Make the custom ROS packages
catkin_make

# Install Arduino sketch
localArduino=~/sketchbook/
jetsonCarSketch="$installJetsonCar/Arduino Firmware/jetsoncar"
cp -r "$jetsonCarSketch" $localArduino

# Install Arduino libraries
cd ~/sketchbook/libraries
rm -rf ros_lib
source $racecarCatkin/devel/setup.bash
rosrun rosserial_arduino make_libraries.py ~/sketchbook/libraries
# make_libraries.py raised an error about tf; I'm ignoring it for now

# Return to the repo
cd $repo

# Optional
# echo "source $racecarCatkin/devel/setup.bash" >> ~/.bashrc
# echo "alias workonRacecar=\"source $racecarCatkin/devel/setup.bash\"" >> ~/.bashrc
