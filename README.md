# FSNView

This utility interprets a disk partition or whole disk with multiple DFXML-generating storage parsers, and compares the results.

Usage: `fsnview disk_image`

Results: By default, a directory is created in the current working directory, named after the extensionless disk image name.  For example, the command `fsnview /bigstorage/DISKIMAGE.iso` creates the directory `./DISKIMAGE`.

Currently this utility compares an XTAF storage system with multiple tools.
