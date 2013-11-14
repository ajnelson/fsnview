#!/bin/sh

python3 \
  make_diff_stats.py \
  -d \
  prog0:p0:../deps/dfxml/samples/difference_test_0.xml \
  prog1:p1:../deps/dfxml/samples/difference_test_1.xml
