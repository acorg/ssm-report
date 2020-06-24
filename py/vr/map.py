import subprocess
from pathlib import Path

# ======================================================================

s_labs_for_subtype = {}

class maker:

    def __init__(self, subtype, assay=None, lab=None, map=None, **options):
        self.subtype = subtype
        self.assay = assay
        self.lab = lab
        self.map_name = map
        self.options = options
        if lab:
            global s_labs_for_subtype
            s_labs_for_subtype.setdefault(self._labs_for_subtype_key(), set()).add(lab)

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
        subtype_short, assay = self._assay()
        merge = f"merges/{lab}-{subtype_short}-{assay}.ace"
        pdf = f"{output_dir}/{self.subtype}-{assay}-{lab}-{self.map_name}.pdf"
        cmd = f"mapi -a vr:{self.map_name} {self._settings()} {merge} {pdf}"
        if interactive:
            cmd += " -i --open"
        elif open_pdf:
            cmd += f" && preview -p 930.0.820.870 {pdf}"

        #print(f"make_map {command_name} -> {self.subtype}, {assay}, {lab}, {self.map_name}")
        print(cmd)
        subprocess.check_call(cmd, shell=True)

    def ts(self, open_pdf, output_dir):
        subtype_short, assay = self._assay()
        merge = f"merges/{self.lab}-{subtype_short}-{assay}.ace"
        cmd = f"mapi -a vr:{self.map_name} {self._settings()} {merge} /"

        print(cmd)
        subprocess.check_call(cmd, shell=True)

        summary_pdf = f"{output_dir}/{self.subtype}-{assay}-{self.lab}-{self.map_name}-summary.pdf"
        cmd2 = f"pdf-combine {output_dir}/{self.subtype}-{assay}-{self.lab}-{self.map_name}-[12]*.pdf {summary_pdf}"
        if open_pdf:
            cmd2 += f" && preview -p 930.0.820.3000 {summary_pdf}"
        print(cmd2)
        subprocess.check_call(cmd2, shell=True)

    def many(self, output_dir):
        global s_labs_for_subtype
        for lab in sorted(s_labs_for_subtype[self._labs_for_subtype_key()]):
            self.one(lab=lab, interactive=False, open_pdf=False, output_dir=output_dir)

    def _assay(self):
        if self.assay is None:
            return self.subtype[:2], "hi"
        else:
            return self.subtype[:2], self.assay

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
