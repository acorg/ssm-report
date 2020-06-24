# ----------------------------------------------------------------------

# [subtype, assay, lab, map-name]
def maps(modul):
    return [
        #     ["h1", "tree"],
        #     ["h3", "tree"],
        #     ["bvic", "tree"],
        #     ["byam", "tree"],

        #     ["~all", "", "", "geographic"],
        #     ["~all", "", "", "stat"],

        # H1 --------------------------------------------------

        # modul.map.maker(subtype="h1", lab="cdc",  map="156"),
        # modul.map.maker(subtype="h1", lab="melb", map="156"),
        # modul.map.maker(subtype="h1", lab="niid", map="156"),
        # modul.map.maker(subtype="h1", lab="nimr", map="156"),

        # H3 --------------------------------------------------

        # B/Vic --------------------------------------------------

        # compare_with_previous

        modul.map.makers(subtype="bvic", labs=["cdc", "crick", "niid", "vidrl"], maps=["clade", "clade-6m", "clade-12m", "clade-ngly", "serology", "ts"], compare_with_previous=True),

        # modul.map.maker(subtype="bvic", lab="cdc",  map="clade"),
        # modul.map.maker(subtype="bvic", lab="melb", map="clade"),
        # modul.map.maker(subtype="bvic", lab="niid", map="clade"),
        # modul.map.maker(subtype="bvic", lab="nimr", map="clade"),

        # modul.map.maker(subtype="bvic", lab="cdc",  map="clade-6m"),
        # modul.map.maker(subtype="bvic", lab="melb", map="clade-6m"),
        # modul.map.maker(subtype="bvic", lab="niid", map="clade-6m"),
        # modul.map.maker(subtype="bvic", lab="nimr", map="clade-6m"),

        # modul.map.maker(subtype="bvic", lab="cdc",  map="clade-12m"),
        # modul.map.maker(subtype="bvic", lab="melb", map="clade-12m"),
        # modul.map.maker(subtype="bvic", lab="niid", map="clade-12m"),
        # modul.map.maker(subtype="bvic", lab="nimr", map="clade-12m"),

        # modul.map.maker(subtype="bvic", lab="cdc",  map="clade-ngly"),
        # modul.map.maker(subtype="bvic", lab="melb", map="clade-ngly"),
        # modul.map.maker(subtype="bvic", lab="niid", map="clade-ngly"),
        # modul.map.maker(subtype="bvic", lab="nimr", map="clade-ngly"),

        # modul.map.maker(subtype="bvic", lab="cdc",  map="serology"),
        # modul.map.maker(subtype="bvic", lab="melb", map="serology"),
        # modul.map.maker(subtype="bvic", lab="niid", map="serology"),
        # modul.map.maker(subtype="bvic", lab="nimr", map="serology"),
        # modul.map.maker(subtype="bvic",             map="serology"),

        # modul.map.maker(subtype="bvic", lab="cdc",  map="ts", compare_with_previous=True),
        # modul.map.maker(subtype="bvic", lab="melb", map="ts", compare_with_previous=True),
        # modul.map.maker(subtype="bvic", lab="niid", map="ts", compare_with_previous=True),
        # modul.map.maker(subtype="bvic", lab="nimr", map="ts", compare_with_previous=True),

        # B/Yam --------------------------------------------------
    ]

# ----------------------------------------------------------------------

def report():
    print("local report")

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
