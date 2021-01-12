from pathlib import Path
import logging; module_logger = logging.getLogger(__name__)
from .lab import lab_new, lab_old

# ----------------------------------------------------------------------

class merge_finder:

    def __init__(self, subtype, assay, rbc, **options):
        self.subtype = subtype
        self.assay = assay
        self.rbc = rbc
        self.options = options

    def merge_exists(self, lab):
        mer = self.merge(lab=lab)
        #print(f"merge {mer} exists {mer.exists()}")
        return mer.exists()

    def merge(self, lab):
        return Path("merges", self.merge_2021(lab=lab))

    def previous_merge(self, lab):
        mer = Path("previous", "merges", self.merge_2021(lab=lab))
        if not mer.exists():
            mer = Path("previous", "merges", self.merge_old(lab=lab))
        if self.options.get("compare_with_previous") and mer.exists():
            return mer
        else:
            return ""

    def merge_2021(self, lab):
        if self.rbc:
            assay_rbc = self.assay_rbc()
        elif self.assay == "neut":
            if lab == "crick":
                assay_rbc = "prn"
            else:
                assay_rbc = "fra"
        else:
            assay_rbc = self.assay
        return f"{self.subtype}-{assay_rbc}-{lab}.ace"

    s_merge_old_subtype_fix = {"h1pdm": "h1"}
    def merge_old(self, lab):
        return f"{lab_old(lab)}-{self.s_merge_old_subtype_fix.get(self.subtype, self.subtype)}-{self.assay}.ace"

    def assay_rbc(self):
        if self.rbc:
            return f"{self.assay or 'hi'}-{self.rbc}"
        else:
            return self.assay or "hi"

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
