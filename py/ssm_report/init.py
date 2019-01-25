import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import os, subprocess, shutil, re, datetime

# ----------------------------------------------------------------------

def init_git():
    project_git_dir = Path(".").resolve().name + ".git"
    module_logger.info("init_git {}".format(project_git_dir))
    # remote
    if not subprocess.call("ssh albertine '[[ -f who-reports/{p}/HEAD ]]'".format(p=project_git_dir), shell=True):
        module_logger.info("Remote git repo exists")
    elif not subprocess.call("ssh albertine '[[ -e who-reports/{p} ]]'".format(p=project_git_dir), shell=True):
        raise RuntimeError("albertine:who-reports/{p} present but it is not a git repository".format(p=project_git_dir))
    else:
        module_logger.info("Creating remote git repo")
        subprocess.check_call("ssh albertine 'mkdir who-reports/{p} && cd who-reports/{p} && git init --bare'".format(p=project_git_dir), shell=True)

    template_dir = _template_dir()
    for src, dest in [["root-gitignore", ".gitignore"], ["rename-report-on-server", "rename-report-on-server"], ["rr", "rr"], ["sy", "sy"], ["index.html", "index.html"]]:
        if not Path(dest).exists():
            shutil.copy(template_dir.joinpath(src).resolve(), Path(dest))

    if Path(".git").is_dir():
        module_logger.info("local repository present")
    elif Path(".git").exists():
        raise RuntimeError(".git exists and it is not a directory")
    else:
        subprocess.check_call("git init && git add rr .gitignore && git commit -m 'ssm-report init_git' && git remote add origin ssh://albertine/home/eu/who-reports/{p} && git push --set-upstream origin master".format(p=project_git_dir), shell=True)

# ----------------------------------------------------------------------

def init_dirs():
    for dir in ["tree", "sp"]:
        Path(dir).mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------

def get_dbs():
    db_dir = Path("db")
    module_logger.info("Updating hidb in " + repr(str(db_dir)))
    subprocess.check_call("rsync -av 'albertine:AD/data/hidb5.*.{{json.xz,hidb5b}}' '{}'".format(db_dir), shell=True)
    module_logger.info("Updating locdb in " + repr(str(db_dir)))
    locdb_file = db_dir.joinpath("locationdb.json.xz")
    if not locdb_file.exists():
        locdb_file.symlink_to(Path(os.environ["ACMACSD_ROOT"], "data", "locationdb.json.xz").resolve())
    shutil.copy(Path(os.environ["ACMACSD_ROOT"], "data", "seqdb.json.xz"), db_dir)

# ----------------------------------------------------------------------

def init_settings():
    _make_report_json()
    from .serum_coverage import make_serum_coverage_report_settings
    make_serum_coverage_report_settings()
    from .geographic import make_geographic_settings
    make_geographic_settings()

    template_dir = _template_dir()
    for fn in ["bv-hi.json", "by-hi.json", "h1-hi.json", "h3-hi.json", "h3-neut.json", "serology.bv-hi.json", "serology.by-hi.json", "serology.h1-hi.json", "serology.h3-hi.json", "serology.h3-neut.json", "vaccines.bv-hi.json", "vaccines.by-hi.json", "vaccines.h1-hi.json", "vaccines.h3-hi.json", "vaccines.h3-neut.json"]:
        if not Path(fn).exists():
            shutil.copy(template_dir.joinpath(fn).resolve(), Path(fn))

# ----------------------------------------------------------------------

def _make_report_json():
    report_json_file = Path("report.json")
    if not report_json_file.exists():
        module_logger.info(f"making report.json")
        today = datetime.date.today()
        if today.month > 2 and today.month < 10:
            hemisphere = "Southern"
            year = str(today.year + 1)
        else:
            hemisphere = "Northern"
            if today.month >= 10:
                year = "{}/{}".format(today.year + 1, today.year + 2)
            else:
                year = "{}/{}".format(today.year, today.year + 1)

        m = re.match(r"(\d\d\d\d)-(\d\d)(\d\d)", Path(".").resolve().name)
        if m:
            meeting_date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).strftime("%d %B %Y")
        else:
            meeting_date = (today + datetime.timedelta(days=7)).strftime("%d %B %Y")

        subst = {
            "previous_dir": _find_previous_dir(),
            "hemisphere": hemisphere,
            "meeting_date": meeting_date,
            "year": year,
            "time_series_start": (today - datetime.timedelta(days=180)).strftime("%Y-%m-01"),
            "time_series_end": today.strftime("%Y-%m-01"),
            "twelve_month_ago": (today - datetime.timedelta(days=365)).strftime("%B %Y"),
            "six_month_ago": (today - datetime.timedelta(days=183)).strftime("%B %Y"),
        }
        report_json_file.open("w").write(_template_dir().joinpath("report.json").resolve().open().read() % subst)

# ----------------------------------------------------------------------

def _find_previous_dir():
    for dd in sorted(Path("..").resolve().glob("*"), reverse=True):
        if dd.is_dir() and dd != Path(".").resolve():
            return str(dd)
    return ""

# ----------------------------------------------------------------------

def _template_dir():
    return Path(os.environ["ACMACSD_ROOT"], "sources", "ssm-report", "template").resolve()

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
