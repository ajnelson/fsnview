#!/bin/bash

set -e
set -x

if [ -r /etc/debian_version ]; then
  #Assume Ubuntu
  sudo apt-get install \
    afflib-tools \
    ewf-tools \
    libafflib-dev \
    libewf-dev
fi
#TODO
#    libexpat1-dev \
