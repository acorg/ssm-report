sLabNew = {
    "cdc": "cdc",
    "cnic": "cnic",
    "melb": "vidrl",
    "vidrl": "vidrl",
    "niid": "niid",
    "nimr": "crick",
    "crick": "crick",
    "crick2": "crick2",
    }

sLabOld = {
    "cdc": "cdc",
    "cnic": "cnic",
    "melb": "melb",
    "vidrl": "melb",
    "niid": "niid",
    "nimr": "nimr",
    "crick": "nimr",
    "crick2": "nimr2",
    }

sLabDisplayName = {
    "cdc": "CDC",
    "cnic": "CNIC",
    "nimr": "Crick",
    "crick": "Crick",
    "crick2": "Crick",
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
