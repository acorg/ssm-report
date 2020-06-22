# ----------------------------------------------------------------------

# [subtype, assay, lab, map-name]
def maps():
    return [
        ["h1", "hi", "cdc", "156"],
        ["h1", "hi", "melb", "156"],

        ["bvic", "hi", "cdc",  "clade"],
        ["bvic", "hi", "melb", "clade"],
        ["bvic", "hi", "niid", "clade"],
        ["bvic", "hi", "nimr", "clade"],
        ["bvic", "hi", "cdc",  "clade-6m"],
        ["bvic", "hi", "melb", "clade-6m"],
        ["bvic", "hi", "niid", "clade-6m"],
        ["bvic", "hi", "nimr", "clade-6m"],
        ["bvic", "hi", "cdc",  "clade-12m"],
        ["bvic", "hi", "melb", "clade-12m"],
        ["bvic", "hi", "niid", "clade-12m"],
        ["bvic", "hi", "nimr", "clade-12m"],
        ["bvic", "hi", "cdc",  "clade-ngly"],
        ["bvic", "hi", "melb", "clade-ngly"],
        ["bvic", "hi", "niid", "clade-ngly"],
        ["bvic", "hi", "nimr", "clade-ngly"],
        ["bvic", "hi", "cdc",  "serology"],
        ["bvic", "hi", "melb", "serology"],
        ["bvic", "hi", "niid", "serology"],
        ["bvic", "hi", "nimr", "serology"],

        ["bvic", "hi", "cdc",  "ts"],
        ["bvic", "hi", "melb", "ts"],
        ["bvic", "hi", "niid", "ts"],
        ["bvic", "hi", "nimr", "ts"],
        # ts: compare with previous

        ["h1", "tree"],
        ["h3", "tree"],
        ["bvic", "tree"],
        ["byam", "tree"],

        ["~all", "", "", "geographic"],
        ["~all", "", "", "stat"],
        ]


# ----------------------------------------------------------------------

def report():
    print("local report")

# ----------------------------------------------------------------------
