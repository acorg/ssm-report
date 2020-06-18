import sys
import logging; module_logger = logging.getLogger(__name__)
from . import report
from .error import Error

# ----------------------------------------------------------------------

sCommands = {
    "report": report.make_report,
    "addendum": report.make_addendum,
    }

# ----------------------------------------------------------------------

def process(command):
    sys.path.insert(0, ".")
    cmd = sCommands.get(command)
    if not cmd:
        raise Error(f"unknown command {command}")
    cmd()

# ----------------------------------------------------------------------

def list_for_helm():
    print("\n".join(sCommands))

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
