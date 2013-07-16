# FSNView

This utility interprets a disk partition or whole disk with multiple DFXML-generating storage parsers, and compares the results.

Usage: `fsnview disk_image`

Currently this utility compares an XTAF storage system with multiple tools.


## Results

By default, a directory is created in the current working directory, named after the extensionless disk image name.  For example, the command `fsnview /bigstorage/DISKIMAGE.iso` creates the directory `./DISKIMAGE`.

In that output directory, most users will be interested in these files:

* `summary.html` - A summary of file system statistics, according to each parser run on the disk image.
* `diffs.html` - A pairwise comparison of the file system parsers' particular statistics (e.g. Parser 1 found N more deleted files than Parser 2).
