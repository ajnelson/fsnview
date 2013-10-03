#!/bin/sh

set -e

if [ ! -r deps/dfxml/python/dfxml.py -o ! -r deps/sleuthkit/configure.ac -o ! -r deps/py360/report360.py ]; then
  git submodule init
  git submodule sync
  git submodule update
fi

aclocal
automake --add-missing
autoreconf -i
