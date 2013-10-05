#!/usr/bin/env python3

__version__ = "0.1.0"

import argparse
import logging
import collections
import os
import sys

import idifference

logging.basicConfig()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("xmldir", help="Directory containing output of fsnview")
    argparser.add_argument("-d", "--debug", help="Enable debug printing", action="store_true")
    opts = argparser.parse_args()

    log = logging.getLogger()
    log.setLevel(logging.DEBUG if opts.debug else logging.INFO)

    image_output_dir = os.path.abspath(os.path.expanduser(opts.xmldir))

    os.makedirs(os.path.join(image_output_dir, "differences"))
    out_latex = open(os.path.join(image_output_dir, "differences/diffs.tex"), "w")
    out_html = open(os.path.join(image_output_dir, "differences/diffs.html"), "w")

    diff_stats = collections.defaultdict(lambda: 0)

    #DFXML paths
    dps = dict()
    dps["fiwalk"] = image_output_dir + "/dfxml/analyze_with_fiwalk.sh/fiwalk.dfxml"
    dps["py360"]  = image_output_dir + "/dfxml/analyze_with_py360.sh/py360.dfxml"
    dps["uxtaf"]  = image_output_dir + "/dfxml/analyze_with_uxtaf.sh/uxtaf.dfxml"

    pairs = [
      ("fiwalk","uxtaf"),
      ("uxtaf","fiwalk"),
      ("uxtaf","py360"),
      ("py360","uxtaf"),
      ("fiwalk","py360"),
      ("py360","fiwalk"),
    ]

    if os.path.isdir(image_output_dir):
        for (prog1,prog2) in pairs:
            xml1_relpath = dps[prog1]
            xml2_relpath = dps[prog2]

            if not os.path.exists(xml1_relpath):
                continue
            if not os.path.exists(xml2_relpath):
                continue

            tempstate = idifference.DiskState()
            log.info("Starting DiskState with %r." % xml1_relpath)
            #TODO This is a hack to assure log order - would be marginally better to call flush on the log file descriptor, if that's accessible
            sys.stderr.flush()
            sys.stdout.flush()
            tempstate.process(xml1_relpath)
            sys.stderr.flush()
            sys.stdout.flush()
            log.info("Getting differences of DiskState against %r." % xml2_relpath)
            sys.stderr.flush()
            sys.stdout.flush()
            tempstate.next()
            tempstate.process(xml2_relpath)
            sys.stderr.flush()
            sys.stdout.flush()
            #tempstate.report()
            #sys.stderr.flush()
            #sys.stdout.flush()

            #Accumulate stats from DiskState
            difftag = "/" + prog1[0] + prog2[0]
            log.debug("difftag = %r" % difftag)
            log.debug("  Pre:  diffstats['added%s']   = %r" % (difftag, diff_stats["added" + difftag]))
            diff_stats["added" + difftag]   += len(tempstate.new_files)
            log.debug("  Post: diffstats['added%s']   = %r" % (difftag, diff_stats["added" + difftag]))
            log.debug("  Pre:  diffstats['missed%s']  = %r" % (difftag, diff_stats["missed" + difftag]))
            diff_stats["missed" + difftag]  += len(tempstate.fnames)
            log.debug("  Post: diffstats['missed%s']  = %r" % (difftag, diff_stats["missed" + difftag]))
            log.debug("  Pre:  diffstats['renamed%s'] = %r" % (difftag, diff_stats["renamed" + difftag]))
            diff_stats["renamed" + difftag] += len(tempstate.renamed_files)
            log.debug("  Post: diffstats['renamed%s'] = %r" % (difftag, diff_stats["renamed" + difftag]))
 
            diff_stats["dsha1" + difftag]     += tempstate.changed_dir_sha1_tally
            diff_stats["fsha1" + difftag]     += tempstate.changed_file_sha1_tally
            diff_stats["filesize" + difftag] += tempstate.changed_filesize_tally
            diff_stats["mtime" + difftag]    += tempstate.changed_mtime_tally
            diff_stats["atime" + difftag]    += tempstate.changed_atime_tally
            diff_stats["ctime" + difftag]    += tempstate.changed_ctime_tally
            diff_stats["crtime" + difftag]   += tempstate.changed_crtime_tally
            diff_stats["fbr" + difftag] = tempstate.changed_first_byterun_tally

    diff_stats["num_images"] = 1
    diff_stats_pretty = collections.defaultdict(lambda: "0")
    for key in diff_stats:
        log.debug("Pretty-print converting: %r -> %r", key, diff_stats[key])
        diff_stats_pretty[key] = str(diff_stats[key])
    diff_stats_pretty["num_images_plural"] = "s" if diff_stats["num_images"] > 1 else ""

    log.debug("Pretty-printable diff stats: %r" % diff_stats_pretty)
    template_latex = r"""\
\begin{table*}[htdp]
\caption{Counts of file system parsing discrepancies between three Xbox 360 analysis utilities, \fiwalk (Fi), \uxtaf (Ux) and \pythreesixty (Py).  Counts are in differences from the first program's DFXML output to the second program, \eg ``Missed files'' indicates the number of files the first program found that the second didn't.  ``Files'' includes directories.  These statistics are from %(num_images)s disk image%(num_images_plural)s.}
\begin{center}
\begin{tabular}{|l|l|l|l|l|l|l|}
\hline
Differences in... & Fi-Ux & Ux-Fi & Ux-Py & Py-Ux & Fi-Py & Py-Fi \\
\hline
Additional files & %(added/fu)s & %(added/uf)s & %(added/up)s & %(added/pu)s & %(added/fp)s & %(added/pf)s \\
Missed files & %(missed/fu)s & %(missed/uf)s & %(missed/up)s & %(missed/pu)s & %(missed/fp)s & %(missed/pf)s \\
Renamed files & %(renamed/fu)s & %(renamed/uf)s & %(renamed/up)s & %(renamed/pu)s & %(renamed/fp)s & %(renamed/pf)s \\
Metadata: & & & & & & \\
~~SHA-1 (dirs) & %(dsha1/fu)s & %(dsha1/uf)s & %(dsha1/up)s & %(dsha1/pu)s & %(dsha1/fp)s & %(dsha1/pf)s \\
~~SHA-1 (files) & %(fsha1/fu)s & %(fsha1/uf)s & %(fsha1/up)s & %(fsha1/pu)s & %(fsha1/fp)s & %(fsha1/pf)s \\
~~File size & %(filesize/fu)s & %(filesize/uf)s & %(filesize/up)s & %(filesize/pu)s & %(filesize/fp)s & %(filesize/pf)s \\
~~Modified time & %(mtime/fu)s & %(mtime/uf)s & %(mtime/up)s & %(mtime/pu)s & %(mtime/fp)s & %(mtime/pf)s \\
~~Access time & %(atime/fu)s & %(atime/uf)s & %(atime/up)s & %(atime/pu)s & %(atime/fp)s & %(atime/pf)s \\
~~Change time & %(ctime/fu)s & %(ctime/uf)s & %(ctime/up)s & %(ctime/pu)s & %(ctime/fp)s & %(ctime/pf)s \\
~~Creation time & %(crtime/fu)s & %(crtime/uf)s & %(crtime/up)s & %(crtime/pu)s & %(crtime/fp)s & %(crtime/pf)s \\
~~Data start offset & %(fbr/fu)s & %(fbr/uf)s & %(fbr/up)s & %(fbr/pu)s & %(fbr/fp)s & %(fbr/pf)s \\
\hline
\end{tabular}
\end{center}
\label{default}
\end{table*}
"""
    template_html = """\
<!DOCTYPE html>
<html>
<head>
<style type="text/css">
caption {text-align: left;}
th {text-align: left;}
thead th {border-bottom:1px solid black;}
tbody th {text-indent: 2em; padding-right: 1em;}
th.breakout {text-indent: 4em;}
</style>
</head>

<body>

<table>
  <caption style='text-align:left;'>Counts of file system parsing discrepancies between three Xbox 360 analysis utilities, <em>Fiwalk</em> (Fi), <em>uxtaf</em> (Ux) and <em>Py360</em> (Py).  Counts are in differences from the first program's DFXML output to the second program, <em>e.g.</em> "Missed files" indicates the number of files the first program found that the second didn't.  "Files" includes directories.  These statistics are from %(num_images)s disk image%(num_images_plural)s.</caption>
  <thead>
    <tr>
      <th>Differences in...</th>
      <th>Fi-Ux</th>
      <th>Ux-Fi</th>
      <th>Ux-Py</th>
      <th>Py-Ux</th>
      <th>Fi-Py</th>
      <th>Py-Fi</th>
    </tr>
  </thead>
  <tfoot></tfoot>
  <tbody>
    <tr>
      <th>Additional files</th>
      <td>%(added/fu)s</td>
<td>%(added/uf)s</td>
<td>%(added/up)s</td>
<td>%(added/pu)s</td>
<td>%(added/fp)s</td>
<td>%(added/pf)s</td>
    </tr>
    <tr>
      <th>Missed files</th>
      <td>%(missed/fu)s</td>
      <td>%(missed/uf)s</td>
      <td>%(missed/up)s</td>
      <td>%(missed/pu)s</td>
      <td>%(missed/fp)s</td>
      <td>%(missed/pf)s</td>
    </tr>
    <tr>
      <th>Renamed files</th>
<td>%(renamed/fu)s</td>
<td>%(renamed/uf)s</td>
<td>%(renamed/up)s</td>
<td>%(renamed/pu)s</td>
<td>%(renamed/fp)s</td>
<td>%(renamed/pf)s</td>
    </tr>
    <tr>
      <th colspan="7">Metadata:</th>
    </tr>
    <tr>
<th class="breakout">SHA-1 (dirs)</th><td>%(dsha1/fu)s</td><td>%(dsha1/uf)s</td><td>%(dsha1/up)s</td><td>%(dsha1/pu)s</td><td>%(dsha1/fp)s</td><td>%(dsha1/pf)s</td>
    </tr>
    <tr>
<th class="breakout">SHA-1 (files)</th><td>%(fsha1/fu)s</td><td>%(fsha1/uf)s</td><td>%(fsha1/up)s</td><td>%(fsha1/pu)s</td><td>%(fsha1/fp)s</td><td>%(fsha1/pf)s</td>
    </tr>
    <tr>
<th class="breakout">File size</th><td>%(filesize/fu)s</td><td>%(filesize/uf)s</td><td>%(filesize/up)s</td><td>%(filesize/pu)s</td><td>%(filesize/fp)s</td><td>%(filesize/pf)s</td>
    </tr>
    <tr>
<th class="breakout">Modified time</th><td>%(mtime/fu)s</td><td>%(mtime/uf)s</td><td>%(mtime/up)s</td><td>%(mtime/pu)s</td><td>%(mtime/fp)s</td><td>%(mtime/pf)s</td>
    </tr>
    <tr>
<th class="breakout">Access time</th><td>%(atime/fu)s</td><td>%(atime/uf)s</td><td>%(atime/up)s</td><td>%(atime/pu)s</td><td>%(atime/fp)s</td><td>%(atime/pf)s</td>
    </tr>
    <tr>
<th class="breakout">Change time</th><td>%(ctime/fu)s</td><td>%(ctime/uf)s</td><td>%(ctime/up)s</td><td>%(ctime/pu)s</td><td>%(ctime/fp)s</td><td>%(ctime/pf)s</td>
    </tr>
    <tr>
<th class="breakout">Creation time</th><td>%(crtime/fu)s</td><td>%(crtime/uf)s</td><td>%(crtime/up)s</td><td>%(crtime/pu)s</td><td>%(crtime/fp)s</td><td>%(crtime/pf)s</td>
    </tr>
    <tr>
<th class="breakout">Data start offset</th><td>%(fbr/fu)s</td><td>%(fbr/uf)s</td><td>%(fbr/up)s</td><td>%(fbr/pu)s</td><td>%(fbr/fp)s</td><td>%(fbr/pf)s</td>
    </tr>
  </tbody>
</table>

</body>
</html>
"""

    out_latex.write(template_latex % diff_stats_pretty)
    out_html.write(template_html % diff_stats_pretty)
#TODO Times & %(times/fu)s & %(times/uf)s & %(times/up)s & %(times/pu)s & %(times/fp)s & %(times/pf)s \\
#TODO File size & & & & & & \\
#TODO Directory size & & & & & & \\
#TODO Byte run coverage & & & & & & \\
#TODO Checksum & & & & & & \\
#TODO File name & & & & & & \\
#TODO Directory entry count & & & & & & \\
