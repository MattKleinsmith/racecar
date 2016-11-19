FROM ubuntu:14.04

SHELL ["/bin/bash", "-c"]

#######################
## Python and OpenCV ##
#######################

# ROS's opencv3 package has video support. Conda's and others' don't.
RUN echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > \
        /etc/apt/sources.list.d/ros-latest.list && \
    apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116

RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-indigo-ros-base

RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-indigo-opencv3

RUN rosdep init && \
     rosdep update

#########
## Pip ##
#########

RUN apt-get update && apt-get install -y --no-install-recommends \
  wget

RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python get-pip.py && \
	rm get-pip.py && \
	pip install --upgrade pip

############################
## Other Python libraries ##
############################

RUN pip install \
  h5py

#########
## GUI ##
#########

# http://wiki.ros.org/docker/Tutorials/GUI
# http://stackoverflow.com/questions/25281992/alternatives-to-ssh-x11-forwarding-for-docker-containers/25334301#25334301
# Add new sudo user
ENV USERNAME gui_user
RUN useradd -m $USERNAME && \
        echo "$USERNAME:$USERNAME" | chpasswd && \
        usermod --shell /bin/bash $USERNAME && \
        usermod -aG sudo $USERNAME && \
        echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
        chmod 0440 /etc/sudoers.d/$USERNAME && \
        # Replace 1000 with your user/group id
        usermod  --uid 1000 $USERNAME && \
        groupmod --gid 1000 $USERNAME
ENV QT_X11_NO_MITSHM 1

############
### Misc. ##
############

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY /scripts /scripts
WORKDIR /scripts
CMD bash -c "source /opt/ros/indigo/setup.bash && python play_video.py"
