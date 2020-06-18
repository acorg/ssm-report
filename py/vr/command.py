import sys, subprocess
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from . import report, map
from .error import Error

# ----------------------------------------------------------------------

def __get_merges(command): get_merges()
def __get_hidb(command): get_hidb()

sCommands = {
    "report": report.make_report,
    "report-addendum": report.make_addendum,
    "~get-merges": __get_merges,
    "~get-hidb": __get_hidb,
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

def get_hidb():
    subprocess.check_call('ssh albertine "whocc-update-ace-store && whocc-hidb5-update" && hidb-get-from-albertine', shell=True)

# ----------------------------------------------------------------------

def list_for_helm():
    print("\n".join(sorted(sCommands)))

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
