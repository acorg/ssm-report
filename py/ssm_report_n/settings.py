import sys, os, json
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from acmacs_base.json import write_json
from acmacs_base.dict_merge import dict_merge

# ----------------------------------------------------------------------

def make_settings(force=False):
    from .settings_report import make_report_settings
    make_report_settings()
    # from .geographic import make_geographic_settings
    # make_geographic_settings()
    # for entry in [{"virus_type": "h3", "assay": "hi"}, {"virus_type": "h3", "assay": "neut"}, {"virus_type": "h1", "assay": "hi"}, {"virus_type": "bvic", "assay": "hi"}, {"virus_type": "byam", "assay": "hi"}]:
    for entry in [{"virus_type": "h3", "assay": "hi"}]:
        make_map_settings(force=force, **entry)

# ----------------------------------------------------------------------

sMapSettings = """{ "_":"-*- js-indent-level: 2 -*-",
  "labs": %(labs)s,
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
        data = sMapSettings % {"labs": json.dumps(labs), "mods": ",\n".join(make_mod(virus_type=virus_type, assay=assay, lab=lab) for lab in labs)}
        map_settings_file.open("w").write(data)
    return map_settings_file

# ----------------------------------------------------------------------

def make_mod(virus_type, assay, lab):
    result = '\n    "?": "===================== {lab}  {virus_type}  {assay} ================================================="'.format(virus_type=virus_type.upper(), assay=assay.upper(), lab=lab)
    result += ",\n" + get_s(virus_type=virus_type, assay=assay, name="data")
    result += ",\n" + get_s_lab(virus_type=virus_type, assay=assay, lab=lab, name="data")
    return result

# ----------------------------------------------------------------------

def get_s(virus_type, assay, name):
    return globals()["s_{}_{}_{}".format(virus_type, assay, name)]

def get_s_lab(virus_type, assay, lab, name):
    return globals()["s_{}_{}_{}_{}".format(virus_type, assay, lab, name)]

# ======================================================================
# H3
# ======================================================================

s_h3_hi_labs = ["CDC", "MELB", "NIMR"]

s_h3_hi_data = """
    "set_scale": [
      {"N": "point_scale", "scale": 2.5, "outline_scale": 1}
    ],
    "set_legend": [
      {"N": "legend", "label_size": 14, "point_size": 10}
    ]"""

# --------------- CDC -------------------------------------------------------

s_h3_hi_CDC_data = """
    "CDC_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise"}
    ],
    "CDC_flip": [
      "?flip_ew"
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

# --------------- MELB -------------------------------------------------------

s_h3_hi_MELB_data = """
    "MELB_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise"}
    ],
    "MELB_flip": [
      "?flip_ew"
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

# --------------- NIMR -------------------------------------------------------

s_h3_hi_NIMR_data = """
    "NIMR_vaccines": [
      {"N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 26, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 26, "show": true, "order": "raise"}
    ],
    "NIMR_flip": [
      "?flip_ew"
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
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
