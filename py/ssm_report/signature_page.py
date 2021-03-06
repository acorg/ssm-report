import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import subprocess, datetime, copy, pprint, shutil

from acmacs_base.json import read_json, write_json
from .map import sLabDisplayName

sVirusTypeShort = {"A(H1N1)": "H1", "A(H3N2)": "H3", "BVIC": "B/Vic", "BYAM": "B/Yam", "h1": "H1", "h3": "H3", "bvic": "B/Vic", "byam": "B/Yam", "bv": "B/Vic", "by": "B/Yam"}
sVirusTypes = ["h1", "h3", "bv", "by"]

# ======================================================================

def signature_page_output_dir_init(sp_dir):
    index_file = Path(sp_dir, "index.html")
    if not index_file.exists():
        with index_file.open("w") as f:
            f.write(sIndex)

def signature_page_source_dir_init(sp_dir):
    sp_dir.mkdir(exist_ok=True)
    for subtype in sVirusTypes:
        for suff in [".tree.json.xz", ".tree.settings.json"]:
            sl = sp_dir.joinpath(subtype + suff)
            if not sl.is_symlink():
                sl.symlink_to(Path("..", "tree", sl.name))

# ======================================================================

def trees_get_from_albertine(tree_dir):
    albertine_dir = subprocess.check_output("ssh albertine ls -1d '/syn/eu/ac/results/whocc-tree/20*'", shell=True).decode("utf-8").strip().split("\n")[-1]
    for vt in sVirusTypes:
        subprocess_check_call("scp 'albertine:{albertine_dir}/{vt}/tree.json.xz' '{tree_dir}/{vt}.tree.json.xz'".format(albertine_dir=albertine_dir, vt=vt, tree_dir=tree_dir))

# ======================================================================

def tree_make(subtype, tree_dir, seqdb, output_dir=None, settings_infix="settings", tree_infix="", interactive=False, report_cumulative=False):
    if output_dir is None:
        output_dir = tree_dir
    else:
        output_dir.mkdir(exist_ok=True)
    tree = tree_dir.joinpath(f"{subtype}.tree.json.xz")
    pdf = output_dir.joinpath(f"{subtype}.tree{tree_infix}.pdf")
    settings = output_dir.joinpath(f"{subtype}.tree{tree_infix}.{settings_infix}.json")
    if not settings.exists():
        subprocess_check_call(f"~/AD/bin/sigp --seqdb '{seqdb}' --init-settings '{settings}' '{tree}' '{pdf}'")
        _tree_update_settings(subtype=subtype, settings=settings)
    sigp_cmd = f"""~/AD/bin/sigp --seqdb "{seqdb}" -s "{settings}" "{tree}" "{pdf}" --open"""
    if report_cumulative:
        sigp_cmd += " --report-cumulative -"
    edit_settings = f'/usr/local/bin/emacsclient -n "{settings}"'
    open_pdf = f'open "{pdf}"'
    if interactive:
        subprocess_check_call(f"""{open_pdf}; sleep 1; {edit_settings}; fswatch --latency=0.1 '{settings}' | xargs -L 1 -I % -R 0 /bin/bash -c 'tink; printf "\n\n> ====================================================================================================\n\n"; {sigp_cmd} || say failed; tink; {edit_settings}'""")
    else:
        subprocess_check_call(f"{sigp_cmd}; sleep 1; {edit_settings}")

# ----------------------------------------------------------------------

def tree_make_aa_pos(subtype, tree_dir, seqdb):
    tree = tree_dir.joinpath(f"{subtype}.tree.json.xz")
    pdf = tree_dir.joinpath(f"{subtype}.tree-aa-at-pos.pdf")
    settings = tree_dir.joinpath(f"{subtype}.tree-aa-at-pos.json")
    if not settings.exists():
        subprocess_check_call(f"~/AD/bin/sigp --seqdb '{seqdb}' --init-settings '{settings}' --show-aa-at-pos --aa-at-pos-hz-section-threshold 100 --not-show-hz-sections '{tree}' '{pdf}' --open")
    else:
        subprocess_check_call(f"~/AD/bin/sigp --seqdb '{seqdb}' -s '{settings}' '{tree}' '{pdf}' --open")

# ----------------------------------------------------------------------

def tree_make_information_settings(virus_type, tree_dir, output_dir):
    output_dir.mkdir(exist_ok=True)
    info_settings = output_dir.joinpath("{}.tree.information.json".format(virus_type))
    if not info_settings.exists():
        settings = read_json(tree_dir.joinpath("{}.tree.settings.json".format(virus_type)))
        for clade_data in settings["clades"]["clades"]:
            clade_data["show"] = False
        settings["title"]["title"] = ""
        settings["tree"]["aa_transition"]["per_branch"]["show"] = False
        settings["tree"]["aa_transition"]["show"] = False
        settings["tree"].update({
            "color_nodes": "continent",
            "force_line_width": True,
            # "label_style": {"family": "", "slant": "normal", "weight": "normal"},
            "line_color": "black",
            "line_width": 1.5,
            })
        for tree_mod in settings["tree"].get("mods", []):
            if tree_mod.get("mod") == "mark-with-label":
                tree_mod["?mod"] = tree_mod.pop("mod")
        for section in settings["hz_sections"]["sections"]:
            section["show_line"] = True
        write_json(info_settings, settings, object_fields_sorting_key=signature_page_settins_object_fields_sorting_key)

# ----------------------------------------------------------------------

def tree_report_first_last_leaves(subtype, tree_dir, seqdb):
    tree = tree_dir.joinpath(f"{subtype}.tree.json.xz")
    subprocess_check_call(f"tal --seqdb '{seqdb}' --first-last-leaves 10 -D whocc '{tree}'")

# ----------------------------------------------------------------------

def _tree_update_settings(subtype, settings):
    data = read_json(settings)
    data.pop("_", None)
    data["title"]["title"] = sVirusTypeShort[subtype]
    data["signature_page"].pop("antigenic_maps_width", None)
    data["signature_page"].pop("mapped_antigens_margin_right", None)
    data.pop("mapped_antigens", None)
    data.pop("antigenic_maps", None)
    for entry_by_aa_label in data["tree"]["aa_transition"]["per_branch"]["by_aa_label"]:
        for field in ["style", "color", "interline", "label_connection_line_color", "label_connection_line_width", "show", "size"]:
            entry_by_aa_label.pop(field, None)
    globals().get("_tree_update_settings_" + subtype)(data=data, settings=settings)
    # data["tree"]["ladderize"] = "max-edge-length"
    write_json(settings, data, object_fields_sorting_key=signature_page_settins_object_fields_sorting_key)

# ----------------------------------------------------------------------

def _tree_update_settings_bv(data, settings):
    report_settings = read_json("report.json")
    # data["signature_page"].update({"left": 50, "right": 0, "clades_width": 50})
    data["time_series"]["begin"] = (datetime.datetime.strptime(report_settings["time_series"]["date"]["end"], "%Y-%m-%d") - datetime.timedelta(days=25*30)).strftime("%Y-%m-01")
    # data["tree"]["mods"] = [
    #     {"mod": "hide-if-cumulative-edge-length-bigger-than", "d1": 0.0191},
    #     {"mod": "mark-clade-with-line", "clade": "2DEL2017", "color": "#A0A0A0", "line_width": 0.2},
    #     {"mod": "mark-clade-with-line", "clade": "3DEL2017", "color": "#606060", "line_width": 0.2},
    #     {"mod": "before2015-58P-or-146I-or-559I", "?": "hides 1B"},
    #     {"?mod": "hide-between", "s1": "B/SHANGHAI-BAOSHAN/193/2011__MDCK1/MDCK1", "s2": "B/SOUTH%20AUSTRALIA/18/2011__MDCK1"},
    #     {"?mod": "hide-between", "s1": "B/JIANGSU-JINGJIANG/33/2012__MDCK2/MDCK2", "s2": "B/PHILIPPINES/2533/2011__MDCK1"}
    #     ]
    for clade_data in data["clades"]["clades"]:
        clade_data["label_offset"] = [3, 0]
        if clade_data["name"] == "1A":
            clade_data["section-inclusion-tolerance"] = 20
        elif clade_data["name"] == "1":
            clade_data["show"] = False

def _tree_update_settings_by(data, settings):
    report_settings = read_json("report.json")
    # data["signature_page"].update({"left": 70, "right": 0, "clades_width": 50})
    data["time_series"]["begin"] = (datetime.datetime.strptime(report_settings["time_series"]["date"]["end"], "%Y-%m-%d") - datetime.timedelta(days=25*30)).strftime("%Y-%m-01")
    # data["tree"]["mods"] = [
    #     {"mod": "hide-if-cumulative-edge-length-bigger-than", "d1": 0.043},
    #     ]
    for clade_data in data["clades"]["clades"]:
        clade_data["label_offset"] = [5, 0]

def _tree_update_settings_h1(data, settings):
    pass
    # data["signature_page"].update({"left": 50, "right": 0, "clades_width": 100})
    # data["tree"]["mods"] = [
    #     {"mod": "hide-if-cumulative-edge-length-bigger-than", "d1": 0.021},
    #     ]
    # data["title"]["title"] = "A(H1N1)"
    # for clade_data in data["clades"]["clades"]:
    #     if clade_data["name"] == "6B":
    #         clade_data["slot"] = 4

def _tree_update_settings_h3(data, settings):
    pass
    # data["signature_page"].update({"left": 50, "right": 0, "clades_width": 160, "time_series_width": 250})
    # data["tree"]["mods"] = [
    #     {"mod": "hide-if-cumulative-edge-length-bigger-than", "d1": 0.04},
    #     ]
    # data["title"]["title"] = "A(H3N2)"
    # for clade_data in data["clades"]["clades"]:
    #     if clade_data["name"] == "3C.2A":
    #         clade_data["slot"] = 7

# ======================================================================

def signature_page_make(virus_type, assay, lab, sp_source_dir, sp_output_dir, tree_dir, merge_dir, seqdb, serum_circles=False, orig_sp_source_dir=None, colored_by_date=True, interactive=False):
    # module_logger.warning("Source {}  Output {}  Tree {}".format(sp_source_dir, sp_output_dir, tree_dir))
    prefix = "{}-{}-{}".format(virus_type, lab, assay)
    settings = sp_source_dir.joinpath(prefix + ".sigp.settings.json")
    if orig_sp_source_dir and not settings.exists():
        orig_settings = orig_sp_source_dir.joinpath(prefix + ".sigp.settings.json")
        if orig_settings.exists():
            shutil.copy(orig_settings, settings)
            _signature_page_update_settings(virus_type=virus_type, assay=assay, lab=lab, settings_file=settings, serum_circles=serum_circles, colored_by_date=colored_by_date, update_vaccines=False)
    tree = tree_dir.joinpath(virus_type + ".tree.json.xz")
    tree_settings = sp_source_dir.joinpath(virus_type + ".tree.settings.json")
    # chart = merge_dir.joinpath("{}-{}-{}.sdb.xz".format(lab, virus_type.replace("b", "b-").replace("h1", "h1pdm"), assay))
    chart = merge_dir.joinpath("{}-{}-{}.ace".format(lab, virus_type, assay))
    pdf = sp_output_dir.joinpath(prefix + ".pdf")
    if not settings.exists():
        no_draw = "--no-draw" if not interactive else ""
        subprocess_check_call(f"""~/AD/bin/sigp --seqdb "{seqdb}" --chart "{chart}" -s "{tree_settings}" {no_draw} --init-settings "{settings}" "{tree}" "{pdf}" """)
        _signature_page_update_settings(virus_type=virus_type, assay=assay, lab=lab, settings_file=settings, serum_circles=serum_circles, colored_by_date=colored_by_date)
    edit_settings = f'/usr/local/bin/emacsclient -n "{tree_settings}"; /usr/local/bin/emacsclient -n "{settings}"'
    subprocess_check_call(edit_settings)
    sigp_cmd = f"""~/AD/bin/sigp --seqdb "{seqdb}" --chart "{chart}" -s "{tree_settings}" -s "{settings}" "{tree}" "{pdf}" """ # --report-hz-section-antigens"""
    pdf_width = 1930
    open_pdf = f'~/bin/preview "{pdf.resolve()}" -p 70.0.{pdf_width}.{int(pdf_width * 0.63) + 50}'
    if interactive:
        subprocess_check_call(f"""{open_pdf}; {edit_settings}; fswatch --latency=0.1 '{settings}' "{tree_settings}" | xargs -L 1 -I % -R 0 /bin/bash -c 'tink; printf "\n\n> ====================================================================================================\n\n"; ( {sigp_cmd} && {open_pdf} ) || say failed; tink'""")
    else:
        subprocess_check_call(f"""{sigp_cmd}; {open_pdf}""")

# ----------------------------------------------------------------------

def _signature_page_update_settings(virus_type, assay, lab, settings_file, serum_circles, colored_by_date, update_vaccines=True):
    # module_logger.warning("_signature_page_update_settings {} {} {}".format(virus_type, assay, lab))
    settings = read_json(settings_file)
    del settings["_"]
    if virus_type == "h3":
        settings["title"]["title"] = "{} {} {}".format(sVirusTypeShort[virus_type], assay.upper(), sLabDisplayName[lab.upper()])
    else:
        settings["title"]["title"] = "{} {}".format(sVirusTypeShort[virus_type], sLabDisplayName[lab.upper()])
    settings.pop("clades", None)
    settings.pop("hz_sections", None)
    settings["time_series"] = {"month_year_to_timeseries_gap": 8}

    # enable/disable tracked serum
    # tracked_antigens fill: by_date
    for mod in settings["antigenic_maps"]["mods"]:
        if serum_circles:
            if isinstance(mod, dict):
                if mod.get("N") in ["?tracked_sera", "?tracked_serum_circles"]:
                    mod["N"] = mod["N"][1:]
                if mod.get("?N") in ["tracked_sera", "tracked_serum_circles"]:
                    mod["N"] = mod["?N"]
                    del mod["?N"]
                if mod.get("N") in ["tracked_serum_circles"]:
                    mod["outline"] = "passage"
        else:
            if isinstance(mod, dict) and mod.get("N") in ["tracked_sera", "tracked_serum_circles"]:
                mod["N"] = "?" + mod["N"]
        if isinstance(mod, dict) and mod.get("N") in ["tracked_antigens"] and colored_by_date:
            mod["fill"] = "by_date"
            mod["outline"] = "black"

    if virus_type in ["by"]:
        settings["antigenic_maps"]["columns"] = 2
    else:
        settings["antigenic_maps"]["columns"] = 3
    if virus_type in ["h3"]:
        settings["signature_page"]["antigenic_maps_width"] = 579
    else:
        settings["signature_page"]["antigenic_maps_width"] = 579

    if update_vaccines:
        # virus_type_long = virus_type.replace("v", "vic").replace("y", "yam")
        map_settings = read_json(f"{virus_type}-{assay}.json")
        vaccine_settings = read_json(f"vaccines.{virus_type}-{assay}.json")
        # update viewport from ssm settings
        _signature_page_update_viewport_rotate_flip(virus_type=virus_type, assay=assay, lab=lab, settings=settings, map_settings=map_settings)
        # update vaccine drawing from ssm settings
        _signature_page_update_vaccines(virus_type=virus_type, assay=assay, lab=lab, settings=settings, map_settings=map_settings, vaccine_settings=vaccine_settings)
        _signature_page_add_antigen_sample(virus_type=virus_type, assay=assay, lab=lab, settings=settings, map_settings=map_settings)

    write_json(settings_file, settings, object_fields_sorting_key=signature_page_settins_object_fields_sorting_key)

# ----------------------------------------------------------------------

def _signature_page_update_vaccines(virus_type, assay, lab, settings, map_settings, vaccine_settings):

    # remove old entries
    for index in sorted((no for no, mod in enumerate(settings["antigenic_maps"]["mods"]) if mod.get("N", mod.get("?N")) in ["antigens", "?antigens", "antigens?"] and mod.get("select", {}).get("vaccine")), reverse=True):
        del settings["antigenic_maps"]["mods"][index]

    # pprint.pprint(vaccine_settings)
    if vaccine_settings:
        vaccines = vaccine_settings["mods"].get(lab.upper() + "-vaccines")
        if vaccines is None:
            vaccines = vaccine_settings["mods"]["ALL-vaccines"]
    else:
        vaccines = map_settings["mods"][lab.upper() + "-vaccines"]
    # pprint.pprint(vaccines)
    for entry in vaccines:
        vaccine_data = copy.deepcopy(entry)
        if vaccine_data.get("label"):
            vaccine_data["label"]["name_type"] = "abbreviated_location_with_passage_type"
            vaccine_data["label"]["size"] = 9
        vaccine_data["outline"] = "black" # "white" # black on Derek's request of 2020-02-18 12:28
        vaccine_data["report"] = True
        vaccine_data["size"] = 15
        # print(vaccine_data)
        settings["antigenic_maps"]["mods"].append(vaccine_data)

# def _signature_page_update_vaccines(virus_type, assay, lab, settings, map_settings):

#     def make_entry(map_draw_entry):
#         module_logger.debug("map_draw_entry {}".format(map_draw_entry))
#         sigp_entry = {"show": map_draw_entry.get("show", True), "label": {"offset": [0, 1]}}
#         try:
#             sigp_entry["type"] = map_draw_entry["select"]["vaccine"]["type"]
#         except KeyError:
#             pass
#         try:
#             sigp_entry["passage"] = map_draw_entry["select"]["vaccine"]["passage"]
#         except KeyError:
#             pass
#         try:
#             sigp_entry["fill"] = map_draw_entry["fill"]
#         except KeyError:
#             pass
#         module_logger.debug("sigp_entry {}".format(sigp_entry))
#         return sigp_entry

#     _remove_mod_entries(settings, "vaccines")

#     vaccines = map_settings["mods"][lab.upper() + "_vaccines"] # in the map-draw format
#     # convert to the old format

#     mods = ([
#         {"outline": "white", "size": 15, "label": {"color": "black", "font_family": "helvetica neu", "name_type": "abbreviated_location_with_passage_type", "size": 9, "slant": "normal", "weight": "normal"}},
#         ]
#         + [make_entry(e) for e in vaccines])


#     vaccine_data = {"N": "vaccines", "mods": mods}
#     settings["antigenic_maps"]["mods"].append(vaccine_data)

# ----------------------------------------------------------------------

def _signature_page_update_viewport_rotate_flip(virus_type, assay, lab, settings, map_settings):

    for field in ["flip", "rotate", "viewport"]:
        data = None
        try:
            module_logger.debug("{} {}".format(lab.upper() + "-" + field, map_settings["mods"][lab.upper() + "-" + field]))
            for mod in map_settings["mods"][lab.upper() + "-" + field]:
                if mod.get("N") == field:
                    data = mod
        except KeyError:
            module_logger.warning("No {} for {} found".format(field, lab.upper()))
        if data:
            _remove_mod_entries(settings, field)
            settings["antigenic_maps"]["mods"].append(data)

# ----------------------------------------------------------------------

def _signature_page_add_antigen_sample(virus_type, assay, lab, settings, map_settings):
    antigen_sample = {"?N": "antigens", "select": {"index": 4981, "name": "TEXAS/2/2013 E5 2015-02-03"}, "shown_on_all": True,
                          "size": 15, "fill": "pink", "outline": "white",
                          "label": {"offset": [0, 1], "display_name": "TX/2/13-egg", "size": 9},
                          "raise_": True, "raise_if_not_found": False}
    settings["antigenic_maps"]["mods"].append(antigen_sample)

# ======================================================================

def _remove_mod_entries(settings, key):
    for index in sorted((no for no, mod in enumerate(settings["antigenic_maps"]["mods"]) if mod.get("N", mod.get("?N")) in [key, "?" + key, key + "?"]), reverse=True):
        del settings["antigenic_maps"]["mods"][index]

# ----------------------------------------------------------------------

def subprocess_check_call(command):
    module_logger.info(command)
    subprocess.check_call(command, shell=True)

# ----------------------------------------------------------------------

sFieldSortingPrefix = {
    "signature_page": "001",
    "label_offset": "011",
    "label": "012",
    "first_leaf_seq_id": "013",
    }

def signature_page_settins_object_fields_sorting_key(key):
    return sFieldSortingPrefix.get(key, "") + key

# ----------------------------------------------------------------------

sIndex = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <style>
        h1 {
          margin-left: 1em;
          text-align: center;
        }
        object {
          width: 1360px;
          height: 860px;
        }
        li {
          margin-bottom: 1em;
        }
    </style>
    <title>Signature pages</title>
  </head>
  <body>
    <h1>Signature pages</h1>
    <ul>
      <li>H3 CDC HI<br><object data="h3-cdc-hi.pdf#toolbar=0"></object></li>
      <li>H3 CDC Neut<br><object data="h3-cdc-neut.pdf#toolbar=0"></object></li>
      <li>H3 Crick HI<br><object data="h3-nimr-hi.pdf#toolbar=0"></object></li>
      <li>H3 Crick Neut<br><object data="h3-nimr-neut.pdf#toolbar=0"></object></li>
      <li>H3 NIID Neut<br><object data="h3-niid-neut.pdf#toolbar=0"></object></li>
      <li>H3 VIDRL<br><object data="h3-melb-hi.pdf#toolbar=0"></object></li>
      <li>H3 VIDRL Neut<br><object data="h3-melb-neut.pdf#toolbar=0"></object></li>
      <li>H1<br><object data="h1-all-hi.pdf#toolbar=0"></object></li>
      <li>H1 CDC<br><object data="h1-cdc-hi.pdf#toolbar=0"></object></li>
      <li>H1 Crick<br><object data="h1-nimr-hi.pdf#toolbar=0"></object></li>
      <li>H1 NIID<br><object data="h1-niid-hi.pdf#toolbar=0"></object></li>
      <li>H1 VIDRL<br><object data="h1-melb-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic CDC<br><object data="bv-cdc-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic Crick<br><object data="bv-nimr-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic NIID<br><object data="bv-niid-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic VIDRL<br><object data="bv-melb-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam CDC<br><object data="by-cdc-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam Crick<br><object data="by-nimr-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam NIID<br><object data="by-niid-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam VIDRL<br><object data="by-melb-hi.pdf#toolbar=0"></object></li>
    </ul>
  </body>
</html>
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
