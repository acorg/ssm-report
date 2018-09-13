import sys, os, json, subprocess, pprint
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

from .charts import get_chart

# ======================================================================

sLogDelimiter = "*" * 70
def n_spaces(n):
    return " " * n

sLabDisplayName = {"CDC": "CDC", "CNIC": "CNIC", "NIMR": "Crick", "NIID": "NIID", "MELB": "VIDRL", "ALL": "CDC+Crick+NIID+VIDRL"}

sApplyFor = {
    "pre": [
        "{lab}_pre",
        "{lab}_flip",
        "{lab}_rotate",
        "{lab}_viewport",
        "all_grey",
        "egg",
        "lower_reference",
        ],
    "post": [
        "{lab}_mid",
        "{lab}_vaccines",
        "set_scale",
        "{lab}_post",
        ],
    "post_information": [
        "{lab}_mid",
        "{lab}_vaccines_information",
        "{lab}_post",
        ],
    "clade": [
        {"N": "clades", "size": 8},
        "*{lab}_clades",
        "set_legend"
        ],
    "clade_6m": [
        {"N": "clades_last_6_months", "size": 8},
        "*{lab}_clades_last_6_months",
        "set_legend"
        ],
    "clade_12m": [
        {"N": "clades_last_12_months", "size": 8},
        "*{lab}_clades_last_12_months",
        "set_legend"
        ],
    "geography": [
        {"N": "continents", "size": 8}
        ],
    "serology": [
        {"N": "clades_light", "size": 8},
        "*serology",
        "set_legend"
        ],
    "information": [
        "information",
        {"N": "legend", "show": False}
        ],
    "serum_sectors": [
        {"N": "clades", "size": 8},
        "serum_sectors",
        ],
    "serum_coverage_circle": [
        {"N": "clades_light", "size": 8},
        ],
    "ts_pre": [
        {"N": "continents"},
        {"N": "antigens", "select": "reference", "outline": "grey80", "fill": "transparent"},
        {"N": "antigens", "select": "test", "show": False},
        ],
    "ts_post": [
        "no_legend"
        ],
    None: []
}

sTitleFor = {
    "clade": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay}{infix} by clade",
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
            "neut": "{lab} {virus_type} {assay}{infix} by clade",
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
            "neut": "{lab} {virus_type} {assay}{infix} by clade",
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
    "aa_at_142": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by amino-acids at 142",
            "neut": "{lab} {virus_type} {assay}{infix} by amino-acids at 142",
        }
    },
    "geography": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by geography",
            "neut": "{lab} {virus_type} {assay}{infix} by geography",
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
            "neut": "{lab} {virus_type} {assay}{infix} with serology antigens",
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
    "serum_coverage": {
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

def make_map(output_dir, prefix, virus_type, assay, mod, force, lab=None, settings_labs_key="labs", open_image=None):
    settings_files = list(Path(".").glob(f"*{virus_type}-{assay}.json"))
    labs = [lab] if lab else json.load(settings_files[0].open())[settings_labs_key]
    for lab in labs:
        make_map_for_lab(output_dir=output_dir, prefix=prefix, virus_type=virus_type, assay=assay, lab=lab, mod=mod, settings_files=settings_files, open_image=open_image)
    sDirsForIndex.add(output_dir)

# ----------------------------------------------------------------------

def make_map_for_lab(output_dir, prefix, virus_type, assay, lab, mod, settings_files, infix="", open_image=None):
    infix = infix or ""
    chart = get_chart(virus_type=virus_type, assay=assay, lab=lab, infix=infix)
    module_logger.info(f"{sLogDelimiter}\nINFO:{n_spaces(30)} {lab.upper()} {virus_type.upper()} {assay.upper()} {infix} {mod}\nINFO: {n_spaces(93)}")
    output_prefix = f"{prefix}-{lab.lower()}{infix}"

    s2_filename = output_dir.joinpath(output_prefix + ".settings.json")
    pre, post = make_pre_post(virus_type=virus_type, assay=assay, mod=mod, lab=lab.upper(), infix=infix)
    if mod == "serology":
        inside = [lab.upper() + "_serology"]
    elif "serum_coverage_circle" in mod:
        inside = sApplyFor["serum_coverage_circle"] + [mod]
        mod = None
    elif mod == "aa_at_142":
        inside = ["*" + lab.upper() + "_aa_at_142"]
    else:
        inside = []
    for_mod = [e.format(virus_type=virus_type, assay=assay.upper(), mod=mod, lab=lab.upper()) if isinstance(e, str) else e for e in sApplyFor.get(mod, [mod])]
    json.dump({"apply": pre + for_mod + inside + post}, s2_filename.open("w"), indent=2)

    script_filename = output_dir.joinpath(output_prefix + ".sh")
    settings_args = " ".join("-s '{}'".format(filename) for filename in (settings_files + [s2_filename]))
    output = output_dir.joinpath(output_prefix + ".pdf")
    script_filename.open("w").write("#! /bin/bash\nexec ad map-draw --db-dir {pwd}/db -v {settings_args} '{chart}' '{output}'\n".format(
        settings_args=settings_args, pwd=os.getcwd(), chart=chart, output=output))
    script_filename.chmod(0o700)
    subprocess.check_call(str(script_filename))
    if open_image == "quicklook":
        subprocess.Popen(["/usr/bin/qlmanage", "-p", output], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif open_image == "open":
        subprocess.Popen(["/usr/bin/open", output], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ----------------------------------------------------------------------

sCompareWithPrevious = {
    True: [{"N": "antigens", "select": {"test": True}, "size": 5, "order": "raise"},
           {"N": "antigens", "select": {"test": True, "not_found_in_previous": True}, "size": 8, "order": "raise"}],
    False: [{"N": "antigens", "select": {"test": True}, "size": 8, "order": "raise"}]
    }

def make_ts(output_dir, virus_type, assay, lab, infix="", force=None):
    report_settings = json.load(Path("report.json").open())
    periods = make_periods(start=report_settings["time_series"]["date"]["start"], end=report_settings["time_series"]["date"]["end"], period=report_settings["time_series"]["period"])
    settings_files = list(Path(".").glob(f"*{virus_type}-{assay}.json"))
    labs = [lab] if lab else json.load(Path("{}-{}.json".format(virus_type, assay)).resolve().open())["labs"]
    for lab in labs:
        compare_with_previous = sCompareWithPrevious[False]
        previous_chart = None
        if report_settings["cover"]["teleconference"]:
            try:
                previous_chart = get_chart(virus_type=virus_type, assay=assay, lab=lab, chart_dir=Path(report_settings["previous"], "merges"))
                compare_with_previous = sCompareWithPrevious[True]
            except:
                module_logger.warning("No previous chart found for {} {} {} in {}".format(virus_type, assay, lab, Path(report_settings["previous"], "merges")))

        for period in periods:
            module_logger.info("{}\nINFO:{} {} {} {} Time Series {} {}".format("*"* 70, " " * 30, lab, virus_type.upper(), assay.upper(), period["numeric_name"], " "* 93))
            output_prefix = f"ts-{lab.lower()}{infix}-{period['numeric_name']}"

            s2_filename = output_dir.joinpath(f"{output_prefix}.settings.json")
            settings_args = " ".join("-s '{}'".format(filename) for filename in (settings_files + [s2_filename]))
            pre, post = make_pre_post(virus_type=virus_type, assay=assay, mod='ts', lab=lab.upper(), period_name=period["text_name"], infix=infix)
            ts = [{"N": "antigens", "select": {"test": True, "date_range": [period["first_date"], period["after_last_date"]]}, "show": True}]
            json.dump({"apply": pre + sApplyFor["ts_pre"] + compare_with_previous + ts + sApplyFor["ts_post"] + post}, s2_filename.open("w"), indent=2)

            script_filename = output_dir.joinpath(output_prefix + ".sh")
            script_filename.open("w").write("#! /bin/bash\nexec ad map-draw --db-dir {pwd}/db -v {settings_args} {previous_chart} '{chart}' '{output}'\n".format(
                settings_args=settings_args,
                chart=get_chart(virus_type=virus_type, assay=assay, lab=lab, infix=infix),
                previous_chart="--previous '{}'".format(previous_chart) if previous_chart else "",
                pwd=os.getcwd(),
                output=output_dir.joinpath(output_prefix + ".pdf")))
            script_filename.chmod(0o700)
            subprocess.check_call(str(script_filename))
    sDirsForIndex.add(output_dir)

# ----------------------------------------------------------------------

def make_periods(start, end, period):
    data = json.loads(subprocess.check_output("ad time-series-gen {period}ly {start} {end}".format(period=period, start=start, end=end), shell=True))
    # pprint.pprint(data)
    return data

# def make_periods(start, end, period):
#     if period == "month":
#         from acmacs_map_draw_backend import MonthlyTimeSeries
#         ts = MonthlyTimeSeries(start=start, end=end)
#     elif period == "year":
#         from acmacs_map_draw_backend import YearlyTimeSeries
#         ts = YearlyTimeSeries(start=start, end=end)
#     elif period == "week":
#         from acmacs_map_draw_backend import WeeklyTimeSeries
#         ts = WeeklyTimeSeries(start=start, end=end)
#     else:
#         raise ValueError("Unsupported period: " + repr(period) + ", expected \"month\", \"year\", \"week\"")
#     return ts

# ----------------------------------------------------------------------

def make_pre_post(virus_type, assay, mod, lab, infix=None, period_name=None):
    if mod == "information":
        return (
            [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["pre"]],
            [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["post_information"]],
            )
    else:
        if "serum_coverage_circle" in mod:
            title_format = sTitleFor["serum_coverage"][virus_type][assay]
        else:
            title_format = sTitleFor[mod][virus_type][assay]
        if infix == "-oseltamivir":
            infix = " with oseltamivir"
        else:
            infix = ""
        title = {
            "N": "title",
            "background": "transparent",
            "border_width": 0,
            "text_size": 24,
            "font_weight": "bold",
            "display_name": [title_format.format(lab=sLabDisplayName[lab], virus_type=virus_type.upper(), assay=assay.upper(), period_name=period_name, infix=infix)],
        }
        return (
            [title] + [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["pre"]],
            [e.format(virus_type=virus_type, assay=assay, mod=mod, lab=lab, period_name=period_name) for e in sApplyFor["post"]]
            )

# ----------------------------------------------------------------------

def make_map_information(output_dir, virus_type, assay, force):
    make_map(output_dir=output_dir, prefix=virus_type + "-" + assay, virus_type=virus_type, assay=assay, mod="information", force=force, settings_labs_key="information_labs")

# ----------------------------------------------------------------------

sHead = """<html>
<head>
  <style>
    ul {list-style-type: none;}
    li {margin: 0.5em 0; }
    object {width: %(width)dpx; height: %(height)dpx;}
    img {width: %(width)dpx;}
    td {vertical-align: top; border-bottom: 1px solid grey; padding-bottom: 1em;}
    td.vaccine-data {padding-left: 1em;}
    td.vaccine-data div {height: 815px; overflow: auto; white-space: nowrap;}
    .vaccine-report { font-size: 1em; }
    .vaccine-title { display: none; }
    .vaccine-chosen { padding-left: 1em; font-weight: bold; }
    .vaccine-header { }
    .antigen-name { padding-left: 1em; }
    .serum-name { padding-left: 3em; }

    table.serum-coverage td { vertical-align: middle; border: none; padding: 0.5em; }
  </style>
  <title>%(title)s</title>
</head>
<body>
  <h2>%(title)s</h2>
"""

def make_index_html():
    # module_logger.info("make_index_html {}".format(sDirsForIndex))
    for output_dir in sDirsForIndex:
        if output_dir.name != "information":
            module_logger.info('making html index in {}'.format(output_dir))
            for safari in [False, True]:
                with output_dir.joinpath("index{}.html".format(".safari" if safari else "")).open("w") as f:
                    title = "{} {}".format(output_dir.name.upper(), output_dir.parent.name)
                    f.write(sHead % {"title": title, "width": 800, "height": 815})
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

def make_index_clade_html(output_dir):
    for safari in [False, True]:
        index_filename = Path(output_dir, "index-clade{}.html".format(".safari" if safari else ""))
        module_logger.info('making html clade index: {}'.format(index_filename))
        with index_filename.open("w") as f:
            f.write(sHead % {"title": "By Clade", "width": 800, "height": 815})
            # img {border: 1px solid black;}
            for filename in sorted(Path(".").glob("*/clade-[acmn]*.pdf")):
                f.write("<h3>{} {}</h3>\n".format(filename.parent.name.upper(), filename.stem))
                if safari:
                    f.write('<img src="{}" />\n'.format(filename))
                else:
                    f.write('<table><tbody><tr>\n<td><object data="{}#toolbar=0"></object></td>\n'.format(filename)) # toolbar=0 is for chrome
                f.write("</tr></tbody></table>\n")
            f.write("</body></html>\n")

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
