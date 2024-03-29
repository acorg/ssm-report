import sys, subprocess, inspect, datetime, pprint
from pathlib import Path
from . import latex

# ----------------------------------------------------------------------

def generate(output_filename: Path, data: list,
             paper_size="a4",
             page_numbering=True,
             landscape="landscape", # portreat
             usepackage="",
             time_stamp=True
):
    output_dir = output_filename.parent
    output_dir.mkdir(exist_ok=True)
    latex_source = output_dir.joinpath(output_filename.stem + ".tex")
    generate_latex(latex_source, inspect.getargvalues(inspect.currentframe()).locals)
    latex_source = latex_source.resolve()
    if output_filename.exists():
        output_filename.chmod(0o644)
    cmd = ["pdflatex", "-interaction=batchmode", "-no-shell-escape", "-file-line-error", str(latex_source)]
    print(f">>> cd {output_dir}\n>>> {' '.join(cmd)}", file=sys.stderr)
    returncode = subprocess.call(cmd, cwd=output_dir)
    if returncode:
        subprocess.call(["grep", "-i", "error", "report.log"], cwd=output_dir)
    if output_filename.exists():
        output_filename.chmod(0o444)
    subprocess.check_call(f"open {output_filename}", shell=True)

# ----------------------------------------------------------------------

def generate_latex(latex_source, args):
    # pprint.pprint(args)
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
    now = datetime.datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M %Z")
    tex = [
        substitute(latex.T_Head, program=sys.argv[0], now=now,
                   documentclass="\documentclass[%spaper,%s,12pt]{article}" % (args["paper_size"], args["landscape"]),
                   usepackage=args["usepackage"],
        ),
        latex.T_BlankPage,
        latex.T_RemoveSectionNumbering,
        latex.T_TableOfContents,
        # latex.T_ColorsBW,
        latex.T_ColorsColors,
        latex.T_ColorCodedBy,
        latex.T_AntigenicMapTable,
        latex.T_WhoccStatisticsTable,
        latex.T_GeographicMapsTable,
        latex.T_WholePagePdf,
        latex.T_SignaturePage,
        # latex.T_AntigenicGeneticMapSingle,
        # latex.T_OverviewMapSingle,
        substitute(latex.T_Begin),
    ]
    if not args["page_numbering"]:
        tex.append(latex.T_NoPageNumbering)
    for entry in args["data"]:
        tex.extend(entry.latex())
    if args.get("time_stamp"):
        tex.append(substitute("\\par\\vspace*{\\fill}\\tiny{Report generated: %now%}\n\\newpage", now=now))
    tex.append(latex.T_Tail)
    text = '\n\n'.join(tex)
    with latex_source.open('w') as f:
        f.write(text)

# ======================================================================

def substitute(__text__, **args):
    # __text__ = __text__.replace('%no-eol%\n', '')
    for option, value in args.items():
        if isinstance(value, (str, int, float)):
            __text__ = __text__.replace('%{}%'.format(option), str(value))
    return __text__

# ======================================================================

def make_report(command_name, *r, **a):
    from report import report
    from . import sections
    from .command import vr_data
    report(Path("report", "report.pdf"), vr_data(), sections)

def make_report_b(command_name, *r, **a):
    from report import report_b
    from . import sections
    from .command import vr_data
    report_b(Path("report", "report-b.pdf"), vr_data(), sections)

def make_report_h1(command_name, *r, **a):
    from report import report_h1
    from . import sections
    from .command import vr_data
    report_h1(Path("report", "report-h1.pdf"), vr_data(), sections)

def make_report_h3(command_name, *r, **a):
    from report import report_h3
    from . import sections
    from .command import vr_data
    report_h3(Path("report", "report-h3.pdf"), vr_data(), sections)

def make_report_and_upload(command_name, *r, **a):
    subprocess.check_call("""ssh i19 "cd $(pwd); if [[ -d report && -f report/report.pdf ]]; then mv report/report.pdf report/report.\$(stat -c %y report/report.pdf | sed 's/\..*//g; s/-//g; s/://g; s/ /-/g').pdf; else echo no report dir; fi" """, shell=True)
    make_report(command_name, *r, **a)
    subprocess.check_call("./sy", shell=True)

# ----------------------------------------------------------------------

from report import *

def make_addendum_X(no, subtype=None, *r, **a):
    from . import sections
    from .command import vr_data
    if subtype:
        globals()[f"addendum_{no}_{subtype}"](Path("report", f"addendum-{no}-{subtype}.pdf"), vr_data(), sections)
    else:
        globals()[f"addendum_{no}"](Path("report", f"addendum-{no}.pdf"), vr_data(), sections)

def make_addendum_1(command_name, *r, **a):
    make_addendum_X(1, *r, **a)

def make_addendum_1_b(command_name, *r, **a):
    make_addendum_X(1, subtype='b', *r, **a)

def make_addendum_1_h1(command_name, *r, **a):
    make_addendum_X(1, subtype='h1', *r, **a)

def make_addendum_1_h3(command_name, subtype='h3', *r, **a):
    make_addendum_X(1, subtype='h3', *r, **a)

def make_addendum_2(command_name, *r, **a):
    make_addendum_X(2, *r, **a)

def make_addendum_2_b(command_name, *r, **a):
    make_addendum_X(2, subtype='b', *r, **a)

def make_addendum_2_h1(command_name, *r, **a):
    make_addendum_X(2, subtype='h1', *r, **a)

def make_addendum_2_h3(command_name, subtype='h3', *r, **a):
    make_addendum_X(2, subtype='h3', *r, **a)

def make_addendum_3(command_name, *r, **a):
    make_addendum_X(3, *r, **a)

def make_addendum_4(command_name, *r, **a):
    make_addendum_X(4, *r, **a)

def make_addendum_5(command_name, *r, **a):
    make_addendum_X(5, *r, **a)

def make_addendum_6(command_name, *r, **a):
    make_addendum_X(6, *r, **a)

# ======================================================================
