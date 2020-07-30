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
        mer = self.tree()
        return Path(mer).exists()

    def _settings(self):
        if self.subtype == "h3":
            return f"-s vr.mapi -s {self.subtype}.mapi -s {self.subtype}-{self.assay}.mapi -s serology.mapi -s vaccines.mapi"
        else:
            return f"-s vr.mapi -s {self.subtype}.mapi -s serology.mapi -s vaccines.mapi"

    def _subtype_key(self):
        return f"{self.subtype} {self.assay if self.assay else 'hi'}"


# ======================================================================

def makers(subtypes=["h1", "h3", "bvic", "byam"], **options):
    return [mk for mk in (maker(subtype=subtype, **options) for subtype in subtypes) if mk.tree_exists()]

# ======================================================================

sTalSettings = """{   "_": "-*- js-indent-level: 4 -*-",
    "tal": [
        "clades-whocc",
        {"?N": "nodes", "select": {"top-cumulative-gap": 2.0, "report": true}, "apply": {"?hide": true, "tree-edge-line-color": "red"}}
    ]
}
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
