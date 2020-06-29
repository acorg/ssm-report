import sys, subprocess, inspect, datetime, pprint
from pathlib import Path
from . import latex

# ----------------------------------------------------------------------

def generate(output_filename: Path, data: list,
             paper_size="a4",
             page_numbering=True,
             landscape="landscape", # portreat
):
    output_dir = output_filename.parent
    output_dir.mkdir(exist_ok=True)
    latex_source = output_dir.joinpath(output_filename.stem + ".tex")
    generate_latex(latex_source, inspect.getargvalues(inspect.currentframe()).locals)
    if output_filename.exists():
        output_filename.chmod(0o644)
    subprocess.check_call(f"cd {output_dir} && pdflatex -interaction=nonstopmode -file-line-error {latex_source.resolve()}", shell=True)
    if output_filename.exists():
        output_filename.chmod(0o444)
    subprocess.check_call(f"open {output_filename}", shell=True)

# ----------------------------------------------------------------------

class cover:

    def __init__(self,
                 cover_top_space="130pt",
                 cover_after_meeting_date_space="180pt",
                 cover_quotation="\\quotation",
                 report_hemisphere="Southern",
                 report_year="2021",
                 teleconference="Teleconference 1",
                 addendum="",
                 meeting_date="11th August 2020"
    ):
        self.args = inspect.getargvalues(inspect.currentframe()).locals

    def latex(self):
        return [
            substitute(latex.T_Cover,
                       **self.args
                       )
            ]
    
# ----------------------------------------------------------------------

def generate_latex(latex_source, args):
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
    tex = [
        substitute(latex.T_Head, program=sys.argv[0], now=datetime.datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M %Z"),
                   documentclass="\documentclass[%spaper,%s,12pt]{article}" % (args["paper_size"], args["landscape"])),
        latex.T_BlankPage,
        latex.T_RemoveSectionNumbering,
        latex.T_TableOfContents,
        # latex.T_ColorsBW,
        latex.T_ColorCodedBy,
        latex.T_AntigenicMapTable,
        latex.T_WhoccStatisticsTable,
        latex.T_GeographicMapsTable,
        latex.T_PhylogeneticTree,
        latex.T_SignaturePage,
        # latex.T_AntigenicGeneticMapSingle,
        # latex.T_OverviewMapSingle,
        substitute(latex.T_Begin),
    ]
    if not args["page_numbering"]:
        tex.append(latex.T_NoPageNumbering)
    for entry in args["data"]:
        tex.extend(entry.latex())
    tex.append(latex.T_Tail)
    text = '\n\n'.join(tex)
    with latex_source.open('w') as f:
        f.write(text)

# ======================================================================

def substitute(text, **args):
    # text = text.replace('%no-eol%\n', '')
    for option, value in args.items():
        if isinstance(value, (str, int, float)):
            text = text.replace('%{}%'.format(option), str(value))
    return text

# ======================================================================

def make_report(command_name, *r, **a):
    from report import report
    report(Path("report", "report.pdf"), sys.modules[__name__])

# ----------------------------------------------------------------------

def make_addendum_1(command_name, *r, **a):
    pass

def make_addendum_2(command_name, *r, **a):
    pass

def make_addendum_3(command_name, *r, **a):
    pass

def make_addendum_4(command_name, *r, **a):
    pass

def make_addendum_5(command_name, *r, **a):
    pass

def make_addendum_6(command_name, *r, **a):
    pass

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
