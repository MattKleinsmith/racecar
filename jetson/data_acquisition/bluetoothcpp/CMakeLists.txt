cmake_minimum_required(VERSION 2.8.3)
project(bluetoothcpp)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS roscpp geometry_msgs)

include_directories(${catkin_INCLUDE_DIRS})

catkin_package(
  INCLUDE_DIRS
  CATKIN_DEPENDS roscpp geometry_msgs
  DEPENDS
)

###########
## Build ##
###########

add_executable(bluetoothNode src/serialTest.cpp)
target_link_libraries(bluetoothNode ${catkin_LIBRARIES})

#############
## Install ##
#############

## Mark executables and/or libraries for installation
install(TARGETS bluetoothNode
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
