#!/bin/sh

set -e

if [ ! -r deps/dfxml/python/dfxml.py ]; then
  git submodule init
  git submodule sync
  git submodule update
fi

autoreconf -i
