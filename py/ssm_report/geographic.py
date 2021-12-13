import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import sys, os, pprint, copy, subprocess

from acmacs_base.json import read_json, write_json
#from acmacs_map_draw import geographic_time_series

# ----------------------------------------------------------------------

def make_geographic(geo_dir, db_dir=None, settings_dir=Path("."), virus_types=None, force=False):
    if force or not geo_dir.joinpath("index.html").exists():
        geo_dir.mkdir(exist_ok=True)
        prefixes = {}
        for virus_type in virus_types or ["B", "H1", "H3"]:
            output_prefix = virus_type + "-geographic"
            output = geo_dir.joinpath(output_prefix + "-")
            script_filename = geo_dir.joinpath(output_prefix + ".sh")
            script_filename.open("w").write("#! /bin/bash\nexec geographic-draw {db_dir} -v -s '{s1}' --time-series '{period}' '{virus_type}' '{output}'\n".format(
                s1=str(settings_dir.joinpath(virus_type.lower() + "-geographic.json")),
                virus_type=virus_type,
                db_dir=f"--db-dir {db_dir}" if db_dir else "",
                period="monthly",
                output=output
                ))
            script_filename.chmod(0o700)
            subprocess.check_call(str(script_filename), shell=True)
            prefixes[virus_type] = output

        make_index_html(geo_dir.joinpath("index.html"), prefixes, safari=False)
        make_index_html(geo_dir.joinpath("index.safari.html"), prefixes, safari=True)

# ----------------------------------------------------------------------

def make_index_html(output_file, prefixes, safari):
    with output_file.open("w") as f:
        f.write("<html><head><style>\nimg {border: 1px solid black;}\nul {list-style-type: none;}\nli {margin: 0.5em 0; }\nobject {width: 800px; height: 415px; }\n</style><title>Geographic maps</title></head><body>\n")
        for vt in sorted(prefixes):
            f.write("<h1>{}</h1>\n<ul>".format(vt))
            for fn in sorted(prefixes[vt].parent.glob(prefixes[vt].name + "*.pdf")):
                if safari:
                    f.write('<li><img src="{}" /></li>\n'.format(Path(fn).name))
                else:
                    f.write('<li><object data="{}#toolbar=0"></object></li>\n'.format(Path(fn).name)) # toolbar=0 is for chrome
            f.write("</ul>\n")
        f.write("</body></html>\n")

# ----------------------------------------------------------------------

sSettings = {
    "coloring?": [
        {"N": "continent", "?continent_color": {"EUROPE": {"fill": "green", "outline": "black", "outline_width": 0}}},
        {"N": "clade", "?clade_color": {"SEQUENCED": {"fill": "yellow", "outline": "black", "outline_width": 0}}},
        {"N": "lineage", "?lineage_color": {"VICTORIA_2DEL": {"fill": "#23a8d1", "outline": "black", "outline_width": 0}, "VICTORIA_3DEL": {"fill": "#80FF00", "outline": "black", "outline_width": 0}}},
        {"N": "lineage-deletion-mutants", "?lineage_color": {"VICTORIA_2DEL": {"fill": "#23a8d1", "outline": "black", "outline_width": 0}, "VICTORIA_3DEL": {"fill": "#80FF00", "outline": "black", "outline_width": 0}}},
        {"N": "amino-acid", "apply": [{"sequenced": True, "color": "red"}, {"aa": ["156N" ,"155G"], "color": "blue"}], "report": False},
        {
            "ana1":  "#03569b",
            "ana2":  "#e72f27",
            "ana3":  "#ffc808",
            "ana4":  "#a2b324",
            "ana5":  "#a5b8c7",
            "ana6":  "#049457",
            "ana7":  "#f1b066",
            "ana8":  "#742f32",
            "ana9":  "#9e806e",
            "ana10": "#75ada9",
            "ana11": "#675b2c",
            "ana12": "#a020f0",
            "ana13": "#8b8989",
            "ana14": "#e9a390",
            "ana15": "#dde8cf",
            "ana16": "#00939f"
        }
    ],
    "point_size_in_pixels": 4.0,
    "point_density": 0.8,
    "continent_outline_color": "grey63",
    "continent_outline_width": 0.5,
    "output_image_width": 800,

    "title": {"offset": [0, 0], "text_size": 20, "background": "transparent", "border_color": "black", "border_width": 0, "text_color": "black", "padding": 10.0},

    "priority?": "draw VICTORIA_DEL on top of VICTORIA",
    "priority": ["YAMAGATA", "VICTORIA", "VICTORIA_DEL"]
}

sColoringByVirusType = {
    "b": {"N": "lineage-deletion-mutants"},
    "h1": {
        "N": "amino-acid",
        "apply": [
            {"sequenced": True, "color": "ana4"},
            {"aa": ["155E"], "color": "ana3"},
            {"aa": ["155X"], "color": "ana8"},
            {"aa": ["156D"], "color": "ana4"},
            {"aa": ["156S"], "color": "ana6"},
            {"aa": ["156K"], "color": "ana2"},
            {"aa": ["156X"], "color": "ana7"},
            {"aa": ["156N" ,"155G"], "color": "ana1"}
        ],
        "report": False
    },
    "h3": {                     # 2021-1216-tc1, Sarah 2021-12-11 14:27: colour the points as per clade in the second set of maps
        "N": "amino-acid",
        "apply": [
            {"sequenced": True, "color": "ana4"},
            {"color": "#1B9E77", "aa": ["92R", "121K", "158N", "159Y", "171K", "311Q", "406V",  "131K"]},
            {"color": "#66A61E", "aa": ["92R", "121K", "158N", "159Y", "171K", "311Q", "406V",  "135K"]},
            {"color": "#D95F02", "aa": ["92R", "121K", "131K", "158N",         "311Q", "406V",   "83E", "!94Y",  "186S"]},
            {"color": "#E6AB02", "aa": ["92R", "121K", "131K", "158N",         "311Q", "406V",   "83E", "!94Y",  "159N"]},
            {"color": "#674d01", "aa": ["92R", "121K", "131K", "158N",         "311Q", "406V",   "83E", "!94Y",  "159N", "156S"]},
            {"color": "#fede83", "aa": ["92R", "121K", "131K", "158N",         "311Q", "406V",   "83E", "!94Y",  "159N", "156Q"]},
            {"color": "#4037B3", "aa": ["92R", "121K", "158N", "159Y", "171K", "311Q", "406V",  "135K", "138S", "186D", "190N", "193S", "198P"]},
            {"color": "#9a4ef2", "aa": ["92R", "121K", "158N", "159Y", "171K", "311Q", "406V",  "135K", "138S", "186D", "190N", "193S", "198P",  "192F"]},
            {"color": "#E7298A", "aa": ["92R", "121K", "158N", "159Y", "171K", "311Q", "406V",  "135K", "137F", "138S", "193S"]}
        ],
        "report": False
    },
    # before 2021-1216-tc1
    # "h3": {"N": "clade"}
}

# ======================================================================

def make_geographic_settings(settings_dir=Path("."), start_date=None, end_date=None, force=False):
    if not start_date and not end_date:
        report_settings = read_json("report.json")
        start_date = report_settings["time_series"]["date"]["start"]
        end_date = report_settings["time_series"]["date"]["end"]
    for virus_type in ["b", "h1", "h3"]:
        filename = settings_dir.joinpath(virus_type + "-geographic.json")
        if force or not filename.exists():
            settings = copy.deepcopy(sSettings)
            settings["coloring"] = sColoringByVirusType[virus_type]
            settings["start_date"] = start_date
            settings["end_date"] = end_date
            write_json(filename, settings, compact=False)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
