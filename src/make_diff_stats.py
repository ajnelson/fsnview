#!/usr/bin/env python3

__version__ = "0.2.3"

import argparse
import logging
import collections
import os
import sys

import Objects
import make_differential_dfxml

_logger = logging.getLogger(os.path.basename(__file__))

class Differ(object):
    def __init__(self, pre_path, post_path):
        self._pre_path = pre_path
        self._post_path = post_path
        self._dfxml_object = None
        self._volume_diffs = None
        self._file_diffs = None

    def __repr__(self):
        return "Differ(%r, %r)" % (self._pre_path, self._post_path)

    def count_property_diffs(self):
        counter = collections.defaultdict(lambda: 0)
        d = self.dfxml_object
        return counter

    def write_differential_dfxml(self, output_path):
        d = self.dfxml_object
        with open(output_path, "w") as output_fh:
            output_fh.write("""<?xml version="1.0"?>\n""")
            print(d.to_dfxml(), file=output_fh)

    @property
    def file_diffs(self):
        """Populates on first access.  There is intentionally no setter."""
        if self._file_diffs is None:
            c = collections.defaultdict(lambda: 0)
            d = self.dfxml_object
            for o in d:
                if not isinstance(o, Objects.FileObject):
                    continue
                for diff in o.diffs:
                    c[diff] += 1
                    #Break out some stats further by file and directory
                    if diff in ["filesize", "sha1"]:
                        if o.name_type in ["d", "r"]:
                            simplified_name_type = o.name_type
                        else:
                            simplified_name_type = "other"
                        c[diff + "/" + simplified_name_type] += 1
            self._file_diffs = c
        return self._file_diffs

    @property
    def dfxml_object(self):
        """Populates on first access.  There is intentionally no setter."""
        if self._dfxml_object is None:
            self._dfxml_object = make_differential_dfxml.make_differential_dfxml(self._pre_path, self._post_path)
        return self._dfxml_object

    @property
    def volume_diffs(self):
        """Populates on first access.  There is intentionally no setter."""
        if self._volume_diffs is None:
            c = collections.defaultdict(lambda: 0)
            d = self.dfxml_object
            for v in d.all_volumes():
                for diff in o.diffs:
                    c[diff] += 1
            self._volume_diffs = c
        return self._volume_diffs

class DifferTabulator(object):

    #The OrderedDict here lets insertion order determine the metadata breakout order in the generated tables.
    _diff_annos = collections.OrderedDict()

    def __init__(self):
        #Key: Pairs of paths to DFXML files
        self._differs = dict()

        #Key: Path to DFXML file
        #Value: Pair, (long label, short label)
        self._annos = dict()

        self._format_dict = None
        self._stats_dict = None

        #The entries containing '/' are broken out in the Differ class.
        self._diff_annos["sha1/d"] = "SHA-1 (dirs)"
        self._diff_annos["sha1/r"] = "SHA-1 (files)"
        self._diff_annos["sha1/other"] = "SHA-1 (other)"
        self._diff_annos["filesize/d"] = "Filesize (dirs)"
        self._diff_annos["filesize/r"] = "Filesize (files)"
        self._diff_annos["filesize/other"] = "Filesize (other)"
        self._diff_annos["mtime"] = "Modified time"
        self._diff_annos["atime"] = "Access time"
        self._diff_annos["ctime"] = "Metadata change time"
        self._diff_annos["crtime"] = "Creation time"
        self._diff_annos["datastart"] = "Data start offset"

    def _get_format_dict(self):
        if self._format_dict:
            return self._format_dict

        f = collections.defaultdict(lambda: str())
        f["tool_count"] = len(self._annos)
        f["html_colspan"] = len(self._differs) + 1
        f["latex_column_aligns"] = "|".join(["r"]*len(self._differs))
        f["metadata_row_span"] = "& " * len(self._differs)

        for (i, (long_label, short_label)) in enumerate(sorted(self._annos.values())):
            if i+1 == len(self._annos):
                f["html_tool_preamble_listing"] += ", and <em>" + long_label + "</em> (\"" + short_label + "\")"
                f["latex_tool_preamble_listing"] += ", and \\emph{" + long_label + "} (``" + short_label + "'')"
            else:
                f["html_tool_preamble_listing"] += ", <em>" + long_label + "</em> (\"" + short_label + "\")"
                f["latex_tool_preamble_listing"] += ", \\emph{" + long_label + "} (``" + short_label + "'')"

        #TODO There'll probably need to be another way to sort these later...
        for (pre_path, post_path) in sorted(self._differs.keys()):
            pre_short_label = self._annos[pre_path][1]
            post_short_label = self._annos[post_path][1]

            f["html_tool_column_headers"] += "<th>%s-%s</th>" % (pre_short_label, post_short_label)
            f["html_row_added_files"] += "<td>%(added_files/" + pre_short_label + "/" + post_short_label + ")s</td>"
            f["html_row_missed_files"] += "<td>%(missed_files/" + pre_short_label + "/" + post_short_label + ")s</td>"
            f["html_row_renamed_files"] += "<td>%(renamed_files/" + pre_short_label + "/" + post_short_label + ")s</td>"

            f["latex_tool_column_headers"] += "%s-%s & " % (pre_short_label, post_short_label)
            f["latex_row_added_files"] += "%(added_files/" + pre_short_label + "/" + post_short_label + ")s & "
            f["latex_row_missed_files"] += "%(missed_files/" + pre_short_label + "/" + post_short_label + ")s & "
            f["latex_row_renamed_files"] += "%(renamed_files/" + pre_short_label + "/" + post_short_label + ")s & "

        for diff_breakout in DifferTabulator._diff_annos:
            pre_short_label = self._annos[pre_path][1]
            post_short_label = self._annos[post_path][1]

            html_metadata_row = "<tr>"
            latex_metadata_row = ""
            html_metadata_row += "<th>" + DifferTabulator._diff_annos[diff_breakout] + "</th>"
            latex_metadata_row += "~~" + DifferTabulator._diff_annos[diff_breakout]
            for (pre_path, post_path) in sorted(self._differs.keys()):
                html_metadata_row += "<td>%(" + "_".join([diff_breakout, pre_short_label, post_short_label]) + ")s</td>"
                latex_metadata_row += " & %(" + "_".join([diff_breakout, pre_short_label, post_short_label]) + ")s "
            html_metadata_row += "</tr>\n"
            latex_metadata_row += "\\\\\n"
            f["html_rows_metadata_breakouts"] += html_metadata_row
            f["latex_rows_metadata_breakouts"] += latex_metadata_row

        self._format_dict = f
        #_logger.debug("self._format_dict = %r" % f)
        return self._format_dict

    def _get_stats_dict(self):
        if self._stats_dict:
            return self._stats_dict

        s = collections.defaultdict(lambda: ".")

        for (pre_path, post_path) in self._differs.keys():
            pre_short_label = self._annos[pre_path][1]
            post_short_label = self._annos[post_path][1]
            differ = self._differs[(pre_path, post_path)]
            for diff_breakout in differ.file_diffs:
                s["%s_%s_%s" % (diff_breakout, pre_short_label, post_short_label)] = str(differ.file_diffs[diff_breakout])

        #Write metadata breakout rows (takes two loops)
        self._stats_dict = s
        #_logger.debug("self._stats_dict = %r" % s)
        return self._stats_dict

    def add(self, long_label, short_label, path):
        self._annos[path] = (long_label, short_label)
        for x in self._annos:
            for y in self._annos:
                if x == y:
                    continue
                if (x, y) not in self._differs:
                    self._differs[(x, y)] = Differ(x, y)
        #_logger.debug("self._annos = %r" % self._annos)
        #_logger.debug("self._differs = %r" % self._differs)

    def write_html(self, fp):
        with open(fp, "w") as fh:
            template0 = """\
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
      <caption>Counts of file system parsing discrepancies between %(tool_count)s storage parsers%(html_tool_preamble_listing)s.  Counts are in differences from the first program's DFXML output to the second program, <em>e.g.</em> "Missed files" indicates the number of files the first program found that the second didn't.  "Files" includes directories.</caption>
      <thead>
        <tr>
          <th>Differences in...</th>
          %(html_tool_column_headers)s
        </tr>
      </thead>
      <tfoot></tfoot>
      <tbody>
        <tr>
          <th>Additional files</th>
          %(html_row_added_files)s
        </tr>
        <tr>
          <th>Missed files</th>
          %(html_row_missed_files)s
        </tr>
        <tr>
          <th>Renamed files</th>
          %(html_row_renamed_files)s
        </tr>
        <tr>
          <th colspan="%(html_colspan)d">Metadata:</th>
        </tr>
        %(html_rows_metadata_breakouts)s
      </tbody>
    </table>
  </body>
</html>
"""

            format_dict = self._get_format_dict()
            stats_dict = self._get_stats_dict()
            template1 = template0 % format_dict
            formatted = template1 % stats_dict
            fh.write(formatted)

    def write_latex(self, fp):
        with open(fp, "w") as fh:
            template0 = r"""\begin{table*}[htdp]
\caption{Counts of file system parsing discrepancies between %(tool_count)s storage parsers%(latex_tool_preamble_listings)s.  Counts are in differences from the first program's DFXML output to the second program, \eg ``Missed files'' indicates the number of files the first program found that the second didn't.  ``Files'' includes directories.}
\begin{center}
\begin{tabular}{|l|%(latex_column_aligns)s|}
\hline
Differences in... %(latex_tool_column_headers)s \\
\hline
Additional files %(latex_row_added_files)s \\
Missed files %(latex_row_missed_files)s \\
Renamed files %(latex_row_renamed_files)s \\
Metadata: %(metadata_row_span)s \\
%(latex_rows_metadata_breakouts)s \hline
\end{tabular}
\end{center}
\label{default}
\end{table*}
"""
            format_dict = self._get_format_dict()
            stats_dict = self._get_stats_dict()
            template1 = template0 % format_dict
            formatted = template1 % stats_dict
            fh.write(formatted)

    def write_differential_dfxml(self, path_prefix):
        "Generate differential DFXML files."
        for key in self._differs:
            path0 = key[0]
            path1 = key[1]
            labels0 = self._annos[path0]
            labels1 = self._annos[path1]
            self._differs[key].write_differential_dfxml(os.path.join(path_prefix, labels0[0] + "-" + labels1[0] + ".dfxml"))

def main():
    global args
    dt = DifferTabulator()

    for annopath in args.labeled_xml_file:
        parts = annopath.split(":")
        if len(parts) < 3:
            raise ValueError("DFXML path specifications must be of the form long_label:short_label:path.")
        long_label = parts[0]
        short_label = parts[1]
        path = ":".join(parts[2:])
        if os.path.exists(path):
            dt.add(long_label, short_label, path)
        else:
            _logger.warning("Could not find file at %r.  Will not compare." % path)

    dt.write_differential_dfxml(".")
    dt.write_html("diffs.html")
    dt.write_latex("diffs.tex")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("labeled_xml_file", help="List of DFXML files, each colon-prefixed with a long and then a short label (e.g. 'Fiwalk:fi:fiout.dfxml')", nargs="+")
    argparser.add_argument("-d", "--debug", help="Enable debug printing", action="store_true")
    args = argparser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    main()

#TODO Byte run coverage & & & & & & \\
#TODO Directory entry count & & & & & & \\
