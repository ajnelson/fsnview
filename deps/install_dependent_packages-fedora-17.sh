#!/bin/bash

set -e
set -x

if [ -r /etc/fedora-release ]; then
  #Assume Fedora
  sudo yum install \
    automake \
    gcc-c++ \
    git \
    libtool \
    openssl-devel \
    python3 \
    zlib-devel
fi
