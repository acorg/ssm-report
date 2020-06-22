import subprocess
from pathlib import Path

# ======================================================================

def make_map(command_name, interactive, *r, **a):
    subtype, assay, lab, map_name = command_name.split("-", maxsplit=3)
    subtype_short = subtype[:2]
    open_pdf = True
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)

    merge = f"merges/{lab}-{subtype_short}-{assay}.ace"

    if map_name == "ts":        # no output pdf for ts, see vr.mapi "vr:ts"
        pdf = "/"
    else:
        pdf = f"{output_dir}/{subtype}-{assay}-{lab}-{map_name}.pdf"

    if subtype == "h3":
        settings = f"-s vr.mapi -s {subtype}.mapi -s {subtype}-{assay}.mapi -s serology.mapi -s vaccines.mapi"
    else:
        settings = f"-s vr.mapi -s {subtype}.mapi -s serology.mapi -s vaccines.mapi"

    cmd = f"mapi -a vr:{map_name} {settings} {merge} {pdf}"
    if open_pdf:
        cmd += " --open"
    if interactive:
        cmd += " -i"
    #print(f"make_map {command_name} -> {subtype}, {assay}, {lab}, {map_name}")
    print(cmd)
    subprocess.check_call(cmd, shell=True)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
