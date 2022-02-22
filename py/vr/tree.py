import sys, subprocess
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from .merge import merge_finder

# ======================================================================

class maker:

    def __init__(self, subtype, infix, **options):
        self.subtype = subtype
        self.infix = infix
        self.options = options

    def command_name_for_helm(self):
        if self.options.get("info"):
            return f"info-{self.subtype}-tree"
        elif self.infix:
            return f"{self.subtype}-tree-{self.infix}"
        else:
            return f"{self.subtype}-tree"

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=None, *r, **a):
        tree_dir = Path("tree")
        info = self.options.get("info")
        if not output_dir:
            if info:
                output_dir = Path("info")
            else:
                output_dir = tree_dir
        output_dir.mkdir(exist_ok=True)
        source_tjz = self.tree()
        if self.infix:
            tal_settings = next(tree_dir.glob(f"{self.subtype}.{self.infix}*.tree.tal"))
        else:
            tal_settings = tree_dir.joinpath(f"{self.subtype}.tree.tal")
        if not tal_settings.exists():
            with tal_settings.open("w") as fd:
                fd.write(sTalSettings)
        pdf = output_dir.joinpath(tal_settings.name).with_suffix(".pdf")
        if info:
            info_settings = output_dir.joinpath(f"{self.subtype}.info.tal")
            if not info_settings.exists():
                with info_settings.open("w") as fd:
                    fd.write(sTalInfoSettings)
            cmd = f"tal -s {tal_settings} -s {info_settings} {source_tjz} {pdf}"
        else:                   # not info
            txt = tal_settings.with_suffix(".txt")
            if not txt.exists():
                cmd = f"tal -s {tal_settings} {source_tjz} {txt}"
                print(cmd)
                subprocess.check_call(cmd, shell=True)
            cmd = f"tal -s {tal_settings} {source_tjz} {pdf}"
        if open_pdf:
            # cmd += " --preview 100.0.834.1000"
            cmd += " --open"
        if interactive:
            cmd += " -i"
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def tree(self):
        if self.infix:
            print(f">>>> glob {self.subtype}.{self.infix}*.tjz", file=sys.stderr)
            if files := list(Path("tree").glob(f"{self.subtype}.{self.infix}*.tjz")):
                return files[0]
            else:
                return ""
        else:
            return f"tree/{self.subtype}.tjz"

    def tree_exists(self):
        return Path(self.tree()).exists()

    # def _settings(self):
    #     if self.subtype == "h3":
    #         return f"-s vr.mapi -s {self.subtype}.mapi -s {self.subtype}-{self.assay}.mapi -s serology.mapi -s vaccines.mapi"
    #     else:
    #         return f"-s vr.mapi -s {self.subtype}.mapi -s serology.mapi -s vaccines.mapi"

    def _subtype_key(self):
        return f"{self.subtype} {self.assay if self.assay else 'hi'}"


# ----------------------------------------------------------------------

def makers(subtypes=["h1", "h3", "bvic", "byam"], **options):
    return [mk for mk in (maker(subtype=subtype, infix=infix, **options) for subtype in subtypes for infix in ["after", None]) if mk.tree_exists()]

def info_makers(subtypes=["h1", "h3", "bvic", "byam"], **options):
    return [mk for mk in (maker(subtype=subtype, infix=infix, info=True, **options) for subtype in subtypes for infix in ["after", None]) if mk.tree_exists()]

# ======================================================================

class sp_maker (merge_finder):

    def __init__(self, subtype, lab, assay, rbc, sp="sp"):
        super().__init__(subtype=subtype, assay=assay, rbc=rbc)
        self.lab = lab
        if self.assay and self.subtype == "h3":
            self.assay_infix = f"-{self.assay}"
        else:
            self.assay_infix = ""
        self.sp = sp

    def command_name_for_helm(self):
        if isinstance(self.lab, str):
            return f"{self.subtype}{self.assay_infix}-{self.lab}-{self.sp}"
        else:
            return f"{self.subtype}{self.assay_infix}-spx"

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=Path("sp"), *r, **a):
        if isinstance(self.lab, str):
            self.run_one(lab=self.lab, sp=self.sp, interactive=interactive, open_pdf=open_pdf, output_dir=output_dir)
        else:
            for lab in self.lab:
                for sp in self.sp:
                    print(f"\n> ======================================================================================================================================================\n> {self.subtype}{self.assay_infix} {lab} {sp}\n> ======================================================================================================================================================\n\n")
                    self.run_one(lab=lab, sp=sp, interactive=False, open_pdf=False, output_dir=output_dir)

    def run_one(self, lab, sp, interactive, open_pdf, output_dir):
        source_tjz = output_dir.joinpath(f"{self.subtype}.tjz")
        tal_settings = output_dir.joinpath(f"{self.subtype}.tree.tal")
        chart = self.merge(lab=lab)
        pdf = output_dir.joinpath(f"{self.subtype}.{lab}{self.assay_infix}.{sp}.pdf")
        cmd = f"tal -s vr.mapi -s {self.subtype}.mapi"
        if self.assay and self.subtype == "h3":
            cmd += f" -s {self.subtype}-{self.assay}.mapi"
        cmd += f" -s serology.mapi -s vaccines.mapi -s sp/{self.subtype}.tree.tal -s sp/sp.tal"
        if sp == "spc":
            cmd += " -s sp/spc.tal"
        cmd += f" -s sp/{self.subtype}.sp.tal -s sp/{self.subtype}.sp.{lab}{self.assay_infix}.tal"
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

# ----------------------------------------------------------------------

def makers_sp(subtype, labs, assay, rbc):
    # print(f"makers_sp {subtype} {labs} {assay} {rbc}")
    # for lab in labs:
    #     mk = sp_maker(subtype=subtype, lab=lab, assay=assay, rbc=rbc, sp='sp')
    #     print(f"    {lab} {mk.merge_exists(lab=mk.lab)} {mk.tree()} {mk.tree_exists()}")
    makers = [mk for mk in (sp_maker(subtype=subtype, lab=lab, assay=assay, rbc=rbc, sp=sp) for lab in labs for sp in ["sp", "spc"]) if mk.tree_exists() and mk.merge_exists(lab=mk.lab)]
    spx_maker = sp_maker(subtype=subtype, lab=labs, assay=assay, rbc=rbc, sp=["sp", "spc"])
    if spx_maker.tree_exists():
        makers.append(spx_maker)
    return makers

# ======================================================================

sTalSettings = """{
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
         "per-clade": [
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

sTalInfoSettings = """{
    "tal-default": [
        {"N": "canvas", "height": "$canvas-height"},
        {"N": "ladderize", "method": "$ladderize-method"},
        {"N": "tree", "color-by": "continent", "width-to-height-ratio": 0.4, "legend": {"show": true}, "debug-outline": false},
        {"N": "nodes", "select": {"all": true}, "apply": {"tree-label-scale": -1, "?": "use -1 to hide label"}},
        {"N": "nodes", "select": {"all-and-intermediate": true}, "apply": {"tree-edge-line-width": 45}},
        {"N": "time-series", "start": "2019-03", "?end": "2020-07", "color-by": "continent", "slot": {"width": 0.0085, "label": {"scale": 0.7, "rotation": "clockwise"}}, "color-scale": {"show": false}, "report": "$report-time-series-output"},
        {"N": "gap", "id": "gap-right", "width-to-height-ratio": 0.02}
    ],

    "? tal": [
        {"N": "margins", "left": 0.01},
        {"N": "title", "show": false},
        {"N": "tree", "width-to-height-ratio": 0.4},
        {"N": "nodes", "select": {"all-and-intermediate": true}, "apply": {"tree-edge-line-width": 45}},
        {"N": "draw-aa-transitions", "show": false},
        {"?N": "time-series", "start": "2018-06", "end": "2020-07", "slot": {"width": 0.0065, "label": {"scale": 0.7, "rotation": "clockwise"}}},
        {"N": "gap", "id": "gap-right", "width-to-height-ratio": 0.07},
        "hz"
    ]
}
"""

# ======================================================================
