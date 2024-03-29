import sys, subprocess, traceback
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from .lab import lab_new, lab_old
from .merge import merge_finder

# ======================================================================

SEP = "> ======================================================================"

s_labs_for_subtype = {}
s_clade_maps = {}

class maker (merge_finder):

    def __init__(self, subtype, assay=None, lab=None, rbc=None, map=None, labs=None, maps=None, info=False, **options):
        super().__init__(subtype=subtype, assay=assay, rbc=rbc, **options)
        self.map_name = map
        self.maps = maps
        self.labs = labs
        self.info = info
        if lab:
            self.lab = lab_new(lab)
            global s_labs_for_subtype
            s_labs_for_subtype.setdefault(self._subtype_key(), set()).add(self.lab)
        else:
            self.lab = None
        if map and (map.startswith("clade-") or map == "clade"):
            global s_clade_maps
            s_clade_maps.setdefault(self._subtype_key(), set()).add(map)

    def command_name_for_helm(self):
        if self.info:
            return "info-" + "-".join(en for en in (self.subtype, self.assay, self.lab, self.map_name) if en)
        else:
            return "-".join(en for en in (self.subtype, self.assay, self.lab, self.map_name) if en)

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=None, *r, **a):
        if not output_dir:
            if self.info:
                output_dir = Path("info")
            else:
                output_dir = Path("out")
        output_dir.mkdir(exist_ok=True)
        if not self.lab and self.map_name:
            self.many_labs(output_dir=output_dir)
        elif self.map_name == "ts":
            self.ts(lab=self.lab, map_name=self.map_name, open_pdf=open_pdf, output_dir=output_dir)
        elif self.map_name == "clades":
            self.many_clades(output_dir=output_dir)
        elif self.lab and not self.map_name and self.maps: # multiple maps for the same lab (all maps)
            for map_name in self.maps:
                if map_name == "ts":
                    self.ts(lab=self.lab, map_name=map_name, open_pdf=False, output_dir=output_dir)
                elif map_name in ["sp", "spc", "spx"]:
                    pass    # no sig page
                else:
                    self.one(map_name=map_name, interactive=False, open_pdf=False, output_dir=output_dir)
        # elif not self.lab and self.labs and self.map_name: # multiple maps for virus type and map type (all labs)
        elif not self.lab and self.labs and not self.map_name and self.maps: # multiple maps for virus type (all maps, all labs)
            for lab in self.labs:
                for map_name in self.maps:
                    if map_name == "ts":
                        self.ts(lab=lab, map_name=map_name, open_pdf=False, output_dir=output_dir)
                    elif map_name in ["sp", "spc", "spx"]:
                        pass    # no sig page
                    else:
                        self.one(lab=lab, map_name=map_name, interactive=False, open_pdf=False, output_dir=output_dir)
        else:
            self.one(lab=self.lab, interactive=interactive, open_pdf=open_pdf, output_dir=output_dir)

    def one(self, interactive, open_pdf, output_dir, lab=None, map_name=None):
        if not lab:
            lab = self.lab
        if not map_name:
            map_name = self.map_name
        if self.merge_exists(lab=lab, map_name=map_name):
            pdf = f"{output_dir}/{self.subtype}-{self.assay_rbc(lab)}-{map_name}-{lab}.pdf"
            cmd = f"mapi -a vr:{map_name} {self._settings()} {self.merge(lab=lab, map_name=map_name)} {self.previous_merge(lab=lab, map_name=map_name)} {self.previous_previous_merge(lab=lab, map_name=map_name)} {pdf}"
            if map_name == "serology":
                # export ace
                cmd += " --export " + pdf.replace(".pdf", ".ace")
            # if open_pdf:
            #     cmd += " --preview 1050.0.930.980"
            if interactive:
                cmd += " -i"

            print(f"{SEP}\n> {lab} {self.subtype} {self.assay_rbc(lab)} {map_name}\n{cmd}\n{SEP}")
            subprocess.check_call(cmd, shell=True)
        else:
            module_logger.warning(f"No merge present: {self.merge(lab=lab)}: cannot make {map_name}")

    def ts(self, lab, map_name, open_pdf, output_dir):
        if self.merge_exists(lab=lab, map_name=map_name):
            compare_with_previous = str(bool(self.options.get("compare_with_previous"))).lower()
            cmd = f"mapi -a vr:{map_name} {self._settings()} -D compare-with-previous={compare_with_previous} {self.merge(lab=lab)} {self.previous_merge(lab=lab, compare_with_previous=self.options.get('compare_with_previous'))} /"
            print(cmd)
            subprocess.check_call(cmd, shell=True)

            summary_pdf = f"{output_dir}/summary-{self.subtype}-{self.assay_rbc(lab)}-{map_name}-{lab}.pdf"
            cmd2 = f"pdf-combine {output_dir}/{self.subtype}-{self.assay_rbc(lab)}-{map_name}-{lab}*.pdf {summary_pdf}"
            if open_pdf:
                cmd2 += f" && preview -p 1050.0.930.3000 {summary_pdf}"
            print(cmd2)
            subprocess.check_call(cmd2, shell=True)
        else:
            module_logger.warning(f"No merge present: {self.merge(lab=lab)}: cannot make ts")

    def many_labs(self, output_dir):
        global s_labs_for_subtype
        for lab in sorted(s_labs_for_subtype[self._subtype_key()]):
            self.one(lab=lab, interactive=False, open_pdf=False, output_dir=output_dir)

    def many_clades(self, output_dir):
        global s_clades
        for clade_map in sorted(s_clade_maps[self._subtype_key()]):
            self.one(lab=self.lab, map_name=clade_map, interactive=False, open_pdf=False, output_dir=output_dir)

    def _settings(self):
        if self.subtype == "h3":
            return f"-s vr.mapi -s {self.subtype}.mapi -s {self.subtype}-{self.assay}.mapi -s serology.mapi -s vaccines.mapi"
        else:
            return f"-s vr.mapi -s {self.subtype}.mapi -s serology.mapi -s vaccines.mapi"

    def _subtype_key(self):
        return f"{self.subtype} {self.assay if self.assay else 'hi'}"

# ======================================================================

def makers(subtype, labs, maps, assay=None, rbc=None, **options):
    # print(f">>>> makers {subtype} {labs} {maps} {assay} {rbc} {options}\n{' '.join(traceback.format_stack())}", file=sys.stderr)
    result = [mk for mk in (maker(subtype=subtype, assay=assay, rbc=rbc, lab=lab, map=map, **options) for lab in labs for map in maps if map != "sp") if mk.merge_exists(mk.lab)]
    # if result and len([en for en in maps if en.startswith("clade")]) > 1:
    #     for lab in labs:
    #         mk = maker(subtype=subtype, assay=assay, rbc=rbc, lab=lab, map="clades", **options)
    #         if mk.merge_exists(lab):
    #             result.append(maker(subtype=subtype, assay=assay, rbc=rbc, lab=lab, map="clades", **options))
    for lab in labs:
        result.append(maker(subtype=subtype, assay=assay, rbc=rbc, lab=lab, maps=maps, **options))
    result.append(maker(subtype=subtype, assay=assay, rbc=rbc, labs=labs, maps=maps, **options))
    if "sp" in maps:
        from . import tree
        result.extend(tree.makers_sp(subtype=subtype, assay=assay, rbc=rbc, labs=labs))
    return result

# ======================================================================

def info_makers(subtype, labs, maps, assay=None, rbc=None, **options):
    result = [mk for mk in (maker(subtype=subtype, assay=assay, rbc=rbc, lab=lab, map=map, info=True, **options) for lab in labs for map in maps) if mk.merge_exists(mk.lab)]
    for lab in labs:
        result.append(maker(subtype=subtype, assay=assay, rbc=rbc, lab=lab, maps=maps, info=True, **options))
    result.append(maker(subtype=subtype, assay=assay, rbc=rbc, labs=labs, maps=maps, info=True, **options))
    return result

# ======================================================================
