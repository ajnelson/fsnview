#!/bin/bash

set -e
set -x

sudo port install \
  autoconf \
  automake \
  libtool \
  py27-crypto \
  py27-fuse \
  python27 \
  python32
