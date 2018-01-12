import sys, os, json, subprocess
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

from .charts import get_chart

# ======================================================================

sLabDisplayName = {"CDC": "CDC", "CNIC": "CNIC", "NIMR": "Crick", "NIID": "NIID", "MELB": "VIDRL", "ALL": "CDC+Crick+NIID+VIDRL"}

sApplyFor = {
    "pre": [
        "{lab}_pre",
        "{lab}_flip",
        "{lab}_rotate",
        "{lab}_viewport",
        "all_grey",
        "egg",
        ],
    "post": [
        "{lab}_mid",
        "{lab}_vaccines",
        "set_scale",
        "set_legend",
        "{lab}_post",
        ],
    "post_information": [
        "{lab}_mid",
        "{lab}_vaccines_information",
        "{lab}_post",
        ],
    "clade": [
        {"N": "clades", "size": 8}
        ],
    "clade_6m": [
        {"N": "clades_last_6_months", "size": 8}
        ],
    "clade_12m": [
        {"N": "clades_last_12_months", "size": 8}
        ],
    "geography": [
        {"N": "continents", "size": 8}
        ],
    "serology": [
        {"N": "clades_light", "size": 8},
        "serology",
        ],
    "information": [
        "information",
        {"N": "legend", "show": False}
        ],
    "serum_sectors": [
        {"N": "clades", "size": 8},
        "serum_sectors",
        ],
    "serum_coverage_hk": [
        {"N": "clades", "size": 8},
        "serum_coverage_hk",
        ],
    "ts_pre": [
        {"N": "continents"},
        {"N": "antigens", "select": "reference", "outline": "grey80", "fill": "transparent"},
        {"N": "antigens", "select": "test", "show": False},
        ],
}

sTitleFor = {
    "clade": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay} by clade",
        },
        "h1": {
            "hi":   "{lab} {virus_type} by clade",
        },
        "bvic": {
            "hi":   "{lab} {virus_type} by clade",
        },
        "byam": {
            "hi":   "{lab} {virus_type} by clade",
        },
    },
    "clade_6m": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay} by clade",
        },
        "h1": {
            "hi":   "{lab} {virus_type} by clade",
        },
        "bvic": {
            "hi":   "{lab} {virus_type} by clade",
        },
        "byam": {
            "hi":   "{lab} {virus_type} by clade",
        },
    },
    "clade_12m": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay} by clade",
        },
        "h1": {
            "hi":   "{lab} {virus_type} by clade",
        },
        "bvic": {
            "hi":   "{lab} {virus_type} by clade",
        },
        "byam": {
            "hi":   "{lab} {virus_type} by clade",
        },
    },
    "geography": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by geography",
            "neut": "{lab} {virus_type} {assay} by geography",
        },
        "h1": {
            "hi":   "{lab} {virus_type} by geography",
        },
        "bvic": {
            "hi":   "{lab} {virus_type} by geography",
        },
        "byam": {
            "hi":   "{lab} {virus_type} by geography",
        },
    },
    "serology": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} with serology antigens",
            "neut": "{lab} {virus_type} {assay} with serology antigens",
        },
        "h1": {
            "hi":   "{lab} {virus_type} with serology antigens",
        },
        "bvic": {
            "hi":   "{lab} {virus_type} with serology antigens",
        },
        "byam": {
            "hi":   "{lab} {virus_type} with serology antigens",
        },
    },
    "serum_sectors": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay}",
            "neut": "{lab} {virus_type} {assay}",
        },
        "h1": {
            "hi":   "{lab} {virus_type}",
        },
    },
    "serum_coverage_hk": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay}",
            "neut": "{lab} {virus_type} {assay}",
        },
        "h1": {
            "hi":   "{lab} {virus_type}",
        },
    },
    "ts": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} {period_name}",
            "neut": "{lab} {virus_type} {assay} {period_name}",
        },
        "h1": {
            "hi":   "{lab} {virus_type} {period_name}",
        },
        "bvic": {
            "hi":   "{lab} {virus_type} {period_name}",
        },
        "byam": {
            "hi":   "{lab} {virus_type} {period_name}",
        },
    },
}

# ======================================================================

sDirsForIndex = set()

def make_map(output_dir, prefix, virus_type, assay, mod, force, settings_labs_key="labs"):
    s1_filename = Path("{}-{}.json".format(virus_type, assay)).resolve()
    settings = json.load(s1_filename.open())
    for lab in settings[settings_labs_key]:
        module_logger.info("{}\nINFO:{} {} {} {} {}\nINFO: {}".format("*"* 70, " " * 30, lab, virus_type.upper(), assay.upper(), mod, " "* 93))
        output_prefix = prefix + "-" + lab.lower()

        s2_filename = output_dir.joinpath(output_prefix + ".settings.json")
        pre, post = make_pre_post(virus_type=virus_type, assay=assay, mod=mod, lab=lab)
        json.dump({"apply": pre + sApplyFor[mod] + post}, s2_filename.open("w"), indent=2)

        script_filename = output_dir.joinpath(output_prefix + ".sh")
        script_filename.open("w").write("#! /bin/bash\nexec ad map-draw --db-dir {pwd}/db -v -s '{s1}' -s '{s2}' '{chart}' '{output}'\n".format(
            s1=s1_filename, s2=s2_filename,
            pwd=os.getcwd(), chart=get_chart(virus_type=virus_type, assay=assay, lab=lab), output=output_dir.joinpath(output_prefix + ".pdf")))
        script_filename.chmod(0o700)
        subprocess.check_call(str(script_filename))
    sDirsForIndex.add(output_dir)

# ----------------------------------------------------------------------

sCompareWithPrevious = {
    True: [{"N": "antigens", "select": {"test": True}, "size": 5, "order": "raise"},
           {"N": "antigens", "select": {"test": True, "not_found_in_previous": True}, "size": 8, "order": "raise"}],
    False: [{"N": "antigens", "select": {"test": True}, "size": 8, "order": "raise"}]
    }

def make_ts(output_dir, virus_type, assay, force):
    report_settings = json.load(Path("report.json").open())
    periods = make_periods(start=report_settings["time_series"]["date"]["start"], end=report_settings["time_series"]["date"]["end"], period=report_settings["time_series"]["period"])
    s1_filename = Path("{}-{}.json".format(virus_type, assay)).resolve()
    settings = json.load(s1_filename.open())
    for lab in settings["labs"]:

        if report_settings["cover"]["teleconference"]:
            previous_chart = None
            compare_with_previous = sCompareWithPrevious[False]
            try:
                previous_chart = get_chart(virus_type=virus_type, assay=assay, lab=lab, chart_dir=Path(report_settings["previous"], "merges"))
                compare_with_previous = sCompareWithPrevious[True]
            except:
                module_logger.warning("No previous chart found for {} {} {} in {}".format(virus_type, assay, lab, Path(report_settings["previous"], "merges")))

        for period in periods:
            module_logger.info("{}\nINFO:{} {} {} {} Time Series {} {}".format("*"* 70, " " * 30, lab, virus_type.upper(), assay.upper(), period.numeric_name(), " "* 93))
            output_prefix = "ts-" + lab.lower() + "-" + period.numeric_name()

            s2_filename = output_dir.joinpath(output_prefix + ".settings.json")
            pre, post = make_pre_post(virus_type=virus_type, assay=assay, mod='ts', lab=lab, period_name=period.text_name())
            ts = [{"N": "antigens", "select": {"test": True, "date_range": [period.first_date(), period.after_last_date()]}, "show": True}]
            json.dump({"apply": pre + sApplyFor["ts_pre"] + compare_with_previous + ts + post}, s2_filename.open("w"), indent=2)

            script_filename = output_dir.joinpath(output_prefix + ".sh")
            script_filename.open("w").write("#! /bin/bash\nexec ad map-draw --db-dir {pwd}/db -v -s '{s1}' -s '{s2}' {previous_chart} '{chart}' '{output}'\n".format(
                s1=s1_filename,
                s2=s2_filename,
                chart=get_chart(virus_type=virus_type, assay=assay, lab=lab),
                previous_chart="--previous '{}'".format(previous_chart) if previous_chart else "",
                pwd=os.getcwd(),
                output=output_dir.joinpath(output_prefix + ".pdf")))
            script_filename.chmod(0o700)
            subprocess.check_call(str(script_filename))

# ----------------------------------------------------------------------

def make_periods(start, end, period):
    if period == "month":
        from acmacs_map_draw_backend import MonthlyTimeSeries
        ts = MonthlyTimeSeries(start=start, end=end)
    elif period == "year":
        from acmacs_map_draw_backend import YearlyTimeSeries
        ts = YearlyTimeSeries(start=start, end=end)
    elif period == "week":
        from acmacs_map_draw_backend import WeeklyTimeSeries
        ts = WeeklyTimeSeries(start=start, end=end)
    else:
        raise ValueError("Unsupported period: " + repr(period) + ", expected \"month\", \"year\", \"week\"")
    return ts

# ----------------------------------------------------------------------

def make_pre_post(virus_type, assay, mod, lab, period_name=None):
    if mod == "information":
        return (
            [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["pre"]],
            [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["post_information"]]
            )
    else:
        title = {
            "N": "title",
            "background": "transparent",
            "border_width": 0,
            "text_size": 24,
            "font_weight": "bold",
            "display_name": [sTitleFor[mod][virus_type][assay].format(lab=sLabDisplayName[lab], virus_type=virus_type.upper(), assay=assay.upper(), period_name=period_name)],
        }
        return (
            [title] + [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["pre"]],
            [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["post"]]
            )

# ----------------------------------------------------------------------

def make_map_information(output_dir, virus_type, assay, force):
    make_map(output_dir=output_dir, prefix=virus_type + "-" + assay, virus_type=virus_type, assay=assay, mod="information", force=force, settings_labs_key="information_labs")

# ----------------------------------------------------------------------

def make_index_html():
    for output_dir in sDirsForIndex:
        if output_dir.name != "information":
            module_logger.info('making html index in {}'.format(output_dir))
            for safari in [False, True]:
                with output_dir.joinpath("index{}.html".format(".safari" if safari else "")).open("w") as f:
                    title = "{} {}".format(output_dir.name.upper(), output_dir.parent.name)
                    f.write("""<html><head>
                            <style>
                              ul {list-style-type: none;}
                              li {margin: 0.5em 0; }
                              object {width: 800px; height: 815px;}
                              td {vertical-align: top; border-bottom: 1px solid grey; padding-bottom: 1em;}
                              td.vaccine-data {padding-left: 1em;}
                              td.vaccine-data div {height: 815px; overflow: auto; white-space: nowrap;}
                              .vaccine-report { font-size: 1em; }
                              .vaccine-title { display: none; }
                              .vaccine-chosen { padding-left: 1em; font-weight: bold; }
                              .vaccine-header { }
                              .antigen-name { padding-left: 1em; }
                              .serum-name { padding-left: 3em; }
                            </style>
                            <title>%(title)s</title></head><body>\n""" % {"title": title})
                    # img {border: 1px solid black;}
                    for filename in sorted(output_dir.glob("*.pdf")):
                        f.write("<h3>{} {}</h3>\n".format(output_dir.name.upper(), filename.stem))
                        if safari:
                            f.write('<img src="{}" />\n'.format(filename.name))
                        else:
                            f.write('<table><tbody><tr>\n<td><object data="{}#toolbar=0"></object></td>\n'.format(filename.name)) # toolbar=0 is for chrome
                        vaccine_data_file = output_dir.joinpath(filename.stem + ".vaccines.html")
                        if vaccine_data_file.exists():
                            f.write("<td class=\"vaccine-data\"><div>" + vaccine_data_file.open().read() + "</div></td>")
                        f.write("</tr></tbody></table>\n")
                    f.write("</body></html>\n")

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
