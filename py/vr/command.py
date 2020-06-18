import sys
import logging; module_logger = logging.getLogger(__name__)
from . import report, map
from .error import Error

# ----------------------------------------------------------------------

sCommands = {
    "report": report.make_report,
    "report-addendum": report.make_addendum,
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

def list_for_helm():
    print("\n".join(sorted(sCommands)))

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
