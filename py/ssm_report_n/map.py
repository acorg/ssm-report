import sys, os, json, subprocess
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

from .charts import get_chart

# ======================================================================

def make_map(output_dir, prefix, virus_type, assay, mod, force):
    settings = json.load(open("{}-{}.json".format(virus_type, assay)))
    for lab in settings["labs"]:
        chart_filename = get_chart(virus_type=virus_type, assay=assay, lab=lab)
        module_logger.info("{}\nINFO:{} {} {} {} {}\nINFO: {}".format("*"* 70, " " * 30, lab, virus_type.upper(), assay.upper(), mod, " "* 93))
        subprocess.check_call("ad map-draw --db-dir db -v '{}' '{}'".format(chart_filename, "--open"), shell=True)

    #     make_map(output_dir=output_dir, prefix=prefix, virus_type=virus_type, assay=assay, mods=mods, report_settings=report_settings(), map_settings=map_sets,
    #                  seqdb_file=self._seqdb_file(), information_meeting=information_meeting, force=self._force)
    # p

# ----------------------------------------------------------------------

def make_map_information(output_dir, prefix, virus_type, assay, mod):
    raise NotImplementedError()

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
