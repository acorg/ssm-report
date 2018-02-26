import sys, os, json, pprint, copy
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from .map import make_map_for_lab
from acmacs_base.json import write_json

# ----------------------------------------------------------------------

sRadiusTime = ["theoretical.all", "theoretical.12m", "empirical.all", "empirical.12m"]

def make_serum_coverage_maps(output_dir, lab, virus_type, assay):
    s1_filename = Path("{}-{}.json".format(virus_type, assay)).resolve()
    s2_filename = Path("serumcoverage/{}-{}-{}.json".format(lab, virus_type, assay)).resolve()
    mods_coverage = json.load(s2_filename.open())["serum_coverage_mods"]
    for radius_time_type in sRadiusTime:
        for mod in mods_coverage[radius_time_type]:
            if mod[0] != "?":
                make_map_for_lab(output_dir=output_dir, prefix="serumcoverage-{}.{}".format(lab, mod), virus_type=virus_type, assay=assay, lab=lab, mod=mod, settings_files=[s1_filename, s2_filename])

# ----------------------------------------------------------------------

def make_serum_coverage_index(output_dir, lab, virus_type, assay, pdf_dir):

    def make_cell(base_filename, infix, safari):
        filename = "{}-{}/{}".format(virus_type, assay, Path(base_filename).name)
        result = ""
        if infix == "theoretical.all":
            result += '<td class="checkbox"><input class="sr-ag-row-selector" type="checkbox" onchange="checkbox_toggled(this);" file="{prefix}" /></td>\n'.format(prefix=filename[:filename.find(".theoretical.all")])
        else:
            filename = filename.replace("theoretical.all", infix)
        if safari:
            result += '<td><img src="{}" /></td>\n'.format(filename)
        else:
            result += '<td><object data="{}#toolbar=0"></object></td>\n'.format(filename) # toolbar=0 is for chrome
        return result

    s2_filename = Path("serumcoverage/{}-{}-{}.json".format(lab, virus_type, assay)).resolve()
    settings = json.load(s2_filename.open())
    for safari in [False, True]:
        index_filename = Path(output_dir, "index-serumcoverage-{}-{}-{}{}.html".format(lab, virus_type, assay, ".safari" if safari else ""))
        module_logger.info('making html serum coverage index: {}'.format(index_filename))
        with index_filename.open("w") as f:
            f.write(sHead % {
                "title": "Serum Coverage {} {} {}".format(lab.upper(), virus_type.upper(), assay.upper()),
                "width": 400,
                "height": 415,
                "export_filename": "serumcoverage-reviewed-{}-{}-{}.DATE.json".format(lab, virus_type, assay),
                })
            for mod in settings["serum_coverage_mods"]["theoretical.all"]:
                if mod[0] != "?":
                    pdf = pdf_dir.joinpath("serumcoverage-{}.{}-{}.pdf".format(lab, mod, lab.lower()))
                    if pdf.exists():
                        mod_data = settings["mods"][mod][0]
                        if mod_data.get("N") == "comment" and mod_data.get("type") == "data":
                            f.write(sSrAgRow.format(**mod_data, columns="\n".join(make_cell(base_filename=pdf, infix=infix, safari=safari) for infix in ["theoretical.all", "theoretical.12m", "empirical.all", "empirical.12m"])))
                        else:
                            f.write("<h3>{}</h3>\n".format(pdf.stem))
            f.write("</body></html>\n")

# ----------------------------------------------------------------------

sHead = """<html>
<head>
  <style>
    ul {list-style-type: none;}
    li {margin: 0.5em 0; }
    object {width: %(width)dpx; height: %(height)dpx;}
    img {width: %(width)dpx;}
    h3 { margin-left: 1.5em; }
    table.serum-coverage td { vertical-align: middle; border: none; padding: 0.5em; }
    table.serum-coverage td.checkbox { padding: 0; }
    div.sr-ag-row { border-left: 5px solid transparent; }
    div.sr-ag-row.sr-ag-chosen { border-left: 5px solid #E0E0FF; }
    table.serum-coverage td.sr-ag-chosen { background-color: #E0E0FF; }
    p { margin-left: 1em; width: 40em; }
    input.export { margin-left: 1em; }
  </style>
  <script>
    function checkbox_toggled(input_node) {
      if (input_node.checked)
        findAncestor(input_node, "sr-ag-row").classList.add('sr-ag-chosen');
      else
        findAncestor(input_node, "sr-ag-row").classList.remove('sr-ag-chosen');
    }

    function export_selection() {
      var selected  = Object.values(document.getElementsByClassName("sr-ag-row-selector")).filter(function(v) { return v.checked; }).map(function(v) { return v.getAttribute("file"); });
      if (selected.length > 0) {
        var export_anchor = document.getElementById('export_anchor');
        export_anchor.setAttribute("href", "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(selected, null, 2)));
        var datestamp = new Date().toISOString().slice(0, 10).replace(/-/g, "") + "-" + new Date().toISOString().slice(11, 16).replace(/:/g, "");
        export_anchor.setAttribute("download", "%(export_filename)s".replace("DATE", datestamp));
        export_anchor.click();
      }
      else {
        alert("Please select serum-antigen pairs using checkboxes on the left");
      }
    }

    function findAncestor(el, cls) {
      while ((el = el.parentElement) && !el.classList.contains(cls));
      return el;
    }
  </script>
  <title>%(title)s</title>
</head>
<body>
  <h2>%(title)s</h2>
  <p>Please select serum-antigen pair rows to be included in the report, then click Export button and send me downloaded %(export_filename)s file.</p>
  <input class="export" type="submit" value="Export" onclick="export_selection();" />
  <a id="export_anchor" style="display:none"></a>
"""

sSrAgRow = """\
<div class="sr-ag-row">
<h3>SR {serum_no} {serum_name}<br>AG {antigen_no} {antigen_name}<br>Titer: {titer}</h3>
<table class="serum-coverage">
  <tr><td></td><td>All theoretical: {theoretical}</td><td> 12 months theoretical: {theoretical}</td><td>All empirical: {empirical}</td><td> 12 months empirical: {empirical}</td></tr>
  <tr>
   {columns}
  </tr>
</table>
</div>
"""

# ----------------------------------------------------------------------

# def make_index_serum_coverage_html(output_dir):
#     def make_image(f, filename, safari):
#         if safari:
#             f.write('<td><img src="{}" /></td>\n'.format(filename))
#         else:
#             f.write('<td><object data="{}#toolbar=0"></object></td>\n'.format(filename)) # toolbar=0 is for chrome

#     for tag, pattern in [["cdc-hi", "h3-hi/serumcoverage*.all-cdc.pdf"], ["melb-hi", "h3-hi/serumcoverage*.all-melb.pdf"], ["nimr-hi", "h3-hi/serumcoverage*.all-nimr.pdf"], ["niid-neut", "h3-neut/serumcoverage*.all-niid.pdf"], ["cdc-neut", "h3-neut/serumcoverage*.all-cdc.pdf"], ["melb-neut", "h3-neut/serumcoverage*.all-melb.pdf"], ["nimr-neut", "h3-neut/serumcoverage*.all-nimr.pdf"]]:
#         filenames = sorted(Path(".").glob(pattern))
#         if filenames:
#             for safari in [False, True]:
#                 index_filename = Path(output_dir, "index-serumcoverage-{}{}.html".format(tag, ".safari" if safari else ""))
#                 module_logger.info('making html serum coverage index: {}'.format(index_filename))
#                 with index_filename.open("w") as f:
#                     f.write(sHead % {"title": "Serum Coverage", "width": 800, "height": 815})
#                     # img {border: 1px solid black;}
#                     for filename in filenames:
#                         f.write("<h3>{} {}</h3>\n".format(filename.parent.name.upper(), filename.stem))
#                         f.write("<table><tr>\n")
#                         make_image(f=f, filename=filename, safari=safari)
#                         filename2 = Path(str(filename).replace(".all-", ".12m-"))
#                         if filename.exists():
#                             make_image(f=f, filename=filename2, safari=safari)
#                         f.write("</tr></table>\n")
#                     f.write("</body></html>\n")


# ----------------------------------------------------------------------

def make_serum_coverage_report_settings():
    serum_coverage_report_file = Path("report-serumcoverage.json")
    if not serum_coverage_report_file.exists():
        report_settings = json.load(Path("report.json").open())
        report = {
            "cover": report_settings["cover"],
            "page_numbering": report_settings["page_numbering"],
            "pages": [
                {"type": "cover"},
                "new_page",
                {"type": "serum_coverage_map_set", "lab": "CDC", "assay": "HI", "virus_type": "H3"},
                {"type": "serum_coverage_map_set", "lab": "CDC", "assay": "NEUT", "virus_type": "H3"},
                {"type": "serum_coverage_map_set", "lab": "NIMR", "assay": "HI", "virus_type": "H3"},
                {"type": "serum_coverage_map_set", "lab": "NIMR", "assay": "NEUT", "virus_type": "H3"},
                {"type": "serum_coverage_map_set", "lab": "NIID", "assay": "NEUT", "virus_type": "H3"},
                {"type": "serum_coverage_map_set", "lab": "MELB", "assay": "HI", "virus_type": "H3"},
                {"type": "serum_coverage_map_set", "lab": "MELB", "assay": "NEUT", "virus_type": "H3"},
                ],
            }
        report["cover"]["addendum"] = "Addendum 2 (sera coverage)"
        write_json(serum_coverage_report_file, report, compact=True)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
