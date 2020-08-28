import subprocess
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)

# ======================================================================

class maker:

    def __init__(self, subtype, **options):
        self.subtype = subtype
        self.options = options

    def command_name_for_helm(self):
        return f"{self.subtype}-tree"

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=Path("tree"), *r, **a):
        output_dir.mkdir(exist_ok=True)
        source_tjz = output_dir.joinpath(f"{self.subtype}.tjz")
        txt = output_dir.joinpath(f"{self.subtype}.tree.txt")
        if not txt.exists():
            cmd = f"tal {source_tjz} {txt}"
            print(cmd)
            subprocess.check_call(cmd, shell=True)
        tal_settings = output_dir.joinpath(f"{self.subtype}.tree.tal")
        pdf = output_dir.joinpath(f"{self.subtype}.tree.pdf")
        if not tal_settings.exists():
            with tal_settings.open("w") as fd:
                fd.write(sTalSettings)
        cmd = f"tal -s {tal_settings} {source_tjz} {pdf}"
        if open_pdf:
            # cmd += " --preview 100.0.834.1000"
            cmd += " --open"
        if interactive:
            cmd += " -i"
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def tree(self):
        return f"tree/{self.subtype}.tjz"

    def tree_exists(self):
        return Path(self.tree()).exists()

    def _settings(self):
        if self.subtype == "h3":
            return f"-s vr.mapi -s {self.subtype}.mapi -s {self.subtype}-{self.assay}.mapi -s serology.mapi -s vaccines.mapi"
        else:
            return f"-s vr.mapi -s {self.subtype}.mapi -s serology.mapi -s vaccines.mapi"

    def _subtype_key(self):
        return f"{self.subtype} {self.assay if self.assay else 'hi'}"


# ----------------------------------------------------------------------

def makers(subtypes=["h1", "h3", "bvic", "byam"], **options):
    return [mk for mk in (maker(subtype=subtype, **options) for subtype in subtypes) if mk.tree_exists()]

# ======================================================================

class sp_maker:

    def __init__(self, subtype, lab, assay, sp="sp"):
        self.subtype = subtype
        self.lab = lab
        self.assay = assay
        if self.assay:
            self.assay_infix = f"-{self.assay}"
        else:
            self.assay_infix = ""
        self.sp = sp

    def command_name_for_helm(self):
        return f"{self.subtype}{self.assay_infix}-{self.lab}-{self.sp}"

    # tal -s ../vr.mapi -s ../h3.mapi -s ../h3-hint.mapi -s ../serology.mapi -s ../vaccines.mapi -s h3.tree.tal -s sp.tal -s h3.sp.tal -s h3.sp.cdc-hint.tal --chart ../merges/cdc-h3-hint.ace h3.tjz h3.cdc-hint.sp.pdf --open
    # tal -s ../vr.mapi -s ../h1.mapi -s ../h1.mapi -s ../serology.mapi -s ../vaccines.mapi -s h1.tree.tal -s sp.tal -s h1.sp.tal -s h1.sp.cdc.tal --chart ../merges/cdc-h1-hi.ace h1.tjz h1.cdc.sp.pdf --open
    # tal -s ../vr.mapi -s ../h1.mapi -s ../h1.mapi -s ../serology.mapi -s ../vaccines.mapi -s h1.tree.tal -s sp.tal -s spc.tal -s h1.sp.tal -s h1.sp.cdc.tal --chart ../merges/cdc-h1-hi.ace h1.tjz h1.cdc.spc.pdf --open

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=Path("sp"), *r, **a):
        source_tjz = output_dir.joinpath(f"{self.subtype}.tjz")
        tal_settings = output_dir.joinpath(f"{self.subtype}.tree.tal")
        chart = self.merge()
        pdf = output_dir.joinpath(f"{self.subtype}.{self.lab}{self.assay_infix}.{self.sp}.pdf")
        cmd = f"tal -s vr.mapi -s {self.subtype}.mapi"
        if self.assay:
            cmd += f" -s {self.subtype}-{self.assay}.mapi"
        cmd += f" -s serology.mapi -s vaccines.mapi -s sp/{self.subtype}.tree.tal -s sp/sp.tal"
        if self.sp == "spc":
            cmd += " -s sp/spc.tal"
        cmd += f" -s sp/{self.subtype}.sp.tal -s sp/{self.subtype}.sp.{self.lab}{self.assay_infix}.tal"
        cmd += f" --chart {chart} {source_tjz} {pdf}"
        if open_pdf:
            # cmd += " --preview 100.0.834.1000"
            cmd += " --open"
        if interactive:
            cmd += " -i"
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def tree(self):
        return f"sp/{self.subtype}.tjz"

    def tree_exists(self):
        return Path(self.tree()).exists()

    def merge(self):
        return f"merges/{self.lab}-{self.subtype[:2]}-{self.assay or 'hi'}.ace"

    def merge_exists(self):
        return Path(self.merge()).exists()

# ----------------------------------------------------------------------

def makers_sp(subtype, labs, assay):
    return [mk for mk in (sp_maker(subtype=subtype, lab=lab, assay=assay, sp=sp) for lab in labs for sp in ["sp", "spc"]) if mk.tree_exists() and mk.merge_exists()]

# ======================================================================

sTalSettings = """{   "_": "-*- js-indent-level: 4 -*-",
    "init": [
        {"?N": "set", "report-cumulative-output": "-"}
    ],

    "tal": [
        {"?N": "margins", "left": 0.015},
        "clades-whocc",
        {"?N": "nodes", "select": {"top-cumulative-gap": 2.0, "report": true}, "apply": {"?hide": true, "tree-edge-line-color": "red"}}
        {"?N": "nodes", "select": {"cumulative >=": 0.035, "report": true}, "apply": {"?hide": true, "tree-edge-line-color": "red"}},
        {"N": "time-series", "?start": "2017-01", "?slot": {"width": 0.005}},
        {"N": "clades", "?slot": {"width": 0.007}, "?width-to-height-ratio": 0.045,
         "?all_clades": {"label": {"scale": 1.4}},
         "per_clade": [
         ]
        },
        "eu-aa-transitions",
        "?hz"
    ],

    "eu-aa-transitions": [
        {"N": "draw-aa-transitions", "?minimum_number_leaves_in_subtree": 0.05,
         "per_node": [
         ]
        }
    ],

    "hz": [
        {"N": "hz-sections", "report": true,
         "sections": [
             {"id": "G133R",       "first": "B/ARGENTINA/2863/2019_OR_h50DEF5B1", "last": "B/KANAGAWA/AC1886/2019_MDCK0/MDCK1_hF636BAFA", "?label": "", "show": true},
         ]
        }
    ],
}
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
