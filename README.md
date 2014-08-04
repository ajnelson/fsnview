# FSNView

This utility interprets a disk partition or whole disk with multiple DFXML-generating storage parsers, and compares the results.

Usage: `fsnview disk_image`

Currently this utility compares an XTAF storage system with multiple tools.


## Building and installing

See INSTALL.


## Process

FSNView runs these steps:

* Analyze - runs multiple parsers against a disk image, generating one DFXML file per tool
* Compare - Takes multiple DFXML files and produces differential DFXML files and aggregations
* Report - Reports the comparison results, producing an HTML report


## Results

By default, a directory is created in the current working directory, named after the extensionless disk image name.  For example, the command `fsnview /bigstorage/DISKIMAGE.iso` creates the directory `./DISKIMAGE`.  Its hierarchy is:

* `parts_mount/` - A directory for analyzing the disk image's partitions with `upartsfs`; used as a FUSE file system mount.
* `dfxml/analyze_with_fiwalk.sh`
* `dfxml/analyze_with_uxtaf.sh` - (XTAF only)
* `dfxml/analyze_with_py360.sh` - (XTAF only)
* `differences/` - Various comparisons of the DFXML
* `validation/` - Results of running `xmllint` on each tool's DFXML file
* `report.html` - Final report

The directories that end with ".sh" also record their respective scripts' standard out, standard error, exit status, and successful completion time in `{out,err,status,done}.log`.

In that output directory, most users will be interested in these files:

* `summary.html` - A summary of file system statistics, according to each parser run on the disk image.
* `diffs.html` - A pairwise comparison of the file system parsers' particular statistics (e.g. Parser 1 found N more deleted files than Parser 2).
