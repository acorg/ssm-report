# ----------------------------------------------------------------------

# [subtype, assay, lab, map-name]
def maps(modul):
    return [
        modul.map.maker(subtype="bvic", lab="cdc",  map="clade"),
        modul.map.maker(subtype="bvic", lab="melb", map="clade"),
        modul.map.maker(subtype="bvic", lab="niid", map="clade"),
        modul.map.maker(subtype="bvic", lab="nimr", map="clade"),

        modul.map.maker(subtype="bvic", lab="cdc",  map="clade-6m"),
        modul.map.maker(subtype="bvic", lab="melb", map="clade-6m"),
        modul.map.maker(subtype="bvic", lab="niid", map="clade-6m"),
        modul.map.maker(subtype="bvic", lab="nimr", map="clade-6m"),

        modul.map.maker(subtype="bvic", lab="cdc",  map="clade-12m"),
        modul.map.maker(subtype="bvic", lab="melb", map="clade-12m"),
        modul.map.maker(subtype="bvic", lab="niid", map="clade-12m"),
        modul.map.maker(subtype="bvic", lab="nimr", map="clade-12m"),

        modul.map.maker(subtype="bvic", lab="cdc",  map="clade-ngly"),
        modul.map.maker(subtype="bvic", lab="melb", map="clade-ngly"),
        modul.map.maker(subtype="bvic", lab="niid", map="clade-ngly"),
        modul.map.maker(subtype="bvic", lab="nimr", map="clade-ngly"),

        modul.map.maker(subtype="bvic", lab="cdc",  map="serology"),
        modul.map.maker(subtype="bvic", lab="melb", map="serology"),
        modul.map.maker(subtype="bvic", lab="niid", map="serology"),
        modul.map.maker(subtype="bvic", lab="nimr", map="serology"),
        modul.map.maker(subtype="bvic",             map="serology"),

        modul.map.maker(subtype="bvic", lab="cdc",  map="ts", compare_with_previous=True),
        modul.map.maker(subtype="bvic", lab="melb", map="ts", compare_with_previous=True),
        modul.map.maker(subtype="bvic", lab="niid", map="ts", compare_with_previous=True),
        modul.map.maker(subtype="bvic", lab="nimr", map="ts", compare_with_previous=True),
    ]

    # return [
    #     ["h1", "hi", "cdc", "156"],
    #     ["h1", "hi", "melb", "156"],

    #     ["bvic", "hi", "cdc",  "clade"],
    #     ["bvic", "hi", "melb", "clade"],
    #     ["bvic", "hi", "niid", "clade"],
    #     ["bvic", "hi", "nimr", "clade"],
    #     ["bvic", "hi", "cdc",  "clade-6m"],
    #     ["bvic", "hi", "melb", "clade-6m"],
    #     ["bvic", "hi", "niid", "clade-6m"],
    #     ["bvic", "hi", "nimr", "clade-6m"],
    #     ["bvic", "hi", "cdc",  "clade-12m"],
    #     ["bvic", "hi", "melb", "clade-12m"],
    #     ["bvic", "hi", "niid", "clade-12m"],
    #     ["bvic", "hi", "nimr", "clade-12m"],
    #     ["bvic", "hi", "cdc",  "clade-ngly"],
    #     ["bvic", "hi", "melb", "clade-ngly"],
    #     ["bvic", "hi", "niid", "clade-ngly"],
    #     ["bvic", "hi", "nimr", "clade-ngly"],
    #     ["bvic", "hi", "cdc",  "serology"],
    #     ["bvic", "hi", "melb", "serology"],
    #     ["bvic", "hi", "niid", "serology"],
    #     ["bvic", "hi", "nimr", "serology"],

    #     ["bvic", "hi", "cdc",  "ts"],
    #     ["bvic", "hi", "melb", "ts"],
    #     ["bvic", "hi", "niid", "ts"],
    #     ["bvic", "hi", "nimr", "ts"],
    #     # ts: compare with previous

    #     ["h1", "tree"],
    #     ["h3", "tree"],
    #     ["bvic", "tree"],
    #     ["byam", "tree"],

    #     ["~all", "", "", "geographic"],
    #     ["~all", "", "", "stat"],
    #     ]


# ----------------------------------------------------------------------

def report():
    print("local report")

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
