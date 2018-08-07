import sys, os, copy, datetime
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
from acmacs_base.json import write_json

# ----------------------------------------------------------------------

def make_report_settings():
    report_settings_file = Path("report.json")
    if not report_settings_file.exists():
        report = copy.deepcopy(sReport)
        report["previous"] = find_previous_dir()
        today = datetime.date.today()
        if today.month > 2 and today.month < 10:
            report["cover"]["hemisphere"] = "Southern"
            report["cover"]["year"] = str(today.year + 1)
        else:
            report["cover"]["hemisphere"] = "Northern"
            if today.month >= 10:
                report["cover"]["year"] = "{}/{}".format(today.year + 1, today.year + 2)
            else:
                report["cover"]["year"] = "{}/{}".format(today.year, today.year + 1)
        report["cover"]["meeting_date"] = (today + datetime.timedelta(days=7)).strftime("%d %B %Y")
        report["time_series"]["date"] = {"start": (today - datetime.timedelta(days=180)).strftime("%Y-%m-01"), "end": today.strftime("%Y-%m-01")}

        subst = {
            "twelve_month_ago": (today - datetime.timedelta(days=365)).strftime("%B %Y"),
            "six_month_ago": (today - datetime.timedelta(days=183)).strftime("%B %Y"),
            }
        def make_subst(entry):
            if isinstance(entry, dict) and isinstance(entry.get("title"), str):
                entry["title"] = entry["title"].format(**subst)
            return entry
        report["pages"] = [make_subst(entry) for entry in sReport["pages"]]

        write_json(report_settings_file, report, compact=False)
    return report_settings_file

# ----------------------------------------------------------------------

def find_previous_dir():
    for dd in sorted(Path("..").resolve().glob("*"), reverse=True):
        if dd.is_dir() and dd != Path(".").resolve():
            return str(dd)
    return None

# ----------------------------------------------------------------------

sReport = {
    "previous": None,
    "cover": {
        "hemisphere": "Northern",
        "meeting_date": "27 February - 2 March 2017",
        "teleconference": "",
        "year": "2017/2018",
        },
    "time_series": {
        "date": {"end": "2017-02-01", "start": "2016-08-01"},
        "period": "month",
        },
    "page_numbering": True,
    "pages": [
        {"type": "cover"},
        {"type": "toc"},
        {"type": "?************************* H1 *****************************"},
        {"type": "section_begin", "title": "H1N1pdm09", "subtype": "h1"},
        {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 geographic data"},
        {"type": "geographic_data_description", "coloring": "continents"},
        "new_page",
        {"type": "geographic_ts", "subtype": "H1"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "H1", "lab": "all"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H1", "assay": "HI", "lab": "all"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 phylogenetic tree"},
        {"type": "phylogenetic_description"},
        "new_page",
        {"type": "phylogenetic_tree", "subtype": "H1"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic map colored by phylogenetic clade"},
        {"type": "description", "text": "CDC+Crick+NIID+VIDRL antigenic map, antigens color-coded by phylogenetic clade."},
        {"type": "map", "subtype": "H1", "assay": "HI", "lab": "all", "map_type": "clade"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H1", "title": "H1N1pdm09 antigenic map with serology antigens."},
        {"type": "description", "text": "CDC+Crick+NIID+VIDRL antigenic map with serology antigens in orange, other antigens color-coded by phylogenetic clade."},
        {"type": "map", "subtype": "H1", "assay": "HI", "lab": "all", "map_type": "serology"},
        "new_page",
        {"type": "?************************* H3 *****************************"},
        {"type": "section_begin", "title": "H3N2", "subtype": "h3"},
        {"type": "subsection_begin", "subtype": "H1", "title": "H3N2 geographic data"},
        {"type": "geographic_data_description", "coloring": "h3_clade"},
        "new_page",
        {"type": "geographic_ts", "subtype": "H3"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "CDC H3N2 HI antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "H3", "lab": "CDC"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "HI", "lab": "CDC"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "CDC H3N2 Neut antigenic data"},
        {"type": "neut_ts_description", "coloring": "continents"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "NEUT", "lab": "CDC"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "Crick H3N2 HI antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "H3", "lab": "NIMR"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "HI", "lab": "NIMR"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "Crick H3N2 Neut antigenic data"},
        {"type": "neut_ts_description", "coloring": "continents"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "NEUT", "lab": "NIMR"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "NIID H3N2 Neut antigenic data"},
        {"type": "neut_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "H3", "lab": "NIID"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "NEUT", "lab": "NIID"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "VIDRL H3N2 HI antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "H3", "lab": "MELB"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "HI", "lab": "MELB"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "VIDRL H3N2 Neut antigenic data"},
        {"type": "neut_ts_description", "coloring": "continents"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "H3", "assay": "NEUT", "lab": "MELB"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 phylogenetic tree"},
        {"type": "phylogenetic_description"},
        "new_page",
        {"type": "phylogenetic_tree", "subtype": "H3"},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 antigenic maps colored by geography"},
        {"type": "maps", "images": [
            "h3-hi/geography-cdc.pdf", "h3-neut/geography-cdc.pdf",
            "h3-hi/geography-nimr.pdf", "h3-neut/geography-nimr.pdf",
            "", "h3-neut/geography-niid.pdf",
            "h3-hi/geography-melb.pdf", "h3-neut/geography-melb.pdf",
            ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 antigenic maps colored by phylogenetic clade"},
        {"type": "maps", "images": [
            "h3-hi/clade-cdc.pdf", "h3-neut/clade-cdc.pdf",
            "h3-hi/clade-nimr.pdf", "h3-neut/clade-nimr.pdf",
            "", "h3-neut/clade-niid.pdf",
            "h3-hi/clade-melb.pdf", "h3-neut/clade-melb.pdf",
            ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 antigenic maps colored by phylogenetic clade (since {twelve_month_ago})"},
        {"type": "maps", "images": [
            "h3-hi/clade-12m-cdc.pdf", "h3-neut/clade-12m-cdc.pdf",
            "h3-hi/clade-12m-nimr.pdf", "h3-neut/clade-12m-nimr.pdf",
            "", "h3-neut/clade-12m-niid.pdf",
            "h3-hi/clade-12m-melb.pdf", "h3-neut/clade-12m-melb.pdf",
            ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 antigenic maps colored by phylogenetic clade (since {six_month_ago})"},
        {"type": "maps", "images": [
            "h3-hi/clade-6m-cdc.pdf", "h3-neut/clade-6m-cdc.pdf",
            "h3-hi/clade-6m-nimr.pdf", "h3-neut/clade-6m-nimr.pdf",
            "", "h3-neut/clade-6m-niid.pdf",
            "h3-hi/clade-6m-melb.pdf", "h3-neut/clade-6m-melb.pdf",
            ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 antigenic maps colored by amino-acids at 131"},
        {"type": "maps", "images": [
            "h3-hi/aa-at-131-cdc.pdf", "h3-neut/aa-at-131-cdc.pdf",
            "h3-hi/aa-at-131-nimr.pdf", "h3-neut/aa-at-131-nimr.pdf",
            "", "h3-neut/aa-at-131-niid.pdf",
            "h3-hi/aa-at-131-melb.pdf", "h3-neut/aa-at-131-melb.pdf"
        ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "H3", "title": "H3N2 antigenic maps with serology antigens"},
        {"type": "maps", "images": [
            "h3-hi/serology-cdc.pdf", "h3-neut/serology-cdc.pdf",
            "h3-hi/serology-nimr.pdf", "h3-neut/serology-nimr.pdf",
            "", "h3-neut/serology-niid.pdf",
            "h3-hi/serology-melb.pdf", "h3-neut/serology-melb.pdf",
            ]},
        "new_page",
        {"type": "?************************* B *****************************"},
        {"type": "section_begin", "title": "B", "subtype": "b"},
        {"type": "subsection_begin", "subtype": "b", "title": "B Victoria and Yamagata geographic data"},
        {"type": "geographic_data_description", "coloring": "b_lineage_vic_deletion_mutants"},
        "new_page",
        {"type": "geographic_ts", "subtype": "b"},
        "new_page",
        {"type": "?************************* B/Vic *****************************"},
        {"type": "section_begin", "title": "B/Vic"},
        {"type": "subsection_begin", "subtype": "bvic", "title": "CDC B/Vic antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "bvic", "lab": "CDC"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "bvic", "assay": "HI", "lab": "CDC"},
        "new_page",
        {"type": "subsection_begin", "subtype": "bvic", "title": "Crick B/Vic antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "bvic", "lab": "NIMR"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "bvic", "assay": "HI", "lab": "NIMR"},
        "new_page",
        {"type": "subsection_begin", "subtype": "bvic", "title": "NIID B/Vic antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "bvic", "lab": "NIID"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "bvic", "assay": "HI", "lab": "NIID"},
        "new_page",
        {"type": "subsection_begin", "subtype": "bvic", "title": "VIDRL B/Vic antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "bvic", "lab": "MELB"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "bvic", "assay": "HI", "lab": "MELB"},
        "new_page",
        {"type": "subsection_begin", "subtype": "bvic", "title": "B/Vic phylogenetic tree"},
        {"type": "phylogenetic_description"},
        {"type": "phylogenetic_description_bvic_del"},
        "new_page",
        {"type": "phylogenetic_tree", "subtype": "bvic"},
        "new_page",
        {"type": "subsection_begin", "subtype": "bvic", "title": "B/Vic antigenic maps colored by phylogenetic clade"},
        {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps, antigens color-coded by phylogenetic clade."},
        {"type": "maps", "images": [
            "bvic-hi/clade-cdc.pdf", "bvic-hi/clade-nimr.pdf",
            "bvic-hi/clade-niid.pdf", "bvic-hi/clade-melb.pdf"
            ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "bvic", "title": "B/Vic antigenic maps with serology antigens"},
        {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps with serology antigens in orange, other antigens color-coded by phylogenetic clade."},
        {"type": "maps", "images": [
            "bvic-hi/serology-cdc.pdf", "bvic-hi/serology-nimr.pdf",
            "bvic-hi/serology-niid.pdf", "bvic-hi/serology-melb.pdf"
            ]},
        "new_page",
        {"type": "?************************* B/Yam *****************************"},
        {"type": "section_begin", "title": "B/Yam"},
        {"type": "subsection_begin", "subtype": "byam", "title": "CDC B/Yam antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "byam", "lab": "CDC"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "byam", "assay": "HI", "lab": "CDC"},
        "new_page",
        {"type": "subsection_begin", "subtype": "byam", "title": "Crick B/Yam antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "byam", "lab": "NIMR"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "byam", "assay": "HI", "lab": "NIMR"},
        "new_page",
        {"type": "subsection_begin", "subtype": "byam", "title": "NIID B/Yam antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "byam", "lab": "NIID"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "byam", "assay": "HI", "lab": "NIID"},
        "new_page",
        {"type": "subsection_begin", "subtype": "byam", "title": "VIDRL B/Yam antigenic data"},
        {"type": "antigenic_ts_description", "coloring": "continents"},
        {"type": "statistics_table", "subtype": "byam", "lab": "MELB"},
        "new_page",
        {"type": "antigenic_ts", "subtype": "byam", "assay": "HI", "lab": "MELB"},
        "new_page",
        {"type": "subsection_begin", "subtype": "byam", "title": "B/Yam phylogenetic tree"},
        {"type": "phylogenetic_description"},
        "new_page",
        {"type": "phylogenetic_tree", "subtype": "byam"},
        "new_page",
        {"type": "subsection_begin", "subtype": "byam", "title": "B/Yam antigenic maps colored by phylogenetic clade"},
        {"type": "description", "text": "CDC, Crick, NIID, VIDRL antigenic maps, antigens color-coded by phylogenetic clade."},
        {"type": "maps", "images": [
            "byam-hi/clade-cdc.pdf", "byam-hi/clade-nimr.pdf",
            "byam-hi/clade-niid.pdf", "byam-hi/clade-melb.pdf"
            ]},
        "new_page",
        {"type": "subsection_begin", "subtype": "byam", "title": "B/Yam antigenic maps with serology antigens"},
        {"type": "description", "text": "Top row left to right CDC, Crick, bottom row left to right NIID, VIDRL antigenic maps with serology antigens in orange, other antigens color-coded by phylogenetic clade."},
        {"type": "maps", "images": [
            "byam-hi/serology-cdc.pdf", "byam-hi/serology-nimr.pdf",
            "byam-hi/serology-niid.pdf", "byam-hi/serology-melb.pdf"
            ]},
        "new_page",
        "?appendices",
        "?serum_circle_description",
        ],
    }

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
