import sys, os, json, subprocess
import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path

from .charts import get_chart

# ======================================================================

sLabDisplayName = {"CDC": "CDC", "CNIC": "CNIC", "NIMR": "Crick", "NIID": "NIID", "MELB": "VIDRL"}

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
    },
    "clade_6m": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay} by clade",
        },
    },
    "clade_12m": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by clade",
            "neut": "{lab} {virus_type} {assay} by clade",
        },
    },
    "geography": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} by geography",
            "neut": "{lab} {virus_type} {assay} by geography",
        },
    },
    "serology": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} with serology antigens",
            "neut": "{lab} {virus_type} {assay} with serology antigens",
        },
    },
    "serum_sectors": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay}",
            "neut": "{lab} {virus_type} {assay}",
        },
    },
    "serum_coverage_hk": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay}",
            "neut": "{lab} {virus_type} {assay}",
        },
    },
    "ts": {
        "h3": {
            "hi":   "{lab} {virus_type} {assay} {period_name}",
            "neut": "{lab} {virus_type} {assay} {period_name}",
        },
    },
}

# ======================================================================

def make_map(output_dir, prefix, virus_type, assay, mod, force):
    s1_filename = Path("{}-{}.json".format(virus_type, assay)).resolve()
    settings = json.load(s1_filename.open())
    for lab in settings["labs"]:
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

# ----------------------------------------------------------------------

def make_ts(output_dir, virus_type, assay, force):
    report_settings = json.load(Path("report.json").open())
    periods = make_periods(start=report_settings["time_series"]["date"]["start"], end=report_settings["time_series"]["date"]["end"], period=report_settings["time_series"]["period"])
    if report_settings["cover"]["teleconference"]:
        compare_with_previous = [{"N": "antigens", "select": {"test": True}, "size": 5, "order": "raise"},
                                     {"N": "antigens", "select": {"test": True, "not_found_in_previous": True}, "size": 8, "order": "raise"}]
    else:
        compare_with_previous = [{"N": "antigens", "select": {"test": True}, "size": 8, "order": "raise"}]
    s1_filename = Path("{}-{}.json".format(virus_type, assay)).resolve()
    settings = json.load(s1_filename.open())
    for lab in settings["labs"]:
        for period in periods:
            module_logger.info("{}\nINFO:{} {} {} {} Time Series: {}".format("*"* 70, " " * 30, lab, virus_type.upper(), assay.upper(), " "* 93))
            output_prefix = "ts-" + lab.lower() + "-" + period.numeric_name()

            s2_filename = output_dir.joinpath(output_prefix + ".settings.json")
            pre, post = make_pre_post(virus_type=virus_type, assay=assay, mod='ts', lab=lab, period_name=period.text_name())
            ts = [{"N": "antigens", "select": {"test": True, "date_range": [period.first_date(), period.after_last_date()]}, "show": True}]
            json.dump({"apply": pre + sApplyFor["ts_pre"] + compare_with_previous + ts + post}, s2_filename.open("w"), indent=2)

            script_filename = output_dir.joinpath(output_prefix + ".sh")
            script_filename.open("w").write("#! /bin/bash\nexec ad map-draw --db-dir {pwd}/db -v -s '{s1}' -s '{s2}' --previous '{previous_chart}' '{chart}' '{output}'\n".format(
                s1=s1_filename,
                s2=s2_filename,
                chart=get_chart(virus_type=virus_type, assay=assay, lab=lab),
                previous_chart=get_chart(virus_type=virus_type, assay=assay, lab=lab, chart_dir=Path(report_settings["previous"], "merges")),
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

def make_map_information(output_dir, prefix, virus_type, assay, mod):
    raise NotImplementedError()

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
