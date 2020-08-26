import sys, os, subprocess, json, datetime
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from . import report, map, tree
from .error import Error

# ----------------------------------------------------------------------

def __get_merges(command, *r, **a): get_merges()
def __get_hidb(command, *r, **a): get_hidb()
def __stat_geo(command, *r, **a): stat_geo()
def __sy(command, *r, **a): sy()

sCommands = {
    "~report": report.make_report,
    "~report-upload": report.make_report_and_upload,
    "~addendum-1": report.make_addendum_1,
    "~addendum-2": report.make_addendum_2,
    "~addendum-3": report.make_addendum_3,
    "~addendum-4": report.make_addendum_4,
    "~addendum-5": report.make_addendum_5,
    "~addendum-6": report.make_addendum_6,
    "~get-merges": __get_merges,
    "~get-hidb": __get_hidb,
    "~stat-geo": __stat_geo,
    "~sy": __sy,
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

class vr_data:

    def __init__(self):
        vr_data = json.load(Path("vr.mapi").open())
        self.start_date = vr_data["init"][0]["time-series-start"]
        self.end_date = vr_data["init"][0]["time-series-end"]
        if len(self.start_date) == 7:
            self.start_date = f"{self.start_date}-01"
        if len(self.end_date) == 7:
            self.end_date = f"{self.end_date}-01"
        self.start_month_year = datetime.date.fromisoformat(self.start_date).strftime("%B %Y")
        self.end_month_year = (datetime.date.fromisoformat(self.end_date) - datetime.timedelta(days=1)).strftime("%B %Y")

# ----------------------------------------------------------------------

def stat_geo():
    from .stat import make_stat
    data = vr_data()
    make_stat(output_dir=Path("stat"), hidb_dir=Path(os.environ["ACMACSD_ROOT"], "data"), start=data.start_date, end=data.end_date, previous_stat_dir=Path("previous/stat"), make_all_names=False, make_tabs=False, make_csv=False, make_webpage=True)
    subprocess.check_call("open stat/index.html", shell=True)

    from .geographic import make_geographic, make_geographic_settings
    geo_dir = Path("geo")
    geo_dir.mkdir(exist_ok=True)
    make_geographic_settings(settings_dir=geo_dir, start_date=data.start_date, end_date=data.end_date, force=False)
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

# ----------------------------------------------------------------------

def sy():
    subprocess.check_call("./sy", shell=True)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
