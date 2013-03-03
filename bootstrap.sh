#!/bin/sh

set -e

if [ ! -r deps/py360/dfxml.py ]; then
  git submodule init deps/py360
  git submodule update deps/py360
  pushd deps/py360
  git submodule init
  git submodule update
  popd
fi

autoreconf -i
