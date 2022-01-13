import sys, traceback
sys.path.insert(0, ".")
try:
    from . import command as command
except Exception as err:
    print(traceback.format_exc())
    # print(err)
    pass

from .error import Error

# ======================================================================
