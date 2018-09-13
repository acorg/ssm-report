import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

# ----------------------------------------------------------------------

def get_chart(virus_type, assay, lab, infix="", chart_dir=Path("merges")):
    if virus_type in ["bvic", "byam"]:
        vt = virus_type[0] + "-" + virus_type[1:]
    elif virus_type in ["h1"]:
        vt = "h1pdm"
    else:
        vt = virus_type
    chart_filename = chart_dir.joinpath(f"{lab.lower()}-{vt}-{assay.lower()}{infix}.ace")
    if not chart_filename.exists():
        raise RuntimeError(f"{chart_filename} not found")
    return chart_filename.resolve()

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
