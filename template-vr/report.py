# ----------------------------------------------------------------------

compare_with_previous = True

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

        modul.map.makers(subtype="h1", labs=["cdc", "crick", "niid", "vidrl"], maps=["clade-156", "clade-156-6m", "clade-156-12m", "serology", "ts"], compare_with_previous=compare_with_previous),

        # you may add individual maps like below
        # modul.map.maker(subtype="h1", lab="cdc",  map="clade-156"),

        # H3 HI --------------------------------------------------

        modul.map.makers(subtype="h3", assay="hi", labs=["crick", "vidrl"], maps=["clade", "clade-6m", "clade-12m", "serology", "ts"], compare_with_previous=compare_with_previous),

        # H3 Neut --------------------------------------------------

        modul.map.makers(subtype="h3", assay="neut", labs=["cdc", "crick", "niid", "vidrl"], maps=["clade", "clade-6m", "clade-12m", "serology", "ts"], compare_with_previous=compare_with_previous),

        # B/Vic --------------------------------------------------

        modul.map.makers(subtype="bvic", labs=["cdc", "crick", "niid", "vidrl"], maps=["clade", "clade-6m", "clade-12m", "clade-ngly", "serology", "ts"], compare_with_previous=compare_with_previous),

        # you may add individual maps like below
        # modul.map.maker(subtype="bvic", lab="cdc",  map="clade"),

        # B/Yam --------------------------------------------------

        modul.map.makers(subtype="byam", labs=["cdc", "crick", "niid", "vidrl"], maps=["clade", "clade-6m", "clade-12m", "serology"], compare_with_previous=compare_with_previous),
    ]

# ----------------------------------------------------------------------

def report():
    print("local report")

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
