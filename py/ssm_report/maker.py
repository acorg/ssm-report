# ssm report 2020-01

import os, json, subprocess
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

sRootDir = Path("/syn/eu/ac/results/ssm")
sSetupFilename = "setup.json"
sReportFilename = "report.json"
sSubtypes = ["h1", "h3", "h3n", "bvic", "byam"]

sSetup = None

sDotSize = None # default is None, see map.py:make_ts()

class Error (RuntimeError): pass

# ----------------------------------------------------------------------

def set_working_dir():
    os.chdir(sorted(sRootDir.glob(f"*/{sSetupFilename}"))[-1].parent)

# ----------------------------------------------------------------------

def load_setup():
    global sSetup
    sSetup = json.load(open(sSetupFilename))

def load_report():
    global sReport
    sReport = json.load(open(sReportFilename))

# ----------------------------------------------------------------------

def list_commands_for_helm():
    for subtype in sSubtypes:
        if sSetup[subtype].get("maps"):
            print(f"{subtype}-maps")
            for map_type in sSetup[subtype]["maps"]:
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

    for command_name in ["get-merges", "get-hidb-seqdb", "report", "report-abbreviated", "addendum-1", "addendum-2", "addendum-3", "addendum-4", "addendum-5"]:
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

def do(command_name):
    Commands().do(command_name)

# ----------------------------------------------------------------------

class Commands:

    def do(self, command_name):
        command = self.parse_cmd(command_name)
        if command.get("command"):
            subprocess.check_call(command["command"], shell=True)
        else:
            Commands().do_parsed(command)

    def do_parsed(self, command):
        # print(command)
        try:
            getattr(self, command["map"].replace("-", "_"))(**command)
        except AttributeError:
            raise Error(f"Unrecognized command: {cmd}")

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

    def maps(self, subtype, assay, **args):
        sep = "=" * 100
        for command_name in sSetup[subtype]["maps"]:
            if not command_name.startswith("tree") and not command_name.startswith("sp"):
                print(f"{sep}\n{command_name}\n{sep}\n")
                self.do(f"{raw_subtype}-{command_name}")

    def aa_156(self, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .map import make_map
        if months:
            mod = f"aa-156-{months}m"
        else:
            mod = f"aa-156"
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_map(prefix=mod, virus_type=subtype, assay=assay, lab=labs, mod=mod, output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and len(labs) == 1, force=True)

    def serology_aa_156(self, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .map import make_map
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_map(prefix="serology-aa-156", virus_type=subtype, assay=assay, lab=labs, mod="serology-aa-156", output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and len(labs) == 1, force=True)

    def ts(self, subtype, assay, lab, open_image=False, **args):
        from .map import make_ts
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_ts(virus_type=subtype, assay=assay, lab=labs, output_dir=self._output_path(subtype=subtype, assay=assay), force=True, dot_size=sDotSize, start=sSetup["time-series"]["date"]["start"], end=sSetup["time-series"]["date"]["end"], period=sSetup["time-series"]["period"], teleconference=sReport["cover"]["teleconference"], previous=sReport["previous"])

    def sp(self, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .signature_page import signature_page_make, signature_page_source_dir_init, signature_page_output_dir_init
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        sp_dir = Path("sp")
        signature_page_source_dir_init(sp_dir)
        signature_page_output_dir_init(sp_dir)
        signature_page_make(virus_type=subtype, assay=assay, lab=labs, sp_source_dir=sp_dir, sp_output_dir=sp_dir, tree_dir=Path("tree"), merge_dir=Path("merges").resolve(), seqdb=self._seqdb_file(), interactive=interactive)

    def spc(self, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .signature_page import signature_page_make, signature_page_source_dir_init, signature_page_output_dir_init
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        sp_dir = Path("spc")
        signature_page_source_dir_init(sp_dir)
        signature_page_output_dir_init(sp_dir)
        signature_page_make(virus_type=subtype, assay=assay, lab=labs, serum_circles=True, orig_sp_source_dir=Path("sp"), sp_source_dir=sp_dir, sp_output_dir=sp_dir, tree_dir=Path("tree"), merge_dir=Path("merges").resolve(), seqdb=self._seqdb_file(), interactive=interactive)

    def _output_path(self, subtype, assay):
        return Path(f"{subtype[:2]}-{assay}")

    def report(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def report_abbreviated(self):
        from .report import make_report_abbreviated
        make_report_abbreviated(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def addendum_1(self):
        from .report import make_signature_page_addendum_interleave
        make_signature_page_addendum_interleave(source_dirs=[Path("sp"), Path("spsc")], output_dir=Path("report"), title="Addendum 1 (integrated genetic-antigenic analyses)", output_name="sp-spsc-addendum", T_SerumCirclesDescriptionEggCell=True)

    def _db_dir(self):
        return Path("db").resolve()

    def _seqdb_file(self):
        return self._db_dir().joinpath("seqdb.json.xz")

    def _get_lab(self, subtype, assay, lab, **args):
        if lab:
            return lab
        else:
            return self._get_setup(subtype=subtype, assay=assay).get("labs")

    def _get_setup(self, subtype, assay):
        if subtype == "h3" and assay == "neut":
            return sSetup.get("h3n", {})
        else:
            return sSetup.get(subtype, {})

    @classmethod
    def parse_cmd(cls, cmd):
        fields = cmd.split("-")
        subtype = fields[0]
        if len(fields) == 1 or subtype not in sSubtypes:
            command = sSetup.get("commands", {}).get(cmd)
            if command:
                return {"command": command}
            else: # elif cmd in ["geo-stat"]:
                return {"map": cmd}
        labs = sSetup.get(subtype, {}).get("labs")
        if not labs:
            raise Error(f"Unrecognized command {cmd}: invalid subtype")
        map_type_end = len(fields)
        if fields[-1] in labs:
            lab = fields[-1]
            map_type_end -= 1
            interactive = len(fields) > 2 and fields[-2] == "i"
        else:
            lab = None
            interactive = fields[-1] == "i"
        if interactive:
            map_type_end -= 1
        months = None
        if fields[map_type_end - 1] == "12m":
            months = 12
            map_type_end -= 1
        elif fields[map_type_end - 1] == "6m":
            months = 6
            map_type_end -= 1
        map_type = "-".join(fields[1:map_type_end])
        if subtype == "h3n":
            inferred_subtype = "h3"
            assay = "neut"
        else:
            inferred_subtype = subtype
            assay = "hi"
        return {"raw_subtype": subtype, "subtype": inferred_subtype, "assay": assay, "map": map_type, "lab": lab, "interactive": interactive, "months": months}

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
