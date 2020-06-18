import sys
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from . import report, map
from .error import Error

# ----------------------------------------------------------------------

def __get_merges(command): get_merges()

sCommands = {
    "report": report.make_report,
    "report-addendum": report.make_addendum,
    "~get-merges": __get_merges,
    }

from report import maps
for map_data in maps():
    sCommands["-".join(map_data)] = map.make_map

# ----------------------------------------------------------------------

def process(command):
    cmd = sCommands.get(command)
    if not cmd:
        raise Error(f"unknown command {command}")
    cmd(command)

# ----------------------------------------------------------------------

def get_merges():
    output_dir = Path("merges")
    output_dir.mkdir(exist_ok=True)
    from acmacs_whocc import acmacs
    acmacs.get_recent_merges(output_dir)

# ----------------------------------------------------------------------

def list_for_helm():
    print("\n".join(sorted(sCommands)))

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
