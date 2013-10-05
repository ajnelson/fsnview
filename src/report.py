#!/usr/bin/python3

__version__ = "0.0.1"

import logging
import idifference
import os

def make_status_dict(results_dirname, expected_result_names):
    """
    Returns a dictionary.
    Key: DFXML file basename
    Value: Pair, (return code, path to xmllint's stderr file)
    """
    retval = dict()
    if not os.path.exists(results_dirname):
        return retval
    for (dirpath, dirnames, filenames) in os.walk(results_dirname):
        for filename in filenames:
            if not filename.endswith(".status.log"):
                continue
            bn = filename.replace(".status.log","")
            if bn not in expected_result_names:
                continue
            slog_fn = filename
            elog_fn = filename.replace(".status.log", ".err.log")
            rc = None
            with open(os.path.join(dirpath, slog_fn), "r") as slog_fh:
                rc_txt = slog_fh.read(10).strip()
                if rc_txt != "":
                    rc = int(rc_txt)
            retval[bn] = (rc, os.path.join(dirpath, elog_fn))
    return retval

def main():
    results_root = os.path.abspath(os.path.expanduser(args.results_directory))
    logging.debug("args.results_directory = %r" % args.results_directory)
    logging.debug("results_root = %r" % results_root)

    stuff = dict()
    stuff["report_title"] = "Template"
    print("""\
<!DOCTYPE html>
<html>
  <head>
    <title>%(report_title)s</title>
  </head>
  <body>
    <h1>%(report_title)s</h1>""" % stuff)

    dfxml_script_list = ["analyze_with_fiwalk.sh", "analyze_with_py360.sh", "analyze_with_uxtaf.sh"]
    dfxml_file_list = ["fiwalk.dfxml", "py360.dfxml", "uxtaf.dfxml"]

    #Retrieve validation results from FSNView directory; store for use in validation section and validation errors appendix
    validation_status = make_status_dict("validation", dfxml_file_list)
    dfxml_status = make_status_dict("dfxml", dfxml_script_list)

    #Write DFXML validation section
    print("""\
    <section>
      <header><h2>DFXML validation</h2></header>
      <table>
        <thead>
          <tr>
            <th>File</th>
            <th>DFXML schema version</th>
            <th>Validates</th>
          </tr>
        </thead>
        <tfoot></tfoot>
        <tbody>""")
    for xml_file_path in dfxml_file_list:
        stuff = dict()

        xml_file_basename = os.path.basename(xml_file_path)

        stuff["xml_basename"] = xml_file_basename
        stuff["dfxml_version"] = "1.0"

        validation_rc = validation_status.get(xml_file_basename,(None,None))[0]
        if validation_rc is None:
            stuff["validation_results"] = "Not checked"
        elif validation_rc == 0:
            stuff["validation_results"] = "Yes"
        else:
            stuff["validation_results"] = """<a href="#validation_error_%s">No</a>""" % xml_file_basename
        print("""\
          <tr>
            <td>%(xml_basename)s</td>
            <td>%(dfxml_version)s</td>
            <td>%(validation_results)s</td>
          </tr>""" % stuff)
    print("""\
        </tbody>
      </table>
    </section>""")

    #Write differences section
    stuff = dict()
    stuff["idifference_version"] = idifference.__version__
    print("""\
    <section>
      <header><h2>Differences in DFXML</h2></header>
      <p>This table was created by using idifference.py (version <code>%(idifference_version)s</code>) as a library.  The name abbreviations are:</p>
      <dl>""" % stuff)
    abbreviations = dict()
    abbreviations["Ux"] = "Uxtaf"
    abbreviations["P3"] = "Py360"
    abbreviations["Fi"] = "Fiwalk"
    for ab in abbreviations:
        print("""\
      <dt>%s</dt><dd>%s</dd>""" % (ab, abbreviations[ab]))
    print("""\
      </dl>""")

    with open(os.path.join(results_root, "differences/diffs.html"), "r") as diffs_table_fh:
        for line in diffs_table_fh:
            print(line)

    print("""\
    </section>""")

    #Report processing results
    print("""\
    <section>
      <header><h2>Processing results</h2></header>
      <p>FSNView ran these scripts, each of which generates DFXML for the disk image's contents:</p>
      <table>
        <thead>
          <tr>
            <th>Script</th>
            <th>Successful</th>
          </tr>
        </thead>
        <tfoot></tfoot>
        <tbody>""")
    for ds in dfxml_script_list:
        stuff = dict()
        stuff["dfxml_script_basename"] = ds
        script_rc = dfxml_status.get(ds, (None,None))[0]
        if script_rc is None:
            stuff["success_results"] = "Not run"
        elif script_rc == 0:
            stuff["success_results"] = "Yes"
        else:
            stuff["success_results"] = """<a href="#script_error_%s">No</a>""" % ds
        print("""\
          <tr>
            <td>%(dfxml_script_basename)s</td>
            <td>%(success_results)s</td>
          <tr>""" % stuff)
    print("""\
        </tbody>
      </table>
    </section>""")

    #Generate success supplemental notes
    if len(dfxml_status.keys()) > 0:
        print("""\
    <section>
      <header><h2>Appendix: DFXML generation script errors</h2></header>""")
        for k in sorted(dfxml_status.keys()):
            stuff = dict()
            stuff["script_basename"] = k
            stuff["script_rc"] = dfxml_status[k][0]
            stuff["script_stderr"] = dfxml_status[k][1]
            if stuff["script_rc"] is None or stuff["script_rc"] == 0:
                continue
            print("""\
      <section id="script_error_%(script_basename)s">
        <header><h3>For %(script_basename)s</h3></header>
        <p>Error code: %(script_rc)r</p>
        <pre>""" % stuff)
            with open(stuff["script_stderr"], "r") as elog_fh:
                for line in elog_fh:
                    print(line[:-1])
            print("""</pre>
      </section>""")
        print("""\
    </section>""")

    #Generate validation supplemental notes
    if len(validation_status.keys()) > 0:
        print("""\
    <section>
      <header><h2>Appendix: DFXML validation errors</h2></header>""")
        for k in sorted(validation_status.keys()):
            stuff = dict()
            stuff["xml_basename"] = k
            stuff["xmllint_rc"] = validation_status[k][0]
            stuff["xmllint_stderr"] = validation_status[k][1]
            print("""\
      <section id="validation_error_%(xml_basename)s">
        <header><h3>For %(xml_basename)s</h3></header>
        <p>Error code: %(xmllint_rc)r</p>
        <pre>""" % stuff)
            with open(stuff["xmllint_stderr"],"r") as elog_fh:
                for line in elog_fh:
                    print(line[:-1])
            print("""</pre>
      </section>""")
        print("""\
    </section>""")

    #Write footer
    print("""\
    <footer>
      <p>Generated by FSNView, Git version TODO.</p>
    </footer>
  </body>
</html>""")   

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("results_directory", help="Directory containing the results of the rest of FSNView's operations.  See README for description of expected hierarchy.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    main()
