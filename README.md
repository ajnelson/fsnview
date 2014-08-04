# FSNView

This utility, "File System N-View," interprets a disk partition or whole disk with multiple DFXML-generating storage parsers, and compares the results.

Currently this utility compares an XTAF storage system with multiple tools, and can do much of the same analysis with pre-generated DFXML output.


## Building and installing

See INSTALL.


## Usage

`fsnview` takes as its first argument a command, `compare` or `xbox360`.  The same objectives are accomplished with either command:

* Compare - Takes multiple DFXML files and produces differential DFXML files and aggregations.
* Report - Reports the comparison results, producing an HTML report.  Tables are also produced in LaTeX.

The `xbox360` command will also handle running multiple storage system metadata parsers against a disk image, mounted with [UPartsFS](https://github.com/ajnelson/upartsfs), generating one DFXML file per tool.  The `compare` command assumes you have run the tools yourself and will provide the pre-computed DFXML.

At present the `xbox360` command has been more extensively tested than the `compare` command.


## Results

By default, results are created in the current working directory.  The results storage hierarchy is:

* `dfxml/` - The DFXML output from tools (produced with the `xbox360` command).
* `validation/` - Results of running `xmllint` on each tool's DFXML file.
* `report.html` - Final report

The directories that end with ".sh" also record their respective scripts' standard out, standard error, exit status, and successful completion time in `{out,err,status,done}.log`.

In the output directory, most users will also be interested in these files (which have corresponding `.tex` files for those of the LaTeX persuasion):

* `summary.html` - A summary of file system statistics, according to each parser run on the disk image.
* `diffs.html` - A pairwise comparison of the file system parsers' particular statistics (e.g. Parser 1 found N more deleted files than Parser 2, etc.).
