#!/bin/sh
# Create a Catkin Workspace and setup ROS environment variables
# Usage setupCatkinWorkspace.sh dirName
CATKIN_DIR="$~/catkin_workspaces/catkin_workspace_$(date +%s)"
CUSTOM_DIR="$1"
if [ ! -z "$CUSTOM_DIR" ]; then 
 CATKIN_DIR="$CUSTOM_DIR"
fi
if [ -e "$CATKIN_DIR" ] ; then
  echo "$CATKIN_DIR already exists; no action taken" 
  exit 1
else 
  echo "Creating Catkin Workspace: $CATKIN_DIR"
fi
echo "$CATKIN_DIR"/src
mkdir -p "$CATKIN_DIR"/src
cd "$CATKIN_DIR"/src
catkin_init_workspace
cd "$CATKIN_DIR"
catkin_make


#setup ROS environment variables
grep -q -F ' ROS_MASTER_URI' ~/.bashrc ||  echo 'export ROS_MASTER_URI=http://localhost:11311' | tee -a ~/.bashrc
grep -q -F ' ROS_IP' ~/.bashrc ||  echo "export ROS_IP=$(hostname -I)" | tee -a ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> ~/.bashrc


