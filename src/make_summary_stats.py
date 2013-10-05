#!/usr/bin/env python3

__version__ = "0.1.0"

import argparse
import logging
import collections
import os

import fiwalk

logging.basicConfig()

class Summarizer(object):
    def __init__(self):
        self.log = logging.getLogger()
        self.stats_summary = collections.defaultdict(lambda: 0)
        self.stats_missed = collections.defaultdict(lambda: 0)
        self.stats_staging = collections.defaultdict(lambda: 0)
        self.volumes = set()

        #A flag set to False at the end of processing every file oject; set to True at the beginning, so non-failure has to be earned.
        self.failed = False

    def roll_stats(self, prog, targetdict):
        """Subroutine"""
        for key in self.stats_staging.keys():
            targetdict[key + "/" + prog] += self.stats_staging[key]

    def count_xml(self,prog,xmlfile):
        log.debug("count_xml(prog=%r, xmlfile=_)" % prog)
        try:
            fiwalk.fiwalk_using_sax(xmlfile=open(xmlfile, "rb"), callback=self.process_fi)
        except:
            pass
        log.debug("count_xml: self.failed=%r" % self.failed)
        #Accumulate staged stats into succeeded or failed pile;
        #TODO This might not be the best volume counting.
        log.debug("count_xml: self.stats_staging = %r" % self.stats_staging)
        if self.failed:
            self.roll_stats(prog, self.stats_missed)
            log.debug("count_xml: self.stats_missed=%r" % self.stats_missed)
            self.stats_missed["images/" + prog] += 1
            self.stats_missed["volumes/" + prog] += len(self.volumes)
        else:
            self.roll_stats(prog, self.stats_summary)
            log.debug("count_xml: self.stats_summary=%r" % self.stats_summary)
            self.stats_summary["images/" + prog] += 1
            self.stats_summary["volumes/" + prog] += len(self.volumes)
        #Reset staging state.
        self.stats_staging = collections.defaultdict(lambda: 0)
        self.volumes = set()
        self.failed = False

    def process_fi(self,fi):
        #This is set to False as the last action of process_fi
        self.failed = True

        volobj = None
        try:
            volobj = fi.volume
        except:
            pass
        if volobj:
            self.volumes.add(volobj)

        s_ftype = "dirs" if fi.is_dir() else "files"
        s_alloc = ("" if fi.allocated() else "un") + "allocated"
        self.stats_staging[s_alloc + "_" + s_ftype] += 1

        self.failed = False

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("xmldir", help="Directory containing output of fsnview")
    argparser.add_argument("-d", "--debug", help="Enable debug printing", action="store_true")
    opts = argparser.parse_args()

    log = logging.getLogger()
    log.setLevel(logging.DEBUG if opts.debug else logging.INFO)

    image_output_dir = os.path.abspath(os.path.expanduser(opts.xmldir))
    if not os.path.isdir(image_output_dir):
        logging.debug("image_output_dir = %r" % image_output_dir)
        raise Exception("Argument 'xmldir' is not a directory: %r." % opts.xmldir)

    out_latex = open(os.path.join(image_output_dir, "differences/summary.tex"), "w")
    out_html = open(os.path.join(image_output_dir, "differences/summary.html"), "w")

    summarizer = Summarizer()
    for prog in ["fiwalk","uxtaf","py360"]:
        xml_relpath = image_output_dir + "/dfxml/analyze_with_" + prog + ".sh/" + prog + ".dfxml"
        summarizer.count_xml(prog, xml_relpath)

    log.debug("summarizer.stats_summary = %r" % summarizer.stats_summary)
    log.debug("summarizer.stats_missed = %r" % summarizer.stats_missed)
    log.debug("summarizer.stats_staging = %r" % summarizer.stats_staging)

    stats_dict = collections.defaultdict(lambda: "0")
    # sorf: Success or Failure
    for (sorf, defdict) in [("s", summarizer.stats_summary), ("f", summarizer.stats_missed)]:
        for key in defdict.keys():
            stats_dict[sorf + "/" + key] = defdict[key]
#% Partitions failed & & & \\ % uxtaf is the only one that will count failed partitions; py360 and fiwalk will lose the whole disk of information on an XML-creating failure.
    template_latex = r"""\
\begin{table}[htdp]
\caption{Summary processing statistics for three DFXML-producing XTAF analyzers.  ``Incomplete'' statistics are counts from utilities that failed partway through processing a disk image.}
\begin{center}
\begin{tabular}{|l|r|r|r|}
\hline
& \fiwalk & \uxtaf & \pythreesixty \\
\hline
Images processed & %(s/images/fiwalk)s & %(s/images/uxtaf)s & %(s/images/py360)s \\
Partitions processed & %(s/volumes/fiwalk)s & %(s/volumes/uxtaf)s & %(s/volumes/py360)s \\
\hline
Allocated directories & %(s/allocated_dirs/fiwalk)s & %(s/allocated_dirs/uxtaf)s & %(s/allocated_dirs/py360)s \\
Allocated files & %(s/allocated_files/fiwalk)s & %(s/allocated_files/uxtaf)s & %(s/allocated_files/py360)s \\
Unallocated directories & %(s/unallocated_dirs/fiwalk)s & %(s/unallocated_dirs/uxtaf)s & %(s/unallocated_dirs/py360)s \\
Unallocated files & %(s/unallocated_files/fiwalk)s & %(s/unallocated_files/uxtaf)s & %(s/unallocated_files/py360)s \\
\hline
Incomplete data: & & & \\
~~Allocated directories & %(f/allocated_dirs/fiwalk)s & %(f/allocated_dirs/uxtaf)s & %(f/allocated_dirs/py360)s \\
~~Allocated files & %(f/allocated_files/fiwalk)s & %(f/allocated_files/uxtaf)s & %(f/allocated_files/py360)s \\
~~Unallocated directories & %(f/unallocated_dirs/fiwalk)s & %(f/unallocated_dirs/uxtaf)s & %(f/unallocated_dirs/py360)s \\
~~Unallocated files & %(f/unallocated_files/fiwalk)s & %(f/unallocated_files/uxtaf)s & %(f/unallocated_files/py360)s \\
\hline
\end{tabular}
\end{center}
\label{default}
\end{table}
""" 
    out_latex.write(template_latex % stats_dict)

    template_html = """\
<!doctype html>
<html>
<head>
<style type="text/css">
caption {text-align: left;}
th {text-align: left;}
thead th {border-bottom: 1px solid black;}
tbody th {text-indent: 2em; padding-right: 1em;}
th.breakout {text-indent: 4em;}
</style>
</head>

<body>
<table>
  <caption>Summary processing statistics for three DFXML-producing XTAF analyzers.  "Incomplete" statistics are counts from utilities that failed partway through processing a disk image.</caption>
  <thead>
    <tr>
      <th />
      <th>Fiwalk</th>
      <th>Uxtaf</th>
      <th>Py360</th>
    </tr>
  </thead>
  <tfoot></tfoot>
  <tbody>
<tr><th>Images processed</td><td>%(s/images/fiwalk)s</td><td>%(s/images/uxtaf)s</td><td>%(s/images/py360)s</td></tr>
<tr><th>Partitions processed</td><td>%(s/volumes/fiwalk)s</td><td>%(s/volumes/uxtaf)s</td><td>%(s/volumes/py360)s</td></tr>
<tr><th>Allocated directories</td><td>%(s/allocated_dirs/fiwalk)s</td><td>%(s/allocated_dirs/uxtaf)s</td><td>%(s/allocated_dirs/py360)s</td></tr>
<tr><th>Allocated files</td><td>%(s/allocated_files/fiwalk)s</td><td>%(s/allocated_files/uxtaf)s</td><td>%(s/allocated_files/py360)s</td></tr>
<tr><th>Unallocated directories</td><td>%(s/unallocated_dirs/fiwalk)s</td><td>%(s/unallocated_dirs/uxtaf)s</td><td>%(s/unallocated_dirs/py360)s</td></tr>
<tr><th>Unallocated files</td><td>%(s/unallocated_files/fiwalk)s</td><td>%(s/unallocated_files/uxtaf)s</td><td>%(s/unallocated_files/py360)s</td></tr>
<tr><th colspan="4">Incomplete data:</th></tr>
<tr><th class="breakout">Allocated directories</td><td>%(f/allocated_dirs/fiwalk)s</td><td>%(f/allocated_dirs/uxtaf)s</td><td>%(f/allocated_dirs/py360)s</td></tr>
<tr><th class="breakout">Allocated files</td><td>%(f/allocated_files/fiwalk)s</td><td>%(f/allocated_files/uxtaf)s</td><td>%(f/allocated_files/py360)s</td></tr>
<tr><th class="breakout">Unallocated directories</td><td>%(f/unallocated_dirs/fiwalk)s</td><td>%(f/unallocated_dirs/uxtaf)s</td><td>%(f/unallocated_dirs/py360)s</td></tr>
<tr><th class="breakout">Unallocated files</td><td>%(f/unallocated_files/fiwalk)s</td><td>%(f/unallocated_files/uxtaf)s</td><td>%(f/unallocated_files/py360)s</td></tr>
  </tbody>
</table>
</body>
</html>
""" 
    out_html.write(template_html % stats_dict)
