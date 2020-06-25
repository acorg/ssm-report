import subprocess
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from .lab import lab_new, lab_old

# ======================================================================

s_labs_for_subtype = {}
s_clade_maps = {}

class maker:

    def __init__(self, subtype, assay=None, lab=None, map=None, maps=None, **options):
        self.subtype = subtype
        self.assay = assay
        self.map_name = map
        self.maps = maps
        self.options = options
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
        return "-".join(en for en in (self.subtype, self.assay, self.lab, self.map_name) if en)

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=Path("out"), *r, **a):
        output_dir.mkdir(exist_ok=True)
        if not self.lab:
            self.many_labs(output_dir=output_dir)
        elif self.map_name == "ts":
            self.ts(open_pdf=open_pdf, output_dir=output_dir)
        elif self.map_name == "clades":
            self.many_clades(output_dir=output_dir)
        elif not self.map_name and self.maps:
            for map_name in self.maps:
                if map_name == "ts":
                    self.ts(open_pdf=False, output_dir=output_dir)
                else:
                    self.one(map_name=map_name, interactive=False, open_pdf=False, output_dir=output_dir)
        else:
            self.one(lab=self.lab, interactive=interactive, open_pdf=open_pdf, output_dir=output_dir)

    def one(self, interactive, open_pdf, output_dir, lab=None, map_name=None):
        if not lab:
            lab = self.lab
        if not map_name:
            map_name = self.map_name
        pdf = f"{output_dir}/{self.subtype}-{self._assay()}-{map_name}-{lab}.pdf"
        cmd = f"mapi -a vr:{map_name} {self._settings()} {self.merge(lab=lab)} {pdf}"
        if open_pdf:
            cmd += " --preview 1050.0.930.980"
        if interactive:
            cmd += " -i"

        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def ts(self, open_pdf, output_dir):
        compare_with_previous = str(bool(self.options.get("compare_with_previous"))).lower()
        cmd = f"mapi -a vr:{self.map_name} {self._settings()} -D compare-with-previous={compare_with_previous} {self.merge(lab=self.lab)} {self.previous_merge(lab=self.lab)} /"
        print(cmd)
        subprocess.check_call(cmd, shell=True)

        summary_pdf = f"{output_dir}/{self.subtype}-{self._assay()}-{self.map_name}-summary-{self.lab}.pdf"
        cmd2 = f"pdf-combine {output_dir}/{self.subtype}-{self._assay()}-{self.map_name}-{self.lab}-[12]*.pdf {summary_pdf}"
        if open_pdf:
            cmd2 += f" && preview -p 1050.0.930.3000 {summary_pdf}"
        print(cmd2)
        subprocess.check_call(cmd2, shell=True)

    def many_labs(self, output_dir):
        global s_labs_for_subtype
        for lab in sorted(s_labs_for_subtype[self._subtype_key()]):
            self.one(lab=lab, interactive=False, open_pdf=False, output_dir=output_dir)

    def many_clades(self, output_dir):
        global s_clades
        for clade_map in sorted(s_clade_maps[self._subtype_key()]):
            self.one(lab=self.lab, map_name=clade_map, interactive=False, open_pdf=False, output_dir=output_dir)

    def _assay(self):
        if self.assay is None:
            return "hi"
        else:
            return self.assay

    def merge(self, lab):
        return f"merges/{lab_old(lab)}-{self.subtype[:2]}-{self._assay()}.ace"

    def previous_merge(self, lab):
        mer = f"previous/merges/{lab_old(lab)}-{self.subtype[:2]}-{self._assay()}.ace"
        if self.options.get("compare_with_previous") and Path(mer).exists():
            return mer
        else:
            return ""

    def merge_exists(self, lab):
        mer = self.merge(lab=lab)
        return Path(mer).exists()

    def _settings(self):
        if self.subtype == "h3":
            return f"-s vr.mapi -s {self.subtype}.mapi -s {self.subtype}-{self.assay}.mapi -s serology.mapi -s vaccines.mapi"
        else:
            return f"-s vr.mapi -s {self.subtype}.mapi -s serology.mapi -s vaccines.mapi"

    def _subtype_key(self):
        return f"{self.subtype} {self.assay if self.assay else 'hi'}"

# ======================================================================

def makers(subtype, labs, maps, assay=None, **options):
    result = [mk for mk in (maker(subtype=subtype, assay=assay, lab=lab, map=map, **options) for lab in labs for map in maps) if mk.merge_exists(mk.lab)]
    if result and len([en for en in maps if en.startswith("clade")]) > 1:
        for lab in labs:
            mk = maker(subtype=subtype, assay=assay, lab=lab, map="clades", **options)
            if mk.merge_exists(lab):
                result.append(maker(subtype=subtype, assay=assay, lab=lab, map="clades", **options))
    for lab in labs:
        result.append(maker(subtype=subtype, assay=assay, lab=lab, maps=maps, **options))
    return result

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
