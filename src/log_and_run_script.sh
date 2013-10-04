#!/bin/bash

#This script does the following:
# * Creates as an output directory $3
# * Descends into the output directory
# * Executes $1 on $2, logging stdout and stderr to $3.{out,err}.log
# * Logs exit status of executing $1 to $3.status.log
# * Exits with the logged status

#Input
script="$1"
disk_image="$2"
outdir="$3"

#Output setup
mkdir -p "$outdir"
cd "$outdir"

#Execution and logging
"$script" "$disk_image" "$outdir" >"${outdir}.out.log" 2>"${outdir}.err.log"
rc=$?
echo $rc >"${outdir}.status.log"

exit $rc
