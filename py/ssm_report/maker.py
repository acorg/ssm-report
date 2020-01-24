# ssm report 2020-01

import os, json
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

sRootDir = Path("/syn/eu/ac/results/ssm")
sSetupFilename = "setup.json"
sSubtypes = ["h1", "h3", "h3n", "bvic", "byam"]

sSetup = None

# ----------------------------------------------------------------------

def set_working_dir():
    os.chdir(sorted(sRootDir.glob(f"*/{sSetupFilename}"))[-1].parent)

# ----------------------------------------------------------------------

def load_setup():
    global sSetup
    sSetup = json.load(open(sSetupFilename))

# ----------------------------------------------------------------------

def list_commands_for_helm():
    for subtype in sSubtypes:
        for map_type in sSetup[subtype].get("maps", []):
            print(f"{subtype}-{map_type}")
            for lab in sSetup.get(subtype, {}).get("labs", []):
                print(f"{subtype}-{map_type}-{lab}")
                if map_type not in ["ts"]:
                    print(f"{subtype}-{map_type}-i-{lab}")

    for command_name in sSetup.get("commands", {}):
        print(command_name)

# ----------------------------------------------------------------------

def init_dir(dir):
    sRootDir.joinpath(dir).mkdir()
    os.chdir(sRootDir.joinpath(dir))
    from . import init
    init.copy_templates(maker_version="2020-01")
    # init.init_git()
    # init.get_dbs()
    init.init_dirs()
    init.init_settings()

# ----------------------------------------------------------------------

def do(cmd):
    command = parse_cmd(cmd)
    print(command)

# ----------------------------------------------------------------------

def parse_cmd(cmd):
    fields = cmd.split("-")
    subtype = fields[0]
    if len(fields) == 1 or subtype not in sSubtypes:
        return {"command": cmd}
    labs = sSetup.get(subtype, {}).get("labs")
    if not labs:
        raise RuntimeError(f"Unrecognized command {cmd}: invalid subtype")
    if fields[-1] in labs:
        lab = fields[-1]
        interactive = len(fields) > 2 and fields[-2] == "i"
        if interactive:
            map_type = "-".join(fields[1:-2])
        else:
            map_type = "-".join(fields[1:-1])
    else:
        lab = None
        interactive = False
        map_type = "-".join(fields[1:])
    return {"subtype": subtype, "map": map_type, "lab": lab, "interactive": interactive}

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
