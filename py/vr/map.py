import subprocess
from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from .lab import lab_new, lab_old

# ======================================================================

s_labs_for_subtype = {}

class maker:

    def __init__(self, subtype, assay=None, lab=None, map=None, **options):
        self.subtype = subtype
        self.assay = assay
        self.map_name = map
        self.options = options
        if lab:
            self.lab = lab_new(lab)
            global s_labs_for_subtype
            s_labs_for_subtype.setdefault(self._labs_for_subtype_key(), set()).add(self.lab)
        else:
            self.lab = None

    def command_name_for_helm(self):
        return "-".join(en for en in (self.subtype, self.assay, self.lab, self.map_name) if en)

    def __call__(self, command_name, interactive, open_pdf=True, output_dir=Path("out"), *r, **a):
        output_dir.mkdir(exist_ok=True)
        if not self.lab:
            self.many(output_dir=output_dir)
        elif self.map_name == "ts":
            self.ts(open_pdf=open_pdf, output_dir=output_dir)
        else:
            self.one(lab=self.lab, interactive=interactive, open_pdf=open_pdf, output_dir=output_dir)

    def one(self, lab, interactive, open_pdf, output_dir):
        pdf = f"{output_dir}/{self.subtype}-{self._assay()}-{self.map_name}-{lab}.pdf"
        cmd = f"mapi -a vr:{self.map_name} {self._settings()} {self.merge(lab=lab)} {pdf}"
        if interactive:
            cmd += " -i --open"
        elif open_pdf:
            cmd += f" && preview -p 930.0.820.870 {pdf}"

        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def ts(self, open_pdf, output_dir):
        cmd = f"mapi -a vr:{self.map_name} {self._settings()} {self.merge(lab=self.lab)} /"

        print(cmd)
        subprocess.check_call(cmd, shell=True)

        summary_pdf = f"{output_dir}/{self.subtype}-{self._assay()}-{self.map_name}-summary-{self.lab}.pdf"
        cmd2 = f"pdf-combine {output_dir}/{self.subtype}-{self._assay()}-{self.map_name}-{self.lab}-[12]*.pdf {summary_pdf}"
        if open_pdf:
            cmd2 += f" && preview -p 930.0.820.3000 {summary_pdf}"
        print(cmd2)
        subprocess.check_call(cmd2, shell=True)

    def many(self, output_dir):
        global s_labs_for_subtype
        for lab in sorted(s_labs_for_subtype[self._labs_for_subtype_key()]):
            if Path(self.merge(lab=lab)).exists():
                self.one(lab=lab, interactive=False, open_pdf=False, output_dir=output_dir)
            else:
                module_logger.warning(f"No merge for \"{lab}\": {self.merge(lab=lab)}")

    def _assay(self):
        if self.assay is None:
            return "hi"
        else:
            return self.assay

    def merge(self, lab):
        return f"merges/{lab_old(lab)}-{self.subtype[:2]}-{self._assay()}.ace"

    def _settings(self):
        if self.subtype == "h3":
            return f"-s vr.mapi -s {self.subtype}.mapi -s {self.subtype}-{assay}.mapi -s serology.mapi -s vaccines.mapi"
        else:
            return f"-s vr.mapi -s {self.subtype}.mapi -s serology.mapi -s vaccines.mapi"

    def _labs_for_subtype_key(self):
        return f"{self.subtype} {assay if self.assay else 'hi'}"

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
