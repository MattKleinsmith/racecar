FROM ubuntu:14.04

SHELL ["/bin/bash", "-c"]

#######################
## Python and OpenCV ##
#######################

RUN echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > \
        /etc/apt/sources.list.d/ros-latest.list && \
    apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116

RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-indigo-ros-base

RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-indigo-opencv3

RUN rosdep init && \
    rosdep update && \
    echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc

#############################
## Other Python libraries ##
#############################

#RUN pip install \
#  h5py

############
### Misc. ##
############

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY /scripts /scripts
WORKDIR /scripts
CMD bash
