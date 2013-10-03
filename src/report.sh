#!/bin/bash

usage="Usage: $0 fsnview_output_directory\n"

get_abspath() {
  $PYTHON3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$1"
}

outdir="$1"

if [ ! -d "$outdir" ]; then
  echo "Error: report.sh: Directory requested for analysis is not a directory: '$outdir'." >&2
  exit 1
fi

pushd "$outdir" >/dev/null

# Output file summary
echo ""
echo "Results"
echo "======="
echo ""
echo "Results directory:"
echo ""
echo "$outdir"
echo ""
echo ""
echo "Exit statuses of all the DFXML-generating programs (should be 0's):"
echo ""
grep '^' {fiwalk,py360,uxtaf}*.status.log | cat
echo ""
echo ""
echo "Review these files for between-tool differences:"
echo ""
ls diffs*.txt
echo ""
echo ""
echo "Review these files for file system timelines according to each tool:"
echo ""
ls mactimeline*.txt
echo ""
echo ""
echo "Review these files for tabulated results:"
echo ""
ls {diffs,summary}.{tex,html}
echo ""
echo ""

popd >/dev/null