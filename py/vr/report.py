import sys

# ----------------------------------------------------------------------

def make_report(command_name):
    print(sys.path, file=sys.stderr)
    from report import report
    report()
    print("make_report")

# ----------------------------------------------------------------------

def make_addendum(command_name):
    pass

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
