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
            print(f"information-{subtype}-maps")
            print(f"information-{subtype}-maps-i")
            for map_type in sSetup[subtype]["maps"]:
                print(f"{subtype}-{map_type}")
                if map_type in ["tree"]:
                    print(f"{subtype}-{map_type}-i")
                    print(f"{subtype}-{map_type}-cumulative")
                    print(f"{subtype}-{map_type}-first-last-leaves")
                    print(f"information-{subtype}-{map_type}")
                else:
                    for lab in sSetup.get(subtype, {}).get("labs", []):
                        print(f"{subtype}-{map_type}-{lab}")
                        if map_type not in ["ts"]:
                            print(f"{subtype}-{map_type}-i-{lab}")
        for lab in sSetup.get(subtype, {}).get("labs", []):
            print(f"{subtype}-names-{lab}")

    for command_name in sSetup.get("commands", {}):
        print(command_name)

    for command_name in ["get-merges", "get-hidb-seqdb", "geo-stat", "geo", "stat", "report", "report-abbreviated", "addendum-1", "addendum-2", "addendum-3", "addendum-4", "addendum-5", "addendum-6"]:
        print(command_name)

# ----------------------------------------------------------------------

def init_dir(dir):
    sRootDir.joinpath(dir).mkdir()
    os.chdir(sRootDir.joinpath(dir))
    from . import init
    init.copy_templates(maker_version="2020-01")
    init.init_git()
    init.get_hidb_seqdb()
    init.init_dirs()
    init.init_settings()
    subprocess.check_call(["emacsclient", "-n", "README.org"])
    subprocess.check_call(["emacsclient", "-n", "setup.json"])

# ----------------------------------------------------------------------

def do(command_name):
    Commands().do(command_name)

# ----------------------------------------------------------------------

class Commands:

    def do(self, command_name):
        command = self.parse_cmd(command_name)
        print(command)
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

    def get_hidb_seqdb(self, **args):
        from . import init
        init.get_hidb_seqdb()

    def geo_stat(self, **args):
        self.stat(**args)
        self.geo(**args)

    def geo(self, **args):
        from .geographic import make_geographic
        make_geographic(geo_dir=Path("geo"), db_dir=self._db_dir(), force=True)

    def stat(self, **args):
        from .stat import make_stat
        make_stat(stat_dir=Path("stat"), hidb_dir=self._db_dir(), force=True)

    def get_merges(self, **args):
        from acmacs_whocc import get_recent_merges
        get_recent_merges(Path("merges"))

    def tree(self, subtype, interactive, information, report_cumulative=False, **args):
        from .signature_page import tree_make
        tree_dir = Path("tree")
        if not information:
            tree_make(subtype=subtype, tree_dir=tree_dir, seqdb=self._db_dir().joinpath("seqdb.json.xz"), interactive=interactive, report_cumulative=report_cumulative)
        else:
            from .signature_page import tree_make_information_settings
            tree_make_information_settings(virus_type=subtype, tree_dir=tree_dir, output_dir=Path("information"))
            tree_make(subtype=subtype, tree_dir=tree_dir, seqdb=self._seqdb_file(), output_dir=Path("information"), settings_infix="information")

    def tree_cumulative(self, **args):
        self.tree(report_cumulative=True, **args)

    def tree_first_last_leaves(self, subtype, **args):
        from .signature_page import tree_report_first_last_leaves
        tree_report_first_last_leaves(subtype=subtype, tree_dir=Path("tree"), seqdb=self._db_dir().joinpath("seqdb.json.xz"))

    def maps(self, raw_subtype, information, subtype, assay, interactive, open_image=True, **args):
        if not information:
            sep = "=" * 100
            for command_name in sSetup[raw_subtype]["maps"]:
                if not command_name.startswith("tree") and not command_name.startswith("sp"):
                    print(f"{sep}\n{command_name}\n{sep}\n")
                    self.do(f"{raw_subtype}-{command_name}")
        else:
            from .map import make_map_information
            make_map_information(virus_type=subtype, assay=assay, output_dir=Path("information"), interactive=interactive, open_image=open_image)

    def names(self, subtype, assay, lab, **args):
        from .charts import get_chart
        chart = get_chart(virus_type=subtype, assay=assay, lab=lab)
        print(f"chart-names {chart}\n")
        subprocess.check_call(["chart-names", chart])

    def clade(self, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .map import make_map
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        if months:
            mod = f"clade-{months}m"
        else:
            mod = "clade"
        make_map(prefix=mod, virus_type=subtype, assay=assay, lab=labs, mod=mod, output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and labs and len(labs) == 1, force=True)

    def aa_156(self, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .map import make_map
        if months:
            mod = f"aa-156-{months}m"
        else:
            mod = f"aa-156"
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_map(prefix=mod, virus_type=subtype, assay=assay, lab=labs, mod=mod, output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and labs and len(labs) == 1, force=True)

    def N_gly_197(self, subtype, assay, lab, interactive, open_image=True, **args):
        "/syn/eu/ac/results/ssm/2020-0123-tc2/custom/bvic-197/README.org"
        from .map import make_map
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_map(prefix="N-gly-197", virus_type=subtype, assay=assay, lab=labs, mod="N-gly-197", output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and labs and len(labs) == 1, force=True)

    def serology(self, subtype, assay, lab, interactive, open_image=True, **args):
        from .map import make_map
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_map(prefix="serology", virus_type=subtype, assay=assay, lab=labs, mod="serology", output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and labs and len(labs) == 1, force=True)

    def serology_aa_156(self, subtype, assay, lab, interactive, open_image=True, **args):
        from .map import make_map
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_map(prefix="serology-aa-156", virus_type=subtype, assay=assay, lab=labs, mod="serology-aa-156", output_dir=self._output_path(subtype=subtype, assay=assay), interactive=interactive, open_image=open_image and labs and len(labs) == 1, force=True)

    def ts(self, subtype, assay, lab, open_image=False, **args):
        from .map import make_ts
        labs = self._get_lab(subtype=subtype, assay=assay, lab=lab)
        make_ts(virus_type=subtype, assay=assay, lab=labs, output_dir=self._output_path(subtype=subtype, assay=assay), force=True, dot_size=sDotSize, start=sSetup["time-series"]["date"]["start"], end=sSetup["time-series"]["date"]["end"], period=sSetup["time-series"]["period"], teleconference=sReport["cover"]["teleconference"], previous=sReport["previous"])

    def sp(self, raw_subtype, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .signature_page import signature_page_make, signature_page_source_dir_init, signature_page_output_dir_init
        labs = self._get_lab(subtype=raw_subtype, assay=assay, lab=lab)
        sp_dir = Path("sp")
        signature_page_source_dir_init(sp_dir)
        signature_page_output_dir_init(sp_dir)
        for lab in labs:
            signature_page_make(virus_type=subtype, assay=assay, lab=lab, sp_source_dir=sp_dir, sp_output_dir=sp_dir, tree_dir=Path("tree"), merge_dir=Path("merges").resolve(), seqdb=self._seqdb_file(), interactive=interactive)

    def spc(self, raw_subtype, subtype, assay, lab, interactive, months, open_image=True, **args):
        from .signature_page import signature_page_make, signature_page_source_dir_init, signature_page_output_dir_init
        labs = self._get_lab(subtype=raw_subtype, assay=assay, lab=lab)
        sp_dir = Path("spc")
        signature_page_source_dir_init(sp_dir)
        signature_page_output_dir_init(sp_dir)
        for lab in labs:
            signature_page_make(virus_type=subtype, assay=assay, lab=lab, serum_circles=True, orig_sp_source_dir=Path("sp"), sp_source_dir=sp_dir, sp_output_dir=sp_dir, tree_dir=Path("tree"), merge_dir=Path("merges").resolve(), seqdb=self._seqdb_file(), interactive=interactive)

    def _output_path(self, subtype, assay):
        return Path(f"{subtype[:2]}-{assay}")

    def report(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def report_abbreviated(self):
        from .report import make_report_abbreviated
        make_report_abbreviated(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def addendum_1(self, **args):
        from .report import make_signature_page_addendum_interleave
        make_signature_page_addendum_interleave(source_dirs=[Path("sp"), Path("spc")], output_dir=Path("report"), title="Addendum 1 (integrated genetic-antigenic analyses)", output_name="sp-spsc-addendum", T_SerumCirclesDescriptionEggCell=True)

    def addendum_2(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-2", report_settings_file="report-addendum-2.json")

    def addendum_3(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-3", report_settings_file="report-addendum-3.json")

    def addendum_4(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-4", report_settings_file="report-addendum-4.json")

    def addendum_5(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-5", report_settings_file="report-addendum-5.json")

    def addendum_6(self, **args):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-6", report_settings_file="report-addendum-6.json")

    def _db_dir(self):
        return Path("db").resolve()

    def _seqdb_file(self):
        return self._db_dir().joinpath("seqdb.json.xz")

    def _get_lab(self, subtype, assay, lab, **args):
        if lab:
            if isinstance(lab, str):
                return [lab]
            else:
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
        if fields[0] == "information":
            information = True
            del fields[0]
        else:
            information = False
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
        elif subtype == "bvic":
            inferred_subtype = "bv"
            assay = "hi"
        elif subtype == "byam":
            inferred_subtype = "by"
            assay = "hi"
        else:
            inferred_subtype = subtype
            assay = "hi"
        return {"raw_subtype": subtype, "subtype": inferred_subtype, "assay": assay, "map": map_type, "lab": lab, "interactive": interactive, "months": months, "information": information}

# ======================================================================
