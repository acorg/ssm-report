import sys, os, subprocess, json, datetime
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from . import report, map, tree
from .error import Error

# ----------------------------------------------------------------------

def __get_merges(command, *r, **a): get_merges()
def __get_merge_from_chain(command, *r, **a): get_merge_from_chain(*r)
def __get_hidb(command, *r, **a): get_hidb()
def __stat_geo(command, *r, **a): stat_geo()
def __geo(command, *r, **a): geo()
def __stat(command, *r, **a): stat()
def __sy(command, *r, **a): sy()

sCommands = {
    "~report": report.make_report,
    "~report-b": report.make_report_b,
    "~report-h1": report.make_report_h1,
    "~report-h3": report.make_report_h3,
    "~report-upload": report.make_report_and_upload,
    "~addendum-1": report.make_addendum_1,
    "~addendum-1-b": report.make_addendum_1_b,
    "~addendum-1-h1": report.make_addendum_1_h1,
    "~addendum-1-h3": report.make_addendum_1_h3,
    "~addendum-2": report.make_addendum_2,
    "~addendum-3": report.make_addendum_3,
    "~addendum-4": report.make_addendum_4,
    "~addendum-5": report.make_addendum_5,
    "~addendum-6": report.make_addendum_6,
    "~get-merges": __get_merges,
    "!get-merge-from-chain": __get_merge_from_chain, # ! - secondary command, do not list for helm
    "~get-hidb": __get_hidb,
    "~stat-geo": __stat_geo,
    "~stat": __stat,
    "~geo": __geo,
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
    command, *args = command.split()
    cmd = sCommands.get(command)
    if not cmd:
        raise Error(f"unknown command {command}")
    cmd(command, interactive=interactive, *args)

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
    stat()
    geo()

def stat():
    from .stat import make_stat
    data = vr_data()
    make_stat(output_dir=Path("stat"), hidb_dir=Path(os.environ["ACMACSD_ROOT"], "data"), start=data.start_date, end=data.end_date, previous_stat_dir=Path("previous/stat"), make_all_names=False, make_tabs=False, make_csv=False, make_webpage=True)
    subprocess.check_call("open stat/index.html", shell=True)

def stat_geo():
    from .geographic import make_geographic, make_geographic_settings
    data = vr_data()
    geo_dir = Path("geo")
    geo_dir.mkdir(exist_ok=True)
    make_geographic_settings(settings_dir=geo_dir, start_date=data.start_date, end_date=data.end_date, force=False)
    make_geographic(geo_dir=geo_dir, settings_dir=geo_dir, force=True)
    subprocess.check_call(f"pdf-combine {geo_dir}/H1-*.pdf {geo_dir}/H3-*.pdf {geo_dir}/B-*.pdf {geo_dir}/all.pdf && open {geo_dir}/all.pdf", shell=True)

# ----------------------------------------------------------------------

def get_merges():
    subprocess.check_call(["ssh", "i19", "ad-run", "ACMACSD_ROOT=/syn/eu/AD.chain", "whocc-report-chains"])

def get_merge_from_chain(srl, remote_filename):
    merge_dir = Path("merges")
    merge_dir.mkdir(exist_ok=True)
    target = merge_dir.joinpath(f"{srl}.chain.ace")
    subprocess.check_call(["rsync", "-v", f"i19:{remote_filename}", str(target)])
    print("\n")
    subprocess.check_call(["chart-info", str(target)])
    target_main = merge_dir.joinpath(f"{srl}.ace")
    if not target_main.exists():
        target_main.symlink_to(target.name)

# def get_merges():
#     output_dir = Path("merges")
#     output_dir.mkdir(exist_ok=True)
#     from acmacs_whocc import get_recent_merges
#     get_recent_merges(output_dir)

# ----------------------------------------------------------------------

def get_hidb():
    subprocess.check_call('ssh albertine "whocc-update-ace-store && whocc-hidb5-update" && hidb-get-from-albertine', shell=True)

# ----------------------------------------------------------------------

def list_for_helm():
    # print("\n".join(sorted(sCommands)))

    def key(name):
        if name[0] == 'h':
            return f"1{name}"
        elif name[0] == 'b':
            return f"2{name}"
        else:
            return f"3{name}"

    print("\n".join(sorted((cmd for cmd in sCommands if cmd and cmd[0] != '!'), key=key))) # commands started with ! are secondary and not listed

# ----------------------------------------------------------------------

def sy():
    subprocess.check_call("./sy", shell=True)

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
