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
sBigSmallDotsDescription = "Small antigen dots indicate strains also in previous report, larger antigen dots indicate strains added since previous report."

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


                       modul.section_title("B"),
                       modul.section_title("B/Vic"),
                       modul.section_title("B/Yam"),
                   ],
                   landscape="portreat"
    )

# ----------------------------------------------------------------------

def h1(modul, vr_data):
    subtype = "A(H1N1)"
    assay = "hi"
    labs = ["CDC", "NIID", "VIDRL"] # "Crick"
    return [
        modul.section_title("{modul.SubtypeDisplay[subtype]}"),
        modul.subsection_title("{modul.SubtypeDisplay[subtype]} geographic data"),
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
    ]

   #  {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 phylogenetic tree"},
   #  {"type": "phylogenetic_description"},
   #  "new_page",
   #  {"type": "phylogenetic_tree", "subtype": "H1"},
   #  "new_page",

   #  {"?type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic map colored by phylogenetic clade"},
   #  {"?type": "description", "text": "CDC+Crick+NIID+VIDRL antigenic map, antigens color-coded by phylogenetic clade."},
   #  {"?type": "map", "subtype": "H1", "assay": "HI", "lab": "all", "map_type": "clade"},
   #  "? new_page",

   #  {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic maps colored by amino-acid at 155, 156"},
   #  {"type": "maps", "images": [
   #    "h1-hi/aa-156-cdc.pdf", "h1-hi/aa-156-nimr.pdf",
   #    "h1-hi/aa-156-niid.pdf", "h1-hi/aa-156-melb.pdf"
   #  ]},
   #  {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic maps colored by amino-acid at 155, 156 (since February 2019)"},
   #  {"type": "maps", "images": [
   #    "h1-hi/aa-156-12m-cdc.pdf", "h1-hi/aa-156-12m-nimr.pdf",
   #    "h1-hi/aa-156-12m-niid.pdf", "h1-hi/aa-156-12m-melb.pdf"
   #  ]},
   #  "new_page",
   #  {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic maps colored by amino-acid at 155, 156 (since August 2019)"},
   #  {"type": "maps", "images": [
   #    "h1-hi/aa-156-6m-cdc.pdf", "h1-hi/aa-156-6m-nimr.pdf",
   #    "h1-hi/aa-156-6m-niid.pdf", "h1-hi/aa-156-6m-melb.pdf"
   #  ]},
   #  "new_page",

   #  {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic maps with serology antigens."},
   #  {"type": "description", "text": "Antigenic maps with serology antigens in orange, other antigens color-coded by by amino-acid at 155, 156."},
   #  {"type": "maps", "images": [
   #    "h1-hi/serology-aa-156-cdc.pdf", "h1-hi/serology-aa-156-nimr.pdf",
   #    "h1-hi/serology-aa-156-niid.pdf", "h1-hi/serology-aa-156-melb.pdf"
   #  ]},
   #  {"?type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic map with serology antigens."},
   #  {"?type": "description", "text": "CDC+Crick+NIID+VIDRL antigenic map with serology antigens in orange, other antigens color-coded by phylogenetic clade."},
   #  {"?type": "map", "subtype": "H1", "assay": "HI", "lab": "all", "map_type": "serology"},
   #  "? new_page",

# ----------------------------------------------------------------------

def h3(modul, vr_data):
    subtype = "A(H3N2)"
    return [
        modul.section_title("{modul.SubtypeDisplay[subtype]}"),
        modul.subsection_title("{modul.SubtypeDisplay[subtype]} geographic data"),
        modul.vspace(3),
        modul.text_no_indent(sGeographicTimeSeriesSubtitle.format(time_series_start=vr_data.start_month_year, time_series_end=vr_data.end_month_year)),
        modul.vspace(1),
        modul.text_no_indent("Strains colored by ??????????"),
        modul.vspace(1),
        modul.text_no_indent(sGeographicMapDesc),
        modul.new_page(), # --------------------------------------------------
        modul.geographic_ts(Path("geo").glob("H3-geographic-*.pdf")),
        modul.new_page(), # --------------------------------------------------
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="CDC", colored_by=sColoredByRegion, vr_data=vr_data),
    ]

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
        modul.antigenic_ts(Path("out").glob(f"{modul.SubtypeFilename[subtype]}-{assay.lower()}-ts-{modul.LabFilename[lab]}-*.pdf")),
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
