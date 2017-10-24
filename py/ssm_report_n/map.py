import sys, os, json, subprocess
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

from .charts import get_chart

# ======================================================================

sLabDisplayName = {"CDC": "CDC", "CNIC": "CNIC", "NIMR": "Crick", "NIID": "NIID", "MELB": "VIDRL"}

sApplyFor = {
    "pre": [
        "{lab}_pre",
        "{lab}_flip",
        "{lab}_rotate",
        "{lab}_viewport",
        "all_grey",
        "egg",
        ],
    "post": [
        "{lab}_mid",
        "{lab}_vaccines",
        "{lab}_post",
        ],
    "clade": [
        "clades",
    ]
}

sTitleFor = {
    "clade": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay} by clade",
        },
    },
}

# ======================================================================

def make_map(output_dir, prefix, virus_type, assay, mod, force):
    s1_filename = Path("{}-{}.json".format(virus_type, assay)).resolve()
    settings = json.load(s1_filename.open())
    for lab in settings["labs"]:
        module_logger.info("{}\nINFO:{} {} {} {} {}\nINFO: {}".format("*"* 70, " " * 30, lab, virus_type.upper(), assay.upper(), mod, " "* 93))
        output_prefix = prefix + "-" + lab.lower()

        s2_filename = output_dir.joinpath(output_prefix + ".settings.json")
        pre, post = make_pre_post(virus_type=virus_type, assay=assay, mod=mod, lab=lab)
        json.dump({"apply": pre + sApplyFor[mod] + post}, s2_filename.open("w"), indent=2)

        script_filename = output_dir.joinpath(output_prefix + ".sh")
        script_filename.open("w").write("#! /bin/bash\nexec ad map-draw --db-dir {pwd}/db -v -s '{s1}' -s '{s2}' '{chart}' '{output}' --open\n".format(
            s1=s1_filename, s2=s2_filename,
            pwd=os.getcwd(), chart=get_chart(virus_type=virus_type, assay=assay, lab=lab), output=output_dir.joinpath(output_prefix + ".pdf")))
        script_filename.chmod(0o700)
        subprocess.check_call(str(script_filename))

# ----------------------------------------------------------------------

def make_pre_post(virus_type, assay, mod, lab):
    title = {
        "N": "title",
        "background": "transparent",
        "border_width": 0,
        "text_size": 24,
        "font_weight": "bold",
        "display_name": [sTitleFor[mod][virus_type][assay].format(lab=sLabDisplayName[lab], virus_type=virus_type.upper(), assay=assay.upper())],
    }
    return (
        [title] + [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab) for e in sApplyFor["pre"]],
        [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab) for e in sApplyFor["post"]]
        )

# ----------------------------------------------------------------------

def make_map_information(output_dir, prefix, virus_type, assay, mod):
    raise NotImplementedError()

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
