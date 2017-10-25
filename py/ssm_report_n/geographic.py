import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import sys, pprint, datetime, copy

from acmacs_base.json import read_json, write_json
#from acmacs_map_draw import geographic_time_series

# ----------------------------------------------------------------------

def make_geographic(geo_dir, db_dir, force=False):
    if force or not geo_dir.joinpath("index.html").exists():
        report_settings = read_json("report.json")
        settings_dates = report_settings["time_series"]["date"]
        module_logger.info('Geographic time series in {} start: {} end: {}'.format(geo_dir, settings_dates["start"], settings_dates["end"]))
        # prefixes = {}
        # for virus_type in ["B", "H1", "H3"]:
        #     settings = copy.deepcopy(geographic_settings["geographic"])
        #     settings["coloring"] = geographic_settings["geographic"]["coloring"].get(virus_type, "continent")
        #     color_override = geographic_settings["geographic"].get("color_override", {}).get(virus_type)
        #     if color_override:
        #         settings["color_override"] = color_override
        #     elif "color_override" in settings:
        #         del settings["color_override"]
        #     settings["hidb_dir"] = hidb_dir
        #     settings["seqdb_dir"] = seqdb_dir
        #     prefixes[virus_type] = geo_dir.joinpath(virus_type + "-geographic-")
        #     geographic_time_series(output_prefix=str(prefixes[virus_type]), virus_type=virus_type, period="month", start_date=settings_dates["start"], end_date=settings_dates["end"], settings=settings)
        # make_index_html(geo_dir.joinpath("index.html"), prefixes)

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
    "geographic": {
        "coloring": {"B": "lineage-deletion-mutants", "H1": "continent", "H3": "clade"},
        "coloring?": ["continent", "clade", "lineage", "lineage-deletion-mutants"],
        "color_override": {"B": {"?": "B/Vic deletion mutants", "?B/DOMINICAN REPUBLIC/9932/2016": "#00FFFF"}},
        "deletion_mutant_color": "cyan",
        "point_size_in_pixels": 4.0,
        "point_density": 0.8,
        "outline_color": "grey63",
        "outline_width": 0.5,
        "title": {"offset": [0, 0], "text_size": 20, "background": "transparent", "border_width": 0},
    }
}

sGeographicSettingsFile = Path("geographic.json")

sGeographicSettings = None

def geographic_settings():
    global sGeographicSettings
    if sGeographicSettings is None:
        sGeographicSettings = read_json(make_geographic_settings())
    return sGeographicSettings

# ======================================================================

def make_geographic_settings():
    global sGeographicSettingsFile
    if not sGeographicSettingsFile.exists():
        geographic = copy.deepcopy(sSettings)
        write_json(sGeographicSettingsFile, geographic, compact=False)
    return sGeographicSettingsFile

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
