import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import sys, os, pprint, copy, subprocess

from acmacs_base.json import read_json, write_json
#from acmacs_map_draw import geographic_time_series

# ----------------------------------------------------------------------

def make_geographic(geo_dir, db_dir, force=False):
    if force or not geo_dir.joinpath("index.html").exists():
        prefixes = {}
        for virus_type in ["B", "H1", "H3"]:
            output_prefix = virus_type + "-geographic"
            output = geo_dir.joinpath(output_prefix + "-")
            script_filename = geo_dir.joinpath(output_prefix + ".sh")
            script_filename.open("w").write("#! /bin/bash\nexec ad geographic-draw --db-dir {pwd}/db -v -s '{s1}' --time-series '{period}' '{virus_type}' '{output}'\n".format(
                s1=str(Path(virus_type.lower() + "-geographic.json")),
                virus_type=virus_type,
                pwd=os.getcwd(),
                period="monthly",
                output=output
                ))
            script_filename.chmod(0o700)
            subprocess.check_call(str(script_filename))
            prefixes[virus_type] = output

        make_index_html(geo_dir.joinpath("index.html"), prefixes)

# ----------------------------------------------------------------------

def make_index_html(output_file, prefixes):
    with output_file.open("w") as f:
        f.write("<html><head><style>\nimg {border: 1px solid black;}\nul {list-style-type: none;}\nli {margin: 0.5em 0; }\nobject {width: 800px; height: 415px; }\n</style><title>Geographic maps</title></head><body>\n")
        for vt in sorted(prefixes):
            f.write("<h1>{}</h1>\n<ul>".format(vt))
            for fn in prefixes[vt].parent.glob(prefixes[vt].name + "*.pdf"):
                #f.write('<li><img src="{}" /></li>\n'.format(Path(fn).name))
                f.write('<li><object data="{}#toolbar=0"></object></li>\n'.format(Path(fn).name)) # toolbar=0 is for chrome
            f.write("</ul>\n")
        f.write("</body></html>\n")

# ----------------------------------------------------------------------

sSettings = {
  "coloring?": ["continent", "clade", "lineage", "lineage-deletion-mutants"],
  "point_size_in_pixels": 4.0,
  "point_density": 0.8,
  "continent_outline_color": "grey63",
  "continent_outline_width": 0.5,
  "output_image_width": 800,

  "title": {"offset": [0, 0], "text_size": 20, "background": "transparent", "border_color": "black", "border_width": 0, "text_color": "black", "padding": 10.0},

  "priority?": "draw VICTORIA_DEL on top of VICTORIA",
  "priority": ["YAMAGATA", "VICTORIA", "VICTORIA_DEL"]
}

sColoringByVirusType = {"b": "lineage-deletion-mutants", "h1": "clade", "h3": "clade"}

# ======================================================================

def make_geographic_settings(force):
    report_settings = read_json("report.json")
    for virus_type in ["b", "h1", "h3"]:
        filename = Path(virus_type + "-geographic.json")
        if force or not filename.exists():
            settings = copy.deepcopy(sSettings)
            settings["coloring"] = sColoringByVirusType[virus_type]
            settings["start_date"] = report_settings["time_series"]["date"]["start"]
            settings["end_date"] = report_settings["time_series"]["date"]["end"]
            write_json(filename, settings, compact=False)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
