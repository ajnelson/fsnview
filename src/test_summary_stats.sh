#!/bin/sh

python3 \
  make_summary_stats.py \
  -d \
  prog0:../deps/dfxml/samples/difference_test_0.xml \
  prog1:../deps/dfxml/samples/difference_test_1.xml
