import sys, os, subprocess, json
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from . import report, map
from .error import Error

# ----------------------------------------------------------------------

def __get_merges(command, *r, **a): get_merges()
def __get_hidb(command, *r, **a): get_hidb()
def __stat_geo(command, *r, **a): stat_geo()

sCommands = {
    "~report": report.make_report,
    "~addendum-1": report.make_addendum_1,
    "~addendum-2": report.make_addendum_2,
    "~addendum-3": report.make_addendum_3,
    "~addendum-4": report.make_addendum_4,
    "~addendum-5": report.make_addendum_5,
    "~addendum-6": report.make_addendum_6,
    "~get-merges": __get_merges,
    "~get-hidb": __get_hidb,
    "~stat-geo": __stat_geo,
    }

from report import maps
for map_maker in maps(sys.modules[__name__]):
    if isinstance(map_maker, list):
        for mm in map_maker:
            sCommands[mm.command_name_for_helm()] = mm
    else:
        sCommands[map_maker.command_name_for_helm()] = map_maker

# ----------------------------------------------------------------------

def process(command, interactive=False):
    cmd = sCommands.get(command)
    if not cmd:
        raise Error(f"unknown command {command}")
    cmd(command, interactive=interactive)

# ----------------------------------------------------------------------

def stat_geo():
    from .stat import make_stat
    vr_data = json.load(Path("vr.mapi").open())
    start_date = vr_data["init"][0]["time-series-start"]
    if len(start_date) == 7:
        start_date = f"{start_date}-01"
    end_date = vr_data["init"][0]["time-series-end"]
    if len(end_date) == 7:
        end_date = f"{end_date}-01"

    make_stat(output_dir=Path("stat"), hidb_dir=Path(os.environ["ACMACSD_ROOT"], "data"), start=start_date, end=end_date, previous_stat_dir=Path("previous/stat"), make_all_names=False, make_tabs=False, make_csv=False, make_webpage=True)
    subprocess.check_call("open stat/index.html", shell=True)

    from .geographic import make_geographic, make_geographic_settings
    geo_dir = Path("geo")
    geo_dir.mkdir(exist_ok=True)
    make_geographic_settings(settings_dir=geo_dir, start_date=start_date, end_date=end_date, force=False)
    make_geographic(geo_dir=geo_dir, settings_dir=geo_dir, force=True)
    subprocess.check_call(f"pdf-combine {geo_dir}/H1-*.pdf {geo_dir}/H3-*.pdf {geo_dir}/B-*.pdf {geo_dir}/all.pdf && open {geo_dir}/all.pdf", shell=True)

# ----------------------------------------------------------------------

def get_merges():
    output_dir = Path("merges")
    output_dir.mkdir(exist_ok=True)
    from acmacs_whocc import acmacs
    acmacs.get_recent_merges(output_dir)

# ----------------------------------------------------------------------

def get_hidb():
    subprocess.check_call('ssh albertine "whocc-update-ace-store && whocc-hidb5-update" && hidb-get-from-albertine', shell=True)

# ----------------------------------------------------------------------

def list_for_helm():
    print("\n".join(sorted(sCommands)))

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
