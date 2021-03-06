from pathlib import Path

# ----------------------------------------------------------------------

cover_data = {
    "report_hemisphere": "%(report_hemisphere)s",
    "report_year": "%(report_year)s",
    "teleconference":  "%(teleconference)s",
    "meeting_date": "%(meeting_date)s"
}

cover_portreat = {
    "cover_top_space": "130pt",
    "cover_after_meeting_date_space": "180pt",
}

cover_landscape = {
    "cover_top_space": "10pt",
    "cover_after_meeting_date_space": "100pt",
}

# ----------------------------------------------------------------------

compare_with_previous = True

# [subtype, assay, lab, map-name]
def maps(modul):
    # modul is vr.command
    return [
        modul.tree.makers(),
        # modul.tree.info_makers(),

        # H1 --------------------------------------------------

        modul.map.makers(subtype="h1pdm", assay="hi",   labs=["cdc", "crick", "niid", "vidrl"], rbc="turkey",    maps=["clade-155-156", "clade-155-156-6m", "clade-155-156-12m", "serology", "ts", "sp"], compare_with_previous=compare_with_previous),

        # you may add individual maps like below
        # modul.map.maker(subtype="h1pdm", lab="cdc",  map="clade-156"),

        # H3 HI --------------------------------------------------

        modul.map.makers(subtype="h3", assay="hint", labs=["cdc"],                                             maps=["clade", "clade-6m", "clade-12m", "serology", "ts", "sp"], compare_with_previous=compare_with_previous),
        modul.map.makers(subtype="h3", assay="hi",   labs=["crick", "vidrl"],                rbc="guinea-pig", maps=["clade", "clade-6m", "clade-12m", "serology", "ts", "sp"], compare_with_previous=compare_with_previous),

        # H3 Neut --------------------------------------------------

        modul.map.makers(subtype="h3", assay="neut", labs=["cdc", "crick", "niid", "vidrl"],                   maps=["clade", "clade-6m", "clade-12m", "serology", "ts", "sp"], compare_with_previous=compare_with_previous),

        # B/Vic --------------------------------------------------

        modul.map.makers(subtype="bvic", assay="hi", labs=["cdc", "crick", "niid", "vidrl"], rbc=["turkey", "chicken"],  maps=["clade", "clade-6m", "clade-12m", "clade-ngly", "clade-ngly-202001", "serology", "ts", "sp"], compare_with_previous=compare_with_previous),
        #modul.map.info_makers(subtype="bvic", assay="hi", labs=["crick"], rbc="turkey", maps=["info-clade-2m"]),
        #modul.map.info_makers(subtype="bvic", assay="hi", labs=["cdc", "crick", "niid", "vidrl"], rbc="turkey", maps=["info-clade-12m"]),

        # you may add individual maps like below
        # modul.map.maker(subtype="bvic", assay="hi", lab="cdc",  rbc="turkey", map="clade"),

        # B/Yam --------------------------------------------------

        modul.map.makers(subtype="byam", assay="hi", labs=["cdc", "crick", "niid", "vidrl"], rbc=["turkey", "chicken"],  maps=["clade", "clade-6m", "clade-12m", "serology"], compare_with_previous=compare_with_previous),
        # modul.map.info_makers(subtype="byam", assay="hi", labs=["cdc", "crick"], rbc="turkey", maps=["info-clade-12m"]),
    ]

# ----------------------------------------------------------------------

sGeographicTimeSeriesSubtitle = "Month-by-month geographic time series from {time_series_start} to {time_series_end}."
sGeographicMapDesc = "Each dot indicates the isolation location for a strain that has been measured in an HI table. Thus these figures can be interpreted as a virologically-confirmed epidemiological spatial timeseries (modulo the usual caveats about surveillance biases)."
sMonthByMonthTimeSeries = "Month-by-month time series from {time_series_start} to {time_series_end}."
sAntigenicMapGrid = "Grid indicates 1 unit of antigenic distance, a 2-fold dilution in HI titer."

sColoredByRegion = r"Reference antigens and antisera no fill. Epi strains (small dots) colored by region: \\ \ColorCodedByRegion"
sColoredByH3Clade = r"Strains colored by clade: 3C2/3C3=Blue, 3C2a=Red, 3C2a1=DarkRed, 3C3a=Green, 3C3b=DarkBlue, sequenced=Yellow, unsequenced=Grey"

sBigSmallDotsDescription = "Small antigen dots indicate strains also in previous report, larger antigen dots indicate strains added since previous report."

sPhylogeneticDescription = r"""

\vspace{3em}
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
    modul.generate(output_filename=output_filename,
                   data=[
                       modul.cover(**cover_data, **cover_portreat),
                       modul.toc(),
                       *h1(modul, vr_data),
                       *h3(modul, vr_data),
                       *b(modul, vr_data),
                   ],
                   landscape="portreat"
    )

# ----------------------------------------------------------------------

def bold_recent_viruses(modul):
    return modul.text_no_indent("{\\fontsize{7}{7} \\selectfont \\textbf{Viruses that have been added to the map since the September 2020 VCM are shown with a thick bold outline and viruses since TC0 with a thicker black outline} }")
    return modul.text_no_indent("\\textbf{Viruses that have been added to the map since the September 2020 VCM are shown with a thick bold outline and viruses since TC0 with a thicker black outline}")

# ----------------------------------------------------------------------

def h1(modul, vr_data):
    subtype = "A(H1N1)"
    assay = "hi"
    labs = ["CDC", "Crick", "NIID", "VIDRL"]
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
        modul.geographic_ts(sorted(Path("geo").glob("H1-geographic-*.pdf"))),

        modul.new_page(), # --------------------------------------------------
        *antigenic_ts(modul=modul, subtype=subtype, assay="hi", labs=labs, colored_by=sColoredByRegion, vr_data=vr_data),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} phylogenetic tree"),
        modul.text(sPhylogeneticDescription),
        modul.whole_page_image(Path("tree", f"h1.tree.pdf")),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by amino-acid at 155, 156"),
        modul.maps_in_two_columns([
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-cdc.pdf"),  Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-crick.pdf"),
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-niid.pdf"), Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by amino-acid at 155, 156 (since {modul.months_ago(12)})"),
        modul.maps_in_two_columns([
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-12m-cdc.pdf"),  Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-12m-crick.pdf"),
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-12m-niid.pdf"), Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-12m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by amino-acid at 155, 156 (since {modul.months_ago(6)})"),
        modul.maps_in_two_columns([
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-6m-cdc.pdf"),  Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-6m-crick.pdf"),
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-6m-niid.pdf"), Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-clade-155-156-6m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps with serology antigens"),
        modul.text_no_indent("Antigenic maps with serology antigens in orange, other antigens color-coded by by amino-acid at 155, 156."),
        modul.maps_in_two_columns([
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-serology-cdc.pdf"),  Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-serology-crick.pdf"),
            Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-serology-niid.pdf"), Path("out", f"{modul.SubtypeFilename[subtype]}-hi-turkey-serology-vidrl.pdf"),
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
        modul.geographic_ts(sorted(Path("geo").glob("H3-geographic-*.pdf"))),

        modul.new_page(), # --------------------------------------------------
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="hint", lab="CDC",   colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="CDC",   colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="hi",   lab="Crick", colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="Crick", colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="NIID",  colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="hi",   lab="VIDRL", colored_by=sColoredByRegion, vr_data=vr_data),
        *antigenic_ts_for_lab(modul=modul, subtype=subtype, assay="neut", lab="VIDRL", colored_by=sColoredByRegion, vr_data=vr_data),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} phylogenetic tree"),
        modul.text_no_indent(sPhylogeneticDescription),
        modul.whole_page_image(Path("tree", f"{modul.SubtypeFilename[subtype]}.tree.pdf")),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade"),
        modul.maps_in_two_columns([
            Path("out", "h3-hint-clade-cdc.pdf"),                Path("out", "h3-neut-clade-cdc.pdf"),
            Path("out", "h3-hi-guinea-pig-clade-crick.pdf"),     Path("out", "h3-neut-clade-crick.pdf"),
            None,                                                Path("out", "h3-neut-clade-niid.pdf"),
            Path("out", "h3-hi-guinea-pig-clade-vidrl.pdf"),     Path("out", "h3-neut-clade-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(12)})"),
        modul.maps_in_two_columns([
            Path("out", "h3-hint-clade-12m-cdc.pdf"),            Path("out", "h3-neut-clade-12m-cdc.pdf"),
            Path("out", "h3-hi-guinea-pig-clade-12m-crick.pdf"), Path("out", "h3-neut-clade-12m-crick.pdf"),
            None,                                                Path("out", "h3-neut-clade-12m-niid.pdf"),
            Path("out", "h3-hi-guinea-pig-clade-12m-vidrl.pdf"), Path("out", "h3-neut-clade-12m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(6)})"),
        modul.maps_in_two_columns([
            Path("out", "h3-hint-clade-6m-cdc.pdf"),             Path("out", "h3-neut-clade-6m-cdc.pdf"),
            Path("out", "h3-hi-guinea-pig-clade-6m-crick.pdf"),  Path("out", "h3-neut-clade-6m-crick.pdf"),
            None,                                                Path("out", "h3-neut-clade-6m-niid.pdf"),
            Path("out", "h3-hi-guinea-pig-clade-6m-vidrl.pdf"),  Path("out", "h3-neut-clade-6m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps with serology antigens"),
        modul.text_no_indent("Antigenic maps with serology antigens in orange, other antigens color-coded by by phylogenetic clade."),
        modul.maps_in_two_columns([
            Path("out", "h3-hint-serology-cdc.pdf"),             Path("out", "h3-neut-serology-cdc.pdf"),
            Path("out", "h3-hi-guinea-pig-serology-crick.pdf"),  Path("out", "h3-neut-serology-crick.pdf"),
            None,                                                Path("out", "h3-neut-serology-niid.pdf"),
            Path("out", "h3-hi-guinea-pig-serology-vidrl.pdf"),  Path("out", "h3-neut-serology-vidrl.pdf"),
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
        modul.geographic_ts(sorted(Path("geo").glob("B-geographic-*.pdf"))),
        *bvic(modul, vr_data),
        *byam(modul, vr_data),
        ]

def bvic(modul, vr_data):
    subtype = "BVIC"
    labs = ["CDC", "Crick", "NIID", "VIDRL"]
    return [
        modul.new_page(), # --------------------------------------------------
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),
        *antigenic_ts(modul=modul, subtype=subtype, assay="hi", labs=labs, colored_by=sColoredByRegion, vr_data=vr_data),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} phylogenetic tree"),
        modul.text_no_indent(sPhylogeneticDescription),
        modul.whole_page_image(Path("tree", f"{modul.SubtypeFilename[subtype]}.tree.pdf")),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade"),
        modul.maps_in_two_columns([
            Path("out", "bvic-hi-turkey-clade-cdc.pdf"),  Path("out", "bvic-hi-turkey-clade-crick.pdf"),
            Path("out", "bvic-hi-chicken-clade-niid.pdf"), Path("out", "bvic-hi-turkey-clade-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(12)})"),
        modul.maps_in_two_columns([
            Path("out", "bvic-hi-turkey-clade-12m-cdc.pdf"),  Path("out", "bvic-hi-turkey-clade-12m-crick.pdf"),
            Path("out", "bvic-hi-chicken-clade-12m-niid.pdf"), Path("out", "bvic-hi-turkey-clade-12m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(6)})"),
        modul.maps_in_two_columns([
            Path("out", "bvic-hi-turkey-clade-6m-cdc.pdf"),  Path("out", "bvic-hi-turkey-clade-6m-crick.pdf"),
            Path("out", "bvic-hi-chicken-clade-6m-niid.pdf"), Path("out", "bvic-hi-turkey-clade-6m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by clade and potential N-gly"),
        modul.maps_in_two_columns([
            Path("out", "bvic-hi-turkey-clade-ngly-cdc.pdf"),  Path("out", "bvic-hi-turkey-clade-ngly-crick.pdf"),
            Path("out", "bvic-hi-chicken-clade-ngly-niid.pdf"), Path("out", "bvic-hi-turkey-clade-ngly-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        # modul.new_page(), # --------------------------------------------------
        # modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by clade and potential N-gly (since {modul.months_ago(12)})"),
        # modul.maps_in_two_columns([
        #     Path("out", "bvic-hi-turkey-clade-ngly-12m-cdc.pdf"),  Path("out", "bvic-hi-turkey-clade-ngly-12m-crick.pdf"),
        #     Path("out", "bvic-hi-chicken-clade-ngly-12m-niid.pdf"), Path("out", "bvic-hi-turkey-clade-ngly-12m-vidrl.pdf"),
        # ]),
        # bold_recent_viruses(modul),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps with serology antigens"),
        modul.text_no_indent("Antigenic maps with serology antigens in orange, other antigens color-coded by by phylogenetic clade."),
        modul.maps_in_two_columns([
            Path("out", "bvic-hi-turkey-serology-cdc.pdf"),  Path("out", "bvic-hi-turkey-serology-crick.pdf"),
            Path("out", "bvic-hi-chicken-serology-niid.pdf"), Path("out", "bvic-hi-turkey-serology-vidrl.pdf"),
        ]),
    ]


def byam(modul, vr_data):
    subtype = "BYAM"
    labs = ["CDC", "Crick", "NIID", "VIDRL"]
    return [
        modul.new_page(), # --------------------------------------------------
        modul.section_title(f"{modul.SubtypeDisplay[subtype]}"),

        # modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} phylogenetic tree"),
        modul.text_no_indent(sPhylogeneticDescription),
        modul.whole_page_image(Path("tree", f"{modul.SubtypeFilename[subtype]}.tree.pdf")),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade"),
        modul.maps_in_two_columns([
            Path("out", "byam-hi-turkey-clade-cdc.pdf"),  Path("out", "byam-hi-turkey-clade-crick.pdf"),
            Path("out", "byam-hi-chicken-clade-niid.pdf"), Path("out", "byam-hi-turkey-clade-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(12)})"),
        modul.maps_in_two_columns([
            Path("out", "byam-hi-turkey-clade-12m-cdc.pdf"),  Path("out", "byam-hi-turkey-clade-12m-crick.pdf"),
            Path("out", "byam-hi-chicken-clade-12m-niid.pdf"), Path("out", "byam-hi-turkey-clade-12m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),
        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps colored by phylogenetic clade (since {modul.months_ago(6)})"),
        modul.maps_in_two_columns([
            Path("out", "byam-hi-turkey-clade-6m-cdc.pdf"),  Path("out", "byam-hi-turkey-clade-6m-crick.pdf"),
            Path("out", "byam-hi-chicken-clade-6m-niid.pdf"), Path("out", "byam-hi-turkey-clade-6m-vidrl.pdf"),
        ]),
        bold_recent_viruses(modul),

        modul.new_page(), # --------------------------------------------------
        modul.subsection_title(f"{modul.SubtypeDisplay[subtype]} antigenic maps with serology antigens"),
        modul.text_no_indent("Antigenic maps with serology antigens in orange, other antigens color-coded by by phylogenetic clade."),
        modul.maps_in_two_columns([
            Path("out", "byam-hi-turkey-serology-cdc.pdf"),  Path("out", "byam-hi-turkey-serology-crick.pdf"),
            Path("out", "byam-hi-chicken-serology-niid.pdf"), Path("out", "byam-hi-turkey-serology-vidrl.pdf"),
        ]),
    ]

# ----------------------------------------------------------------------

def antigenic_ts(modul, subtype, assay, rbc, labs, colored_by, vr_data):
    return [item for lab in labs for item in antigenic_ts_for_lab(modul=modul, subtype=subtype, assay=assay, rbc=rbc, lab=lab, colored_by=colored_by, vr_data=vr_data)]

def antigenic_ts_for_lab(modul, subtype, assay, lab, colored_by, vr_data, rbc=None):
    lab = lab.upper()
    subtype = subtype.upper()
    if rbc:
        if isinstance(rbc, list):
            for rb in rbc:
                pdf_pattern = f"{modul.SubtypeFilename[subtype]}-{assay.lower()}-{rb}-ts-{modul.LabFilename[lab]}-*.pdf"
                if list(Path("out").glob(pdf_pattern)):
                    break
        else:
            pdf_pattern = f"{modul.SubtypeFilename[subtype]}-{assay.lower()}-{rbc}-ts-{modul.LabFilename[lab]}-*.pdf"
    else:
        pdf_pattern = f"{modul.SubtypeFilename[subtype]}-{assay.lower()}-ts-{modul.LabFilename[lab]}-*.pdf"
    pdfs = sorted(Path("out").glob(pdf_pattern))
    maps = modul.maps_in_two_columns(pdfs)
    # print(f">>>> {pdf_pattern!r} {pdfs}")
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
        modul.statistics_table(subtype=modul.SubtypeStat[subtype], lab=lab, current=Path("stat", "stat.json.xz"), previous=Path("previous", "stat", "stat.json.xz"), start=vr_data.start_date, end=vr_data.end_date),
        modul.new_page(), # --------------------------------------------------
        maps,
        modul.new_page()
        ]

# ----------------------------------------------------------------------

def addendum_1(output_filename, vr_data, modul):
    pages = [modul.signature_page(path) for path in (Path("sp", f"{subtype}.{lab}{assay}.{sp}.pdf") for subtype in ["h1pdm", "h3", "bvic", "byam"] for lab in ["cdc", "nimr", "niid", "melb"] for assay in ["-hi", "-hint", "-neut", ""] for sp in ["sp", "spc"]) if path.exists()]
    modul.generate(output_filename=output_filename,
                   paper_size="a4", landscape="landscape", page_numbering=True,
                   usepackage=r"\usepackage[noheadfoot,nomarginpar,margin=0pt,bottom=10pt,paperheight=900.0pt,paperwidth=565.0pt]{geometry}",
                   data=[
                       modul.cover(addendum="Addendum 1 (integrated genetic-antigenic analyses)", **cover_data, **cover_landscape),
                       modul.serum_circle_description_page(),
                   ] + pages,
    )

# ----------------------------------------------------------------------

def addendum_2(output_filename, vr_data, modul):
    pass

def addendum_3(output_filename, vr_data, modul):
    pass

def addendum_4(output_filename, vr_data, modul):
    pass

def addendum_5(output_filename, vr_data, modul):
    pass

def addendum_6(output_filename, vr_data, modul):
    pass

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
