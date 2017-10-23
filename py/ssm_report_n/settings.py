import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

# ----------------------------------------------------------------------

def make_settings():
    from .settings_report import make_report_settings
    make_report_settings()
    # from .geographic import make_geographic_settings
    # make_geographic_settings()
    # for entry in [{"virus_type": "h3", "assay": "hi"}, {"virus_type": "h3", "assay": "neut"}, {"virus_type": "h1", "assay": "hi"}, {"virus_type": "bvic", "assay": "hi"}, {"virus_type": "byam", "assay": "hi"}]:
    #     make_map_settings(**entry)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
