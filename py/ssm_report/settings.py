import sys, os, json
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from acmacs_base.json import write_json
from acmacs_base.dict_merge import dict_merge

# ----------------------------------------------------------------------

def make_settings(force=False):
    from .settings_report import make_report_settings
    make_report_settings()
    from .serum_coverage import make_serum_coverage_report_settings
    make_serum_coverage_report_settings()
    from .geographic import make_geographic_settings
    make_geographic_settings(force=force)
    for entry in [
            {"virus_type": "h3", "assay": "hi"},
            {"virus_type": "h3", "assay": "neut"},
            {"virus_type": "h1", "assay": "hi"},
            {"virus_type": "bvic", "assay": "hi"},
            {"virus_type": "byam", "assay": "hi"}
            ]:
        make_map_settings(force=force, **entry)

# ----------------------------------------------------------------------

sMapSettings = """{ "_":"-*- js-indent-level: 2 -*-",
  "labs": %(labs)s,
  "information_labs": %(labs)s,
  "mods": {
%(mods)s
  }
}
"""

def make_map_settings(virus_type, assay, force):
    vta = virus_type + "-" + assay
    map_settings_file = Path(vta + ".json")
    if force or not map_settings_file.exists():
        module_logger.info("writing {}".format(map_settings_file))
        labs = get_s(virus_type, assay, "labs")
        data = sMapSettings % {"labs": json.dumps(labs), "mods": get_s(virus_type=virus_type, assay=assay, name="data") + ",\n" + ",\n".join(make_mod(virus_type=virus_type, assay=assay, lab=lab) for lab in labs)}
        map_settings_file.open("w").write(data)
    return map_settings_file

# ----------------------------------------------------------------------

def make_mod(virus_type, assay, lab):
    result = '\n    "?": "===================== {lab}  {virus_type}  {assay} ================================================="'.format(virus_type=virus_type.upper(), assay=assay.upper(), lab=lab)
    result += ",\n" + get_s_lab(virus_type=virus_type, assay=assay, lab=lab, name="data")
    return result

# ----------------------------------------------------------------------

def get_s(virus_type, assay, name):
    return globals()["s_{}_{}_{}".format(virus_type, assay, name)]

def get_s_lab(virus_type, assay, lab, name):
    return globals()["s_{}_{}_{}_{}".format(virus_type, assay, lab, name)]

# ======================================================================
# H1 HI
# ======================================================================

s_h1_hi_labs = ["ALL"]

s_h1_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      "clades",
      {"N": "antigens", "select": {"older_than_days": 183}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "serology": [
      {"N": "antigens", "select": {"name": "SHIMANE/75/2017", "passage": "cell"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}}
    ]"""

# --------------- ALL H1 -------------------------------------------------------

s_h1_hi_ALL_data = """
    "ALL_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "ALL_vaccines_information": [
    ],
    "ALL_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "ALL_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "ALL_viewport": [
      {"N": "viewport", "rel": [8, 5.5, -12]}
    ],
    "ALL_pre": [
    ],
    "ALL_mid": [
    ],
    "ALL_post": [
    ],
    "ALL_serology": [
    ]"""

# --------------- CDC H1 -------------------------------------------------------

s_h1_hi_CDC_data = """
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
        "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "CDC_vaccines_information": [
    ],
    "CDC_serology": [
    ],
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# ======================================================================
# H3 HI
# ======================================================================

s_h3_hi_labs = ["CDC", "MELB", "NIMR"]

s_h3_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "aa_at_142": [
      {"N": "amino-acids", "pos": [142], "outline": "black", "legend": {"count": true}, "order": "raise"}
    ],
    "serology": [
      {"N": "antigens", "select": {"name": "WASHINGTON/106/2016", "passage": "cell"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}},
      {"N": "antigens", "select": {"name": "WASHINGTON/106/2016", "passage": "egg"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}}
    ],
    "information": [
      "clades",
      {"N": "antigens", "select": {"older_than_days": 183}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ]"""

    # "serum_sectors": [
    #   {"N": "serum_circle", "serum": {"lab": "provide-lab", "index": "provide serum selector"}, "?antigen": {"index": 0}, "report": true,
    #    "circle": {"fill": "#C08080FF", "outline": "blue", "outline_width": 2, "angle_degrees": [0, 30], "radius_line_dash": "dash2", "?radius_line_color": "red", "?radius_line_width": 1},
    #    "mark_serum": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}},
    #    "mark_antigen": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}}}
    # ],
    # "serum_coverage_hk": [
    #   {"N": "serum_coverage", "serum": {"lab": "provide lab", "index": "provide serum selector"}, "?antigen": {"index": 1}, "report": true,
    #    "mark_serum": {"fill": "red", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12, "weight": "bold"}},
    #    "within_4fold": {"outline": "pink", "outline_width": 3, "order": "raise"},
    #    "outside_4fold": {"fill": "grey50", "outline": "black", "order": "raise"}}
    # ]

# --------------- CDC H3 HI -------------------------------------------------------

s_h3_hi_CDC_data = """
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise"}
    ],
    "CDC_vaccines_information": [
    ],
    "CDC_serology": [
    ],
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [6.5, 7.5, -11]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- MELB H3 HI -------------------------------------------------------

s_h3_hi_MELB_data = """
    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"}
    ],
    "MELB_vaccines_information": [
    ],
    "MELB_serology": [
    ],
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [3.2, 1, -6]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- NIMR H3 HI -------------------------------------------------------

s_h3_hi_NIMR_data = """
    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIMR_vaccines_information": [
    ],
    "NIMR_serology": [
    ],
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [1.5, 2, -3]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
# H3 Neut
# ======================================================================

s_h3_neut_labs = ["CDC", "MELB", "NIID", "NIMR"]

s_h3_neut_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "serology": [
      {"N": "antigens", "select": {"name": "WASHINGTON/106/2016", "passage": "cell"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}},
      {"N": "antigens", "select": {"name": "WASHINGTON/106/2016", "passage": "egg"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}}
    ],
    "information": [
      "clades",
      {"N": "antigens", "select": {"older_than_days": 183}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ]"""

    # "serum_sectors": [
    #   {"N": "serum_circle", "serum": {"lab": "provide-lab", "index": "provide serum selector"}, "?antigen": {"index": 0}, "report": true,
    #    "circle": {"fill": "#C08080FF", "outline": "blue", "outline_width": 2, "angle_degrees": [0, 30], "radius_line_dash": "dash2", "?radius_line_color": "red", "?radius_line_width": 1},
    #    "mark_serum": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}},
    #    "mark_antigen": {"fill": "lightblue", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12}}}
    # ],
    # "serum_coverage_hk": [
    #   {"N": "serum_coverage", "serum": {"lab": "provide lab", "index": "provide serum selector"}, "?antigen": {"index": 1}, "report": true,
    #    "mark_serum": {"fill": "red", "outline": "black", "order": "raise", "label": {"name_type": "full", "offset": [0, 1.2], "color": "black", "size": 12, "weight": "bold"}},
    #    "within_4fold": {"outline": "pink", "outline_width": 3, "order": "raise"},
    #    "outside_4fold": {"fill": "grey50", "outline": "black", "order": "raise"}}
    # ]

# --------------- CDC H3 Neut -------------------------------------------------------

s_h3_neut_CDC_data = """
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "CDC_vaccines_information": [
    ],
    "CDC_serology": [
    ],
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- MELB H3 Neut -------------------------------------------------------

s_h3_neut_MELB_data = """
    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "MELB_vaccines_information": [
    ],
    "MELB_serology": [
    ],
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- NIID H3 Neut -------------------------------------------------------

s_h3_neut_NIID_data = """
    "NIID_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIID_vaccines_information": [
    ],
    "NIID_serology": [
    ],
    "NIID_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIID_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIID_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "NIID_pre": [
    ],
    "NIID_mid": [
    ],
    "NIID_post": [
    ]"""

# --------------- NIMR H3 Neut -------------------------------------------------------

s_h3_neut_NIMR_data = """
    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIMR_vaccines_information": [
    ],
    "NIMR_serology": [
    ],
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [0, 0, 0]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
# B/Vic HI
# ======================================================================

s_bvic_hi_labs = ["CDC", "MELB", "NIID", "NIMR"]

s_bvic_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      "clades",
      {"N": "antigens", "select": {"older_than_days": 183}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "serology": [
      {"N": "antigens", "select": {"name": "SINGAPORE/INFKK-16-0575/2016", "passage": "egg"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}}
    ]"""

# --------------- CDC B/Vic HI -------------------------------------------------------

s_bvic_hi_CDC_data = """
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "CDC_vaccines_information": [
    ],
    "CDC_serology": [
    ],
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [10, 10, -15]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- MELB B/Vic HI -------------------------------------------------------

s_bvic_hi_MELB_data = """
    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "MELB_vaccines_information": [
    ],
    "MELB_serology": [
    ],
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [4, 6.5, -7]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- NIID B/Vic HI -------------------------------------------------------

s_bvic_hi_NIID_data = """
    "NIID_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIID_vaccines_information": [
    ],
    "NIID_serology": [
    ],
    "NIID_flip": [
      {"N": "flip", "direction": "ew"}
    ],
    "NIID_rotate": [
      {"N": "rotate", "degrees": 90}
    ],
    "NIID_viewport": [
      {"N": "viewport", "rel": [1.6, 1.2, -3]}
    ],
    "NIID_pre": [
    ],
    "NIID_mid": [
    ],
    "NIID_post": [
    ]"""

# --------------- NIMR B/Vic HI -------------------------------------------------------

s_bvic_hi_NIMR_data = """
    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIMR_vaccines_information": [
    ],
    "NIMR_serology": [
    ],
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [4, 4, -7]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
# B/Yam HI
# ======================================================================

s_byam_hi_labs = ["CDC", "MELB", "NIID", "NIMR"]

s_byam_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ],
    "no_legend": [
      {"N": "legend", "show": false}
    ],
    "information": [
      "clades",
      {"N": "antigens", "select": {"older_than_days": 183}, "fill": "grey80", "outline": "grey80", "order": "lower"},
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "serology": [
      {"N": "antigens", "select": {"name": "SINGAPORE/INFTT-16-0610/2016", "passage": "egg"}, "fill": "#FFA500",  "report": true, "outline": "black", "size": 18, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 24}}
    ]"""

# --------------- B/Yam HI CDC -------------------------------------------------------

s_byam_hi_CDC_data = """
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "CDC_vaccines_information": [
    ],
    "CDC_serology": [
    ],
    "CDC_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "CDC_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "CDC_viewport": [
      {"N": "viewport", "rel": [2, 5, -7]}
    ],
    "CDC_pre": [
    ],
    "CDC_mid": [
    ],
    "CDC_post": [
    ]"""

# --------------- B/Yam HI MELB -------------------------------------------------------

s_byam_hi_MELB_data = """
    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "MELB_vaccines_information": [
    ],
    "MELB_serology": [
    ],
    "MELB_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "MELB_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "MELB_viewport": [
      {"N": "viewport", "rel": [2.5, 1.2, -4]}
    ],
    "MELB_pre": [
    ],
    "MELB_mid": [
    ],
    "MELB_post": [
    ]"""

# --------------- B/Yam HI NIID -------------------------------------------------------

s_byam_hi_NIID_data = """
    "NIID_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIID_vaccines_information": [
    ],
    "NIID_serology": [
    ],
    "NIID_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIID_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIID_viewport": [
      {"N": "viewport", "rel": [-0.7, -0.3, -1]}
    ],
    "NIID_pre": [
    ],
    "NIID_mid": [
    ],
    "NIID_post": [
    ]"""

# --------------- B/Yam HI NIMR -------------------------------------------------------

s_byam_hi_NIMR_data = """
    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}},
      {"N": "antigens", "select": {"vaccine": {"type": "surrogate"}},                          "fill": "pink",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise",
          "label": {"offset": [0, 1], "name_type": "abbreviated_with_passage_type", "size": 32}}
    ],
    "NIMR_vaccines_information": [
    ],
    "NIMR_serology": [
    ],
    "NIMR_flip": [
      {"?N": "flip", "direction": "ew"}
    ],
    "NIMR_rotate": [
      {"N": "rotate", "degrees": 0}
    ],
    "NIMR_viewport": [
      {"N": "viewport", "rel": [1.5, 2.3, -4]}
    ],
    "NIMR_pre": [
    ],
    "NIMR_mid": [
    ],
    "NIMR_post": [
    ]"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
