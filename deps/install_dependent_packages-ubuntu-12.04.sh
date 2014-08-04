#!/bin/bash

set -e
set -x

if [ -r /etc/debian_version ]; then
  #Assume Ubuntu
  sudo apt-get install \
    autoconf \
    g++ \
    git \
    libssl-dev \
    libtool \
    make \
    python3 \
    python-crypto \
    python-fuse \
    zlib1g-dev
fi
#TODO
#    libexpat1-dev \
