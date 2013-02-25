#!/bin/bash

#This script runs the development gamut: Builds everything, runs unit tests, and installs to a test directory.

set -e

./bootstrap.sh
./configure --prefix=$PWD/build
make
make check
make distcheck
make install
