#!/bin/sh

if [ -z "$prefix" ]; then
  prefix="$PWD/build"
fi

set -e

if [ ! -r deps/dfxml/python/dfxml.py -o \
  ! -r deps/sleuthkit/configure.ac -o \
  ! -r deps/py360/report360.py -o \
  ! -r deps/upartsfs/configure.ac \
]; then
  git submodule init
  git submodule sync
  git submodule update
fi

#In case Git doesn't recursively initialize submodules
if [ ! -r deps/py360/py360/Objects.py ]; then
  pushd deps/py360
  git submodule init
  git submodule sync
  git submodule update
  popd
fi

echo
echo
echo "Building and installing UPartsFS, assuming you're going to use the prefix '$prefix'."
echo "If that's an incorrect assumption, run:"
echo
echo "    prefix=\$your_prefix $0"
echo
echo "This workaround is due to a strange build dependency that may be gone soon."
echo
echo

pushd deps/upartsfs
./bootstrap.sh
./configure --disable-java --prefix="$prefix/share/fsnview/upartsfs"
make -j
make install
popd

aclocal
automake --add-missing
autoreconf -i
