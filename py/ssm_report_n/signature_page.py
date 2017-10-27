import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import subprocess, datetime, pprint

from acmacs_base.json import read_json, write_json
from .map import sLabDisplayName

sVirusTypeShort = {"A(H1N1)": "H1", "A(H3N2)": "H3", "BVIC": "B/Vic", "BYAM": "B/Yam", "h1": "H1", "h3": "H3", "bvic": "B/Vic", "byam": "B/Yam"}

# ======================================================================

def signature_page_output_dir_init(sp_dir):
    index_file = Path(sp_dir, "index.html")
    if not index_file.exists():
        with index_file.open("w") as f:
            f.write(sIndex)

def signature_page_source_dir_init(sp_dir):
    for subtype in ["h1", "h3", "bvic", "byam"]:
        for suff in [".tree.json.xz", ".tree.settings.json"]:
            sl = sp_dir.joinpath(subtype + suff)
            if not sl.is_symlink():
                sl.symlink_to(Path("..", "tree", sl.name))

# ======================================================================

def tree_make(subtype, tree_dir, seqdb, output_dir, settings_infix="settings"):
    tree = tree_dir.joinpath(subtype + ".tree.json.xz")
    pdf = output_dir.joinpath(subtype + ".tree.pdf")
    settings = tree_dir.joinpath(subtype + ".tree." + settings_infix + ".json")
    if not settings.exists():
        subprocess_check_call("~/AD/bin/sigp --seqdb '{seqdb}' --init-settings '{settings}' --tree '{tree}' --output '{pdf}'".format(seqdb=seqdb, settings=settings, tree=tree, pdf=pdf))
        _tree_update_settings(subtype=subtype, settings=settings)
    subprocess_check_call("~/AD/bin/sigp --seqdb '{seqdb}' -s '{settings}' --tree '{tree}' --output '{pdf}'".format(seqdb=seqdb, settings=settings, tree=tree, pdf=pdf))

# ----------------------------------------------------------------------

def _tree_update_settings(subtype, settings):
    data = read_json(settings)
    data["title"]["title"] = sVirusTypeShort[subtype]
    data["signature_page"].pop("antigenic_maps_width", None)
    data["signature_page"].pop("mapped_antigens_margin_right", None)
    data.pop("mapped_antigens", None)
    data.pop("antigenic_maps", None)
    globals().get("_tree_update_settings_" + subtype)(data=data, settings=settings)
    write_json(settings, data)

# ----------------------------------------------------------------------

def _tree_update_settings_bvic(data, settings):
    report_settings = read_json("report.json")
    data["signature_page"].update({"left": 50, "right": 0, "clades_width": 50})
    data["time_series"]["begin"] = (datetime.datetime.strptime(report_settings["time_series"]["date"]["end"], "%Y-%m-%d") - datetime.timedelta(days=25*30)).strftime("%Y-%m-01")
    data["tree"]["mods"] = [
        {"mod": "before2015-58P-or-146I-or-559I", "?": "hides 1B"},
        {"?mod": "hide-between", "s1": "B/SHANGHAI-BAOSHAN/193/2011__MDCK1/MDCK1", "s2": "B/SOUTH%20AUSTRALIA/18/2011__MDCK1"},
        {"?mod": "hide-between", "s1": "B/JIANGSU-JINGJIANG/33/2012__MDCK2/MDCK2", "s2": "B/PHILIPPINES/2533/2011__MDCK1"}
        ]
    for clade_data in data["clades"]["clades"]:
        clade_data["label_offset"] = [3, 0]
        if clade_data["name"] == "1A":
            clade_data["section_inclusion_tolerance"] = 20
        elif clade_data["name"] == "1":
            clade_data["show"] = False

def _tree_update_settings_byam(data, settings):
    report_settings = read_json("report.json")
    data["signature_page"].update({"left": 70, "right": 0, "clades_width": 50})
    data["time_series"]["begin"] = (datetime.datetime.strptime(report_settings["time_series"]["date"]["end"], "%Y-%m-%d") - datetime.timedelta(days=25*30)).strftime("%Y-%m-01")
    for clade_data in data["clades"]["clades"]:
        clade_data["label_offset"] = [5, 0]

def _tree_update_settings_h1(data, settings):
    data["signature_page"].update({"left": 50, "right": 0, "clades_width": 60})
    data["tree"]["mods"] = [
        {"mod": "?hide-if-cumulative-edge-length-bigger-than", "d1": 0.029},
        ]

def _tree_update_settings_h3(data, settings):
    data["signature_page"].update({"left": 50, "right": 0, "clades_width": 100})
    data["tree"]["mods"] = [
        {"mod": "hide-if-cumulative-edge-length-bigger-than", "d1": 0.04},
        ]

# ======================================================================

def signature_page_make(virus_type, assay, lab, sp_source_dir, sp_output_dir, tree_dir, merge_dir, seqdb):
    # module_logger.warning("Source {}  Output {}  Tree {}".format(sp_source_dir, sp_output_dir, tree_dir))
    prefix = "{}-{}-{}".format(virus_type, lab, assay)
    settings = sp_source_dir.joinpath(prefix + ".sigp.settings.json")
    tree = tree_dir.joinpath(virus_type + ".tree.json.xz")
    tree_settings = sp_source_dir.joinpath(virus_type + ".tree.settings.json")
    # chart = merge_dir.joinpath("{}-{}-{}.sdb.xz".format(lab, virus_type.replace("b", "b-").replace("h1", "h1pdm"), assay))
    chart = merge_dir.joinpath("{}-{}-{}.ace".format(lab, virus_type.replace("b", "b-").replace("h1", "h1pdm"), assay))
    pdf = sp_output_dir.joinpath(prefix + ".pdf")
    if not settings.exists():
        subprocess_check_call("~/AD/bin/sigp --seqdb '{seqdb}' --chart '{chart}' -s '{tree_settings}' --no-draw --init-settings '{settings}' --tree '{tree}' -o '{pdf}'".format(seqdb=seqdb, chart=chart, settings=settings, tree_settings=tree_settings, tree=tree, pdf=pdf))
        _signature_page_update_settings(virus_type=virus_type, assay=assay, lab=lab, settings_file=settings)
    subprocess_check_call("~/AD/bin/sigp --seqdb '{seqdb}' --chart '{chart}' -s '{tree_settings}' -s '{settings}' --tree '{tree}' -o '{pdf}'".format(seqdb=seqdb, chart=chart, settings=settings, tree_settings=tree_settings, tree=tree, pdf=pdf))

# ----------------------------------------------------------------------

def _signature_page_update_settings(virus_type, assay, lab, settings_file):
    settings = read_json(settings_file)
    if virus_type == "h3":
        settings["title"]["title"] = "{} {} {}".format(sVirusTypeShort[virus_type], assay.upper(), sLabDisplayName[lab.upper()])
    else:
        settings["title"]["title"] = "{} {}".format(sVirusTypeShort[virus_type], sLabDisplayName[lab.upper()])
    settings.pop("clades", None)
    settings.pop("hz_sections", None)
    settings.pop("time_series", None)

    # disable tracked serum
    for mod in settings["antigenic_maps"]["mods"]:
        if isinstance(mod, dict) and mod.get("N") in ["tracked_sera", "tracked_serum_circles"]:
            mod["N"] = "?" + mod["N"]

    settings["antigenic_maps"]["columns"] = 3
    settings["signature_page"]["antigenic_maps_width"] = 579

    map_settings = read_json("{virus_type}-{assay}.json".format(virus_type=virus_type, assay=assay))
    # update viewport from ssm settings
    _signature_page_update_viewport(virus_type=virus_type, assay=assay, lab=lab, settings=settings, map_settings=map_settings)
    # update vaccine drawing from ssm settings
    _signature_page_update_vaccines(virus_type=virus_type, assay=assay, lab=lab, settings=settings, map_settings=map_settings)

    write_json(settings_file, settings)

# ----------------------------------------------------------------------

def _signature_page_update_vaccines(virus_type, assay, lab, settings, map_settings):

    vaccines = map_settings["mods"][lab.upper() + "_vaccines"] # in the map-draw format
    # convert to the old format

    _remove_mod_entries(settings, "vaccines")

    # try:
    #     for v_mod in map_settings["mods"][lab.upper() + "_vaccines"]:
    #         if vp_mod.get("N") == "viewport":
    #             viewport = vp_mod
    # except KeyError:
    #     pass

    # def fix_map_mod(mm):
    #     return {k: v for k,v in mm.items() if k not in ["size", "label"]}

    # for mod in settings["antigenic_maps"]["mods"]:
    #     if isinstance(mod, dict) and mod.get("N") == "vaccines":
    #         vaccine_mods = mod.setdefault("mods", [])
    #         for map_mod_all in filter(lambda e: e.get("N") == "vaccines", map_settings.get("4_mod_post", [])):
    #             map_mods = [mm2 for mm2 in (fix_map_mod(mm) for mm in map_mod_all.get("by_lab", {}).get(lab.upper(), {}).get("mods", [])) if mm2]
    #             # pprint.pprint(map_mods)
    #         mod["mods"].extend(map_mods)
    #         break

    # for mod in settings["antigenic_maps"]["mods"]:
    #     if isinstance(mod, dict) and mod.get("N") == "vaccines":
    #         vaccine_mods = mod.setdefault("mods", [])
    #         vaccine_mods1 = list(filter(lambda e: not e.get("label") and not e.get("name"), vaccine_mods))
    #         # pprint.pprint(vaccine_mods1)
    #         vaccine_mods2 = list(filter(lambda e: e.get("label") or e.get("name"), vaccine_mods))
    #         # pprint.pprint(vaccine_mods2)
    #         for map_mod_all in filter(lambda e: e.get("N") == "vaccines", map_settings.get("4_mod_post", [])):
    #             map_mods = [mm2 for mm2 in (fix_map_mod(mm) for mm in map_mod_all.get("by_lab", {}).get(lab.upper(), {}).get("mods", [])) if mm2]
    #             # pprint.pprint(map_mods)
    #             mod["mods"] = vaccine_mods1 + map_mods + vaccine_mods2
    #         break

# ----------------------------------------------------------------------

def _signature_page_update_viewport(virus_type, assay, lab, settings, map_settings):

    def viewport_index():
        for no, mod in enumerate(settings["antigenic_maps"]["mods"]):
            if mod.get("N") == "viewport":
                return no
        return None

    viewport = None
    try:
        for vp_mod in map_settings["mods"][lab.upper() + "_viewport"]:
            if vp_mod.get("N") == "viewport":
                viewport = vp_mod
    except KeyError:
        pass

    if viewport:
        _remove_mod_entries(settings, "viewport")
        # add new viewport entry
        # module_logger.debug("Viewport {}".format(viewport))
        settings["antigenic_maps"]["mods"].append(viewport)
    else:
        module_logger.warning("No viewport for {} found".format(lab.upper()))

# ======================================================================

def _remove_mod_entries(settings, key):
    for index in sorted((no for no, mod in enumerate(settings["antigenic_maps"]["mods"]) if mod.get("N", mod.get("?N")) in [key, "?" + key, key + "?"]), reverse=True):
        del settings["antigenic_maps"]["mods"][index]

# ----------------------------------------------------------------------

def subprocess_check_call(command):
    module_logger.info(command)
    subprocess.check_call(command, shell=True)

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
      <li>B/Vic CDC<br><object data="bvic-cdc-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic Crick<br><object data="bvic-nimr-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic NIID<br><object data="bvic-niid-hi.pdf#toolbar=0"></object></li>
      <li>B/Vic VIDRL<br><object data="bvic-melb-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam CDC<br><object data="byam-cdc-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam Crick<br><object data="byam-nimr-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam NIID<br><object data="byam-niid-hi.pdf#toolbar=0"></object></li>
      <li>B/Yam VIDRL<br><object data="byam-melb-hi.pdf#toolbar=0"></object></li>
    </ul>
  </body>
</html>
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
