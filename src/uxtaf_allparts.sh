#!/bin/bash

if [ $# -lt 1 ]; then
  echo Usage: $0 image_path
  exit 1
fi

#Allow environment-specified uxtaf path
if [ "x$UXTAF" == "x" ]; then
  UXTAF=uxtaf
fi

IMAGE=$1

rm -f uxtaf.info

#uxtaf's general construction of its XML:
#Generate head, creating uxtaf.dfxml.
#For each partition offset:
#	Run uxtaf dfxml, creating uxtaf_$offset.dfxml.
#	If dfxml succeeded, append uxtaf_$offset.dfxml to uxtaf.dfxml;
#	Else if failed, append comment with exit status to uxtaf.dfxml.
#Generate foot, appending to uxtaf.dfxml.
$UXTAF dfxml_head $IMAGE >uxtaf.dfxml 2>>uxtaf.err.log

for part_off in 524288 2148007936 4496818176 4713021440 4847239168 5115674624; do
  $UXTAF attach $IMAGE ${part_off} >uxtaf_${part_off}.out.log 2>uxtaf_${part_off}.err.log && \
    $UXTAF dfxml >uxtaf_${part_off}.dfxml 2>>uxtaf_${part_off}.err.log
  rc=$?
  echo $rc >uxtaf_${part_off}.status.log

  if [ $rc -eq 0 ]; then
    cat uxtaf_${part_off}.dfxml >>uxtaf.dfxml
  else
    echo "  <!-- Error: Unable to create process partition at ${part_off}.  uxtaf exited with status $rc.  See error log at uxtaf_${part_off}.err.log -->" >>uxtaf.dfxml
  fi
done
$UXTAF dfxml_foot >>uxtaf.dfxml 2>>uxtaf.err.log

rm -f uxtaf.info
