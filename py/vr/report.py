import sys, subprocess, inspect, pprint
from pathlib import Path

# ----------------------------------------------------------------------

def generate(output_filename: Path, data: list,
             paper_size="a4",
             landscape="landscape", # portreat
             cover_top_space="130pt",
             cover_after_meeting_date_space="180pt"
):
    output_dir = output_filename.parent
    output_dir.mkdir(exist_ok=True)
    latex_source = output_dir.joinpath(output_filename.stem + ".tex")
    generate_latex(inspect.getargvalues(inspect.currentframe()).locals)
    if output_filename.exists():
        output_filename.chmod(0o644)
    subprocess.check_call(f"cd {output_dir} && pdflatex -interaction=nonstopmode -file-line-error {latex_source.resolve()}", shell=True)
    if output_filename.exists():
        output_filename.chmod(0o444)
    subprocess.check_call(f"open {output_filename}")

# ----------------------------------------------------------------------

def generate_latex(args):
    pass

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
