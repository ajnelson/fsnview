#!/bin/bash

set -e
set -x

if [ -r /etc/debian_version ]; then
  #Assume Ubuntu
  sudo apt-get install \
    autoconf \
    automake \
    g++ \
    libtool \
    make
fi
#TODO
#    afflib-tools \
#    ewf-tools \
#    libafflib-dev \
#    libewf-dev \
#    libexpat1-dev \
#    libxml2-dev \
#    libxml2-utils \
#    python3 \
#    python-dev \
#    zlib1g-dev
