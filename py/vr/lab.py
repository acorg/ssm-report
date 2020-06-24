sLabNew = {
    "cdc": "cdc",
    "melb": "vidrl",
    "vidrl": "vidrl",
    "niid": "niid",
    "nimr": "crick",
    "crick": "crick",
    }

sLabOld = {
    "cdc": "cdc",
    "melb": "melb",
    "vidrl": "melb",
    "niid": "niid",
    "nimr": "nimr",
    "crick": "nimr",
    }

def lab_new(lab):
    return sLabNew[lab.lower()]

def lab_old(lab):
    return sLabOld[lab.lower()]

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
