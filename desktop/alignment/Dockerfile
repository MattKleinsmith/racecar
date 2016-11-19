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

#############################
## Other Python libraries ##
#############################

#RUN pip install \
#  h5py

############
### Misc. ##
############
RUN apt-get update && apt-get install -y --no-install-recommends \
  wget

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# https://github.com/thewtex/jupyter-notebook-debian/blob/master/Dockerfile
# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
ENV TINI_VERSION v0.10.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
# RUN export uid=1000 gid=1000 && \
#     mkdir -p /home/developer && \
#     echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
#     echo "developer:x:${uid}:" >> /etc/group && \
#     echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
#     chmod 0440 /etc/sudoers.d/developer && \
#     chown ${uid}:${gid} -R /home/developer
# USER developer
# ENV HOME /home/developer
RUN mkdir /home/user
RUN groupadd -r user -g 777 && \
 useradd -u 431 -r -g user -d /home/user -s /sbin/nologin -c "Docker image user" user
RUN sudo rosdep init && \
     rosdep update && \
     echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
 
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py && rm get-pip.py
RUN pip install --upgrade \
  pip
RUN pip install \
  jupyter
RUN chown -R user:user /home/user
USER user


COPY /scripts /scripts
WORKDIR /scripts
CMD bash -c "source /opt/ros/indigo/setup.bash && python play_video.py"
#CMD /usr/bin/firefox
#CMD ["bash", "-c", "source /opt/ros/indigo/setup.bash && jupyter notebook --port=8888 --no-browser --ip=0.0.0.0"]
#CMD ["bash", "-c", "source /opt/ros/indigo/setup.bash && python play_video.py"]
#CMD ["bash", "-c", "source /opt/ros/indigo/setup.bash && jupyter notebook --ip='*' --no-browser --port=8008"]
