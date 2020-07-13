from pathlib import Path

# ----------------------------------------------------------------------

compare_with_previous = True

# [subtype, assay, lab, map-name]
def maps(modul):
    return [
        #     ["h1", "tree"],
        #     ["h3", "tree"],
        #     ["bvic", "tree"],
        #     ["byam", "tree"],

        # H1 --------------------------------------------------

        modul.map.makers(subtype="h1", labs=["cdc", "crick", "niid", "vidrl"], maps=["clade-155-156", "clade-155-156-6m", "clade-155-156-12m", "serology", "ts"], compare_with_previous=compare_with_previous),

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

sGeographicTimeSeriesSubtitle = "Month-by-month geographic time series from {time_series_start} to {time_series_end}."
sGeographicMapDesc = "Each dot indicates the isolation location for a strain that has been measured in an HI table. Thus these figures can be interpreted as a virologically-confirmed epidemiological spatial timeseries (modulo the usual caveats about surveillance biases)."
sMonthByMonthTimeSeries = "Month-by-month time series from {time_series_start} to {time_series_end}."
sAntigenicMapGrid = "Grid indicates 1 unit of antigenic distance, a 2-fold dilution in HI titer."

sColoredByRegion = r"Reference antigens and antisera no fill. Epi strains (small dots) colored by region: \\ \ColorCodedByRegion"
sColoredByH3Clade = r"Strains colored by clade: 3C2/3C3=Blue, 3C2a=Red, 3C2a1=DarkRed, 3C3a=Green, 3C3b=DarkBlue, sequenced=Yellow, unsequenced=Grey"

sBigSmallDotsDescription = "Small antigen dots indicate strains also in previous report, larger antigen dots indicate strains added since previous report."

sPhylogeneticDescription = r"""\vspace{3em}
\noindent
The phylogenetic tree is color coded by region, legend is in the bottom left corner of the next page.

\vspace{1em}
\noindent
The month in which recent strains in the tree were isolated is indicated
by horizontal bars to the right of the tree drawn at the same vertical
position as the position of the strain in the tree. The horizontal bars
are also colored by region. This tree is zoomable, and when zoomed the
strain names and dates on which they were isolated can be read.

\vspace{1em}
\noindent
Nucleotide sequences of the HA1 domain of the HA were aligned. MODELTEST was run
on the aligned sequences and GTR+I+gamma4 was determined to be the most
appropriate evolutionary model for phylogenetic tree construction. Initial
tree construction was performed using RAxML v8.2.8 under the GTRGAMMAI
model. Global optimization of branch topology was then performed on the tree
with the best likelihood score from RAxML using GARLI v2.1 under the model
parameters determined by MODELTEST. Garli was run for 1,000,000 generations.
"""

# ----------------------------------------------------------------------

def report(output_filename, vr_data, modul):
    import pprint
    pprint.pprint(vars(vr_data))
    modul.generate(output_filename=output_filename,
                   data=[
                       modul.cover(),
                       modul.toc(),
                       *h1(modul, vr_data),
                       *h3(modul, vr_data),
                       *b(modul, vr_data),
                   ],
                   landscape="portreat"
    )

# ----------------------------------------------------------------------

def h1(modul, vr_data):
    subtype = "A(H1N1)"
    assay = "hi"
    labs = ["CDC", "NIID", "VIDRL"] # "Crick"
    return [
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),

        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} geographic data"),
        modul.vspace(3),
        modul.text_no_indent(sGeographicTimeSeriesSubtitle.format(time_series_start=vr_data.start_month_year, time_series_end=vr_data.end_month_year)),
        modul.vspace(1),
        modul.text_no_indent("Strains colored by clade: 156N+155G=Blue, 156K=Red, 155E=Yellow, 156D=Green, 156S=SpringGreen, 156X=Orange, 155X=Brown, unsequenced=Grey"),
        modul.vspace(1),
        modul.text_no_indent(sGeographicMapDesc),
        modul.new_page(), # --------------------------------------------------
        modul.geographic_ts(Path("geo").glob("H1-geographic-*.pdf")),

        modul.new_page(), # --------------------------------------------------
        *antigenic_ts(modul=modul, subtype=subtype, assay="hi", labs=labs, colored_by=sColoredByRegion, vr_data=vr_data),

        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} phylogenetic tree"),
        modul.text(sPhylogeneticDescription),
        modul.whole_page_image(Path("tree", f"{modul.SubtypeFilename[subtype]}.tree.pdf")),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by amino-acid at 155, 156"),
        modul.maps_in_two_columns([
            Path("out", "h1-hi-clade-155-156-cdc.pdf"),  Path("out", "h1-hi-clade-155-156-crick.pdf"),
            Path("out", "h1-hi-clade-155-156-niid.pdf"), Path("out", "h1-hi-clade-155-156-vidrl.pdf"),
        ]),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by amino-acid at 155, 156 (since {modul.months_ago(12)})"),
        modul.maps_in_two_columns([
            Path("out", "h1-hi-clade-155-156-12m-cdc.pdf"),  Path("out", "h1-hi-clade-155-156-12m-crick.pdf"),
            Path("out", "h1-hi-clade-155-156-12m-niid.pdf"), Path("out", "h1-hi-clade-155-156-12m-vidrl.pdf"),
        ]),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by amino-acid at 155, 156 (since {modul.months_ago(6)})"),
        modul.maps_in_two_columns([
            Path("out", "h1-hi-clade-155-156-6m-cdc.pdf"),  Path("out", "h1-hi-clade-155-156-6m-crick.pdf"),
            Path("out", "h1-hi-clade-155-156-6m-niid.pdf"), Path("out", "h1-hi-clade-155-156-6m-vidrl.pdf"),
        ]),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps with serology antigens"),
        modul.text_no_indent("Antigenic maps with serology antigens in orange, other antigens color-coded by by amino-acid at 155, 156."),
        modul.maps_in_two_columns([
            Path("out", "h1-hi-serology-cdc.pdf"),  Path("out", "h1-hi-serology-crick.pdf"),
            Path("out", "h1-hi-serology-niid.pdf"), Path("out", "h1-hi-serology-vidrl.pdf"),
        ]),
    ]

# ----------------------------------------------------------------------

def h3(modul, vr_data):
    subtype = "A(H3N2)"
    return [
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} geographic data"),
        modul.vspace(3),
        modul.text_no_indent(sGeographicTimeSeriesSubtitle.format(time_series_start=vr_data.start_month_year, time_series_end=vr_data.end_month_year)),
        modul.vspace(1),
        modul.text_no_indent(sColoredByH3Clade),
        modul.vspace(1),
        modul.text_no_indent(sGeographicMapDesc),
        modul.new_page(), # --------------------------------------------------
        modul.geographic_ts(Path("geo").glob("H3-geographic-*.pdf")),

        modul.new_page(), # --------------------------------------------------
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="CDC",   colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="hi",   lab="Crick", colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="Crick", colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="NIID",  colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="hi",   lab="VIDRL", colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="VIDRL", colored_by=sColoredByRegion, vr_data=vr_data),

        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} phylogenetic tree"),
        modul.text_no_indent(sPhylogeneticDescription),
        modul.whole_page_image(Path("tree", f"{modul.SubtypeFilename[subtype]}.tree.pdf")),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade"),
        modul.maps_in_two_columns([
            None,                                     Path("out", "h3-neut-clade-cdc.pdf"),
            Path("out", "h3-hi-clade-crick.pdf"),     Path("out", "h3-neut-clade-crick.pdf"),
            None,                                     Path("out", "h3-neut-clade-niid.pdf"),
            Path("out", "h3-hi-clade-vidrl.pdf"),     Path("out", "h3-neut-clade-vidrl.pdf"),
        ]),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(12)})"),
        modul.maps_in_two_columns([
            None,                                     Path("out", "h3-neut-clade-12m-cdc.pdf"),
            Path("out", "h3-hi-clade-12m-crick.pdf"), Path("out", "h3-neut-clade-12m-crick.pdf"),
            None,                                     Path("out", "h3-neut-clade-12m-niid.pdf"),
            Path("out", "h3-hi-clade-12m-vidrl.pdf"), Path("out", "h3-neut-clade-12m-vidrl.pdf"),
        ]),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(6)})"),
        modul.maps_in_two_columns([
            None,                                     Path("out", "h3-neut-clade-6m-cdc.pdf"),
            Path("out", "h3-hi-clade-6m-crick.pdf"),  Path("out", "h3-neut-clade-6m-crick.pdf"),
            None,                                     Path("out", "h3-neut-clade-6m-niid.pdf"),
            Path("out", "h3-hi-clade-6m-vidrl.pdf"),  Path("out", "h3-neut-clade-6m-vidrl.pdf"),
        ]),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps with serology antigens"),
        modul.text_no_indent("Antigenic maps with serology antigens in orange, other antigens color-coded by by phylogenetic clade."),
        modul.maps_in_two_columns([
            None,                                     Path("out", "h3-neut-serology-cdc.pdf"),
            Path("out", "h3-hi-serology-crick.pdf"),  Path("out", "h3-neut-serology-crick.pdf"),
            None,                                     Path("out", "h3-neut-serology-niid.pdf"),
            Path("out", "h3-hi-serology-vidrl.pdf"),  Path("out", "h3-neut-serology-vidrl.pdf"),
        ]),
    ]

# ----------------------------------------------------------------------

def b(modul, vr_data):
    subtype = "B"
    return [
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} Victoria and Yamagata geographic data"),
        modul.vspace(3),
        modul.text_no_indent(sGeographicTimeSeriesSubtitle.format(time_series_start=vr_data.start_month_year, time_series_end=vr_data.end_month_year)),
        modul.vspace(1),
        modul.text_no_indent(r"Strains colored by lineage: \\ \ColorCodedByLineageVicDelMut"),
        modul.vspace(1),
        modul.text_no_indent(sGeographicMapDesc),
        modul.new_page(), # --------------------------------------------------
        modul.geographic_ts(Path("geo").glob("B-geographic-*.pdf")),
        *bvic(modul, vr_data),
        *byam(modul, vr_data),
        ]

def bvic(modul, vr_data):
    subtype = "BVIC"
    return [
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),
        ]

    # {"type": "section_begin", "title": "B/Vic"},
    # {"type": "subsection_begin", "subtype": "bv", "title": "CDC B/Vic antigenic data"},
    # {"type": "antigenic_ts_description", "coloring": "continents"},
    # {"type": "statistics_table", "subtype": "bv", "lab": "CDC"},
    # "new_page",
    # {"type": "antigenic_ts", "subtype": "bv", "assay": "HI", "lab": "CDC"},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "Crick B/Vic antigenic data"},
    # {"type": "antigenic_ts_description", "coloring": "continents"},
    # {"type": "statistics_table", "subtype": "bv", "lab": "NIMR"},
    # "new_page",
    # {"type": "antigenic_ts", "subtype": "bv", "assay": "HI", "lab": "NIMR"},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "NIID B/Vic antigenic data"},
    # {"type": "antigenic_ts_description", "coloring": "continents"},
    # {"type": "statistics_table", "subtype": "bv", "lab": "NIID"},
    # "new_page",
    # {"type": "antigenic_ts", "subtype": "bv", "assay": "HI", "lab": "NIID"},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "VIDRL B/Vic antigenic data"},
    # {"type": "antigenic_ts_description", "coloring": "continents"},
    # {"type": "statistics_table", "subtype": "bv", "lab": "MELB"},
    # "new_page",
    # {"type": "antigenic_ts", "subtype": "bv", "assay": "HI", "lab": "MELB"},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "B/Vic phylogenetic tree"},
    # {"type": "phylogenetic_description"},
    # {"type": "phylogenetic_description_bvic_del"},
    # "new_page",
    # {"type": "phylogenetic_tree", "subtype": "bv"},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "B/Vic antigenic maps colored by phylogenetic clade"},
    # {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps, antigens color-coded by phylogenetic clade."},
    # {"type": "maps", "images": [
    #   "bv-hi/clade-cdc.pdf", "bv-hi/clade-nimr.pdf",
    #   "bv-hi/clade-niid.pdf", "bv-hi/clade-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "B/Vic antigenic maps colored by phylogenetic clade (since February 2019)"},
    # {"type": "maps", "images": [
    #   "bv-hi/clade-12m-cdc.pdf", "bv-hi/clade-12m-nimr.pdf",
    #   "bv-hi/clade-12m-niid.pdf", "bv-hi/clade-12m-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "B/Vic antigenic maps colored by phylogenetic clade (since August 2019)"},
    # {"type": "maps", "images": [
    #   "bv-hi/clade-6m-cdc.pdf", "bv-hi/clade-6m-nimr.pdf",
    #   "bv-hi/clade-6m-niid.pdf", "bv-hi/clade-6m-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "B/Vic antigenic maps colored by clade and potential N-gly"},
    # {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps, antigens color-coded by clade and potential N-gly."},
    # {"type": "maps", "images": [
    #   "bv-hi/N-gly-197-cdc.pdf", "bv-hi/N-gly-197-nimr.pdf",
    #   "bv-hi/N-gly-197-niid.pdf", "bv-hi/N-gly-197-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "bv", "title": "B/Vic antigenic maps with serology antigens"},
    # {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps with serology antigens in orange, other antigens color-coded by phylogenetic clade."},
    # {"type": "maps", "images": [
    #   "bv-hi/serology-cdc.pdf", "bv-hi/serology-nimr.pdf",
    #   "bv-hi/serology-niid.pdf", "bv-hi/serology-melb.pdf"
    # ]},

def byam(modul, vr_data):
    subtype = "BYAM"
    return [
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),
        ]

    # {"type": "subsection_begin", "subtype": "by", "title": "B/Yam phylogenetic tree"},
    # {"type": "phylogenetic_description"},
    # "new_page",
    # {"type": "phylogenetic_tree", "subtype": "by"},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "by", "title": "B/Yam antigenic maps colored by phylogenetic clade"},
    # {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps, antigens color-coded by phylogenetic clade."},
    # {"type": "maps", "images": [
    #   "by-hi/clade-cdc.pdf", "by-hi/clade-nimr.pdf",
    #   "by-hi/clade-niid.pdf", "by-hi/clade-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "by", "title": "B/Yam antigenic maps colored by phylogenetic clade (since February 2019)"},
    # {"type": "maps", "images": [
    #   "by-hi/clade-12m-cdc.pdf", "by-hi/clade-12m-nimr.pdf",
    #   "by-hi/clade-12m-niid.pdf", "by-hi/clade-12m-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "by", "title": "B/Yam antigenic maps colored by phylogenetic clade (since August 2019)"},
    # {"type": "maps", "images": [
    #   "by-hi/clade-6m-cdc.pdf", "by-hi/clade-6m-nimr.pdf",
    #   "by-hi/clade-6m-niid.pdf", "by-hi/clade-6m-melb.pdf"
    # ]},
    # "new_page",
    # {"type": "subsection_begin", "subtype": "by", "title": "B/Yam antigenic maps with serology antigens"},
    # {"type": "description", "text": "Top row left to right CDC, Crick, bottom row left to right NIID, VIDRL antigenic maps with serology antigens in orange, other antigens color-coded by phylogenetic clade."},
    # {"type": "maps", "images": [
    #   "by-hi/serology-cdc.pdf", "by-hi/serology-nimr.pdf",
    #   "by-hi/serology-niid.pdf", "by-hi/serology-melb.pdf"
    # ]},

# ----------------------------------------------------------------------

def antigenic_ts(modul, subtype, assay, labs, colored_by, vr_data):
    return [item for lab in labs for item in antigenic_ts_for_lab(modul=modul, subtype=subtype, assay=assay, lab=lab, colored_by=colored_by, vr_data=vr_data)]

def antigenic_ts_for_lab(modul, subtype, assay, lab, colored_by, vr_data):
    lab = lab.upper()
    subtype = subtype.upper()
    return [
        modul.subsection_title(f"{modul.LabDisplay[lab]} {modul.subtype_assay_display(subtype, assay)} antigenic data"),
        modul.vspace(3),
        modul.text_no_indent(sMonthByMonthTimeSeries.format(time_series_start=vr_data.start_month_year, time_series_end=vr_data.end_month_year)),
        modul.vspace(1),
        modul.text_no_indent(sAntigenicMapGrid),
        modul.vspace(1),
        modul.text_no_indent(colored_by),
        # modul.vspace(1),
        # modul.text_no_indent(sBigSmallDotsDescription),
        modul.vspace(3),
        modul.statistics_table(subtype=subtype, lab=lab, current=Path("stat", "stat.json.xz"), previous=Path("previous", "stat", "stat.json.xz"), start=vr_data.start_date, end=vr_data.end_date),
        modul.new_page(), # --------------------------------------------------
        modul.maps_in_two_columns(Path("out").glob(f"{modul.SubtypeFilename[subtype]}-{assay.lower()}-ts-{modul.LabFilename[lab]}-*.pdf")),
        modul.new_page()
        ]

# ----------------------------------------------------------------------

def addendum_1(output_filename, modul):
    pass

def addendum_2(output_filename, modul):
    pass

def addendum_3(output_filename, modul):
    pass

def addendum_4(output_filename, modul):
    pass

def addendum_5(output_filename, modul):
    pass

def addendum_6(output_filename, modul):
    pass

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
