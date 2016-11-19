FROM ubuntu:14.04

SHELL ["/bin/bash", "-c"]

###############
## Miniconda ##
###############

# https://hub.docker.com/r/continuumio/miniconda/~/dockerfile/
RUN apt-get update && apt-get install -y --no-install-recommends \
  wget \
  ca-certificates

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget https://repo.continuum.io/miniconda/Miniconda2-4.1.11-Linux-x86_64.sh -O miniconda.sh && \
    /bin/bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH /opt/conda/bin:$PATH
RUN conda update -y \
  setuptools
RUN pip install --upgrade \
  pip

############
## OpenCV ##
############

# http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
RUN apt-get update && apt-get install -y --no-install-recommends \
  gfortran \
  libatlas-base-dev \
  libavcodec-dev \
  libavformat-dev \
  libgtk2.0-dev \
  libjasper-dev \
  libjpeg8-dev \
  libpng12-dev \
  libswscale-dev \
  libtiff4-dev \
  libv4l-dev \
  software-properties-common

RUN add-apt-repository -y \
  ppa:mc3man/trusty-media

RUN apt-get update && apt-get install -y --no-install-recommends \
  ffmpeg

# https://anaconda.org/menpo/opencv3
RUN conda install -y -c \
  menpo opencv3=3.1.0

#############################
## Other Python libraries ##
#############################

RUN pip install \
  h5py

############
### Misc. ##
############

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY /scripts /scripts
WORKDIR /scripts
CMD bash
