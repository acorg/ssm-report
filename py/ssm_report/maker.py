# ssm report 2020-01

import os, json, subprocess
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
            if map_type in ["tree"]:
                print(f"{subtype}-{map_type}-i")
                print(f"{subtype}-{map_type}-cumulative")
            else:
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
    if command.get("command"):
        subprocess.check_call(command["command"], shell=True)
    else:
        # print(command)
        commands = Commands()
        getattr(commands, command["map"].replace("-", "_"))(**command)

# ----------------------------------------------------------------------

class Commands:

    def geo_stat(self, **args):
        from .stat import make_stat
        make_stat(stat_dir=Path("stat"), hidb_dir=self._db_dir(), force=True)
        from .geographic import make_geographic
        make_geographic(geo_dir=Path("geo"), db_dir=self._db_dir(), force=True)

    def tree(self, subtype, interactive, report_cumulative=False, **args):
        from .signature_page import tree_make
        tree_make(subtype=subtype, tree_dir=Path("tree"), seqdb=self._db_dir().joinpath("seqdb.json.xz"), interactive=interactive, report_cumulative=report_cumulative)

    def tree_cumulative(self, **args):
        self.tree(report_cumulative=True, **args)

    def _db_dir(self):
        return Path("db").resolve()

# ----------------------------------------------------------------------

def parse_cmd(cmd):
    fields = cmd.split("-")
    subtype = fields[0]
    if len(fields) == 1 or subtype not in sSubtypes:
        command = sSetup.get("commands", {}).get(cmd)
        if command:
            return {"command": command}
        elif cmd in ["geo-stat"]:
            return {"map": cmd}
        else:
            raise RuntimeError(f"Unrecognized command {cmd}")
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
        interactive = fields[-1] == "i"
        if interactive:
            map_type = "-".join(fields[1:-1])
        else:
            map_type = "-".join(fields[1:])
    return {"subtype": subtype, "map": map_type, "lab": lab, "interactive": interactive}

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
