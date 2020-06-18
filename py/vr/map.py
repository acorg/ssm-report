import subprocess

# ======================================================================

def make_map(command_name):
    subtype, assay, lab, map_name = command_name.split("-", maxsplit=4)
    print(f"make_map {command_name} -> {subtype}, {assay}, {lab}, {map_name}")
    
# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
