import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from acmacs_base.json import write_json
from acmacs_base.dict_merge import dict_merge

# ----------------------------------------------------------------------

def make_settings():
    from .settings_report import make_report_settings
    make_report_settings()
    # from .geographic import make_geographic_settings
    # make_geographic_settings()
    # for entry in [{"virus_type": "h3", "assay": "hi"}, {"virus_type": "h3", "assay": "neut"}, {"virus_type": "h1", "assay": "hi"}, {"virus_type": "bvic", "assay": "hi"}, {"virus_type": "byam", "assay": "hi"}]:
    for entry in [{"virus_type": "h3", "assay": "hi"}]:
        make_map_settings(**entry)

# ----------------------------------------------------------------------

def make_map_settings(virus_type, assay):
    vta = virus_type + "-" + assay
    map_settings_file = Path(vta + ".json")
    if not map_settings_file.exists():
        module_logger.info("writing {}".format(map_settings_file))
        map_settings_file.open("w").write(sMapSettings % {**{k: get_s(virus_type, assay, k) for k in ["labs", "vaccines"]}})
    return map_settings_file

# ----------------------------------------------------------------------

sMapSettings = """{ "_":"-*- js-indent-level: 2 -*-",
  %(labs)s,
  "mods": {
    "vaccines": [%(vaccines)s
    ]
  }
}
"""

def get_s(virus_type, assay, name):
    return globals()["s_{}_{}_{}".format(virus_type, assay, name)]

# ======================================================================
# H3
# ======================================================================

s_h3_hi_labs = '"labs": ["CDC", "MELB", "NIMR"]'

s_h3_hi_vaccines = """
      {"N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "previous", "passage": "cell"       }}, "fill": "blue",  "report": true, "outline": "black", "size": 15, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "current",  "passage": "egg"        }}, "fill": "red",   "report": true, "outline": "black", "size": 15, "show": true, "order": "raise"},
      {"N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "current",  "passage": "reassortant"}}, "fill": "green", "report": true, "outline": "black", "size": 15, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "surrogate"}}, "report": true, "outline": "black", "fill": "pink", "size": 15, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "previous", "passage": "egg"        }}, "report": true, "outline": "black", "fill": "blue", "size": 15, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "previous", "passage": "reassortant"}}, "report": true, "outline": "black", "fill": "blue", "size": 15, "show": true, "order": "raise"},
        {"?N": "antigens", "select": {"lab": "CDC", "vaccine": {"type": "current",  "passage": "cell"       }}, "report": true, "outline": "black", "fill": "red", "size": 15, "show": true, "order": "raise"},
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
