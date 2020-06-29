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

sLabDisplayName = {
    "cdc": "CDC",
    "cnic": "CNIC",
    "nimr": "Crick",
    "crick": "Crick",
    "niid": "NIID",
    "melb": "VIDRL",
    "vidrl": "VIDRL",
    "all": "All labs"
}

def lab_new(lab):
    return sLabNew[lab.lower()]

def lab_old(lab):
    return sLabOld[lab.lower()]

def lab_display_name(lab):
    return sLabDisplayName[lab.lower()]

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
