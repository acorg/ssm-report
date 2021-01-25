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

    def previous_merge(self, lab, compare_with_previous=True):
        previous_merges_dir = Path("previous", "merges")
        mer = previous_merges_dir.joinpath(self.merge_2021(lab=lab))
        # print(f">>>> prev 2021 {mer} {mer.exists()}")
        if not mer.exists():
            mer = previous_merges_dir.joinpath(self.merge_old(lab=lab))
            # print(f">>>> prev old {mer} {mer.exists()}")
        if compare_with_previous and mer.exists():
            return mer
        else:
            return ""

    def previous_previous_merge(self, lab):
        previous_previous_merges_dir = Path("previous", "previous", "merges")
        mer = previous_previous_merges_dir.joinpath(self.merge_2021(lab=lab))
        # print(f">>>> prev-prev 2021 {mer} {mer.exists()}")
        if not mer.exists():
            mer = previous_previous_merges_dir.joinpath(self.merge_old(lab=lab))
            # print(f">>>> prev-prev old {mer} {mer.exists()}")
        if mer.exists():
            return mer
        else:
            return ""

    def merge_2021(self, lab):
        if self.rbc and isinstance(self.rbc, list):
            for rbc in self.rbc:
                mrg = f"{self.subtype}-hi-{rbc}-{lab}.ace"
                # print(f">>>> {mrg} {Path('merges', mrg).exists()}")
                if Path("merges", mrg).exists():
                    return mrg
            return "{self.subtype}-hi-{self.rbc}-{lab}.ace *not-found*"
        elif self.rbc:
            assay_rbc = self.assay_rbc(lab)
        elif self.assay == "neut":
            if lab == "crick":
                assay_rbc = "prn"
            else:
                assay_rbc = "fra"
        else:
            assay_rbc = self.assay
        return f"{self.subtype}-{assay_rbc}-{lab}.ace"

    s_merge_old_subtype_fix = {"h1pdm": "h1", "bvic": "bv", "byam": "by"}
    def merge_old(self, lab):
        return f"{lab_old(lab)}-{self.s_merge_old_subtype_fix.get(self.subtype, self.subtype)}-{self.assay}.ace"

    def assay_rbc(self, lab):
        if self.rbc and isinstance(self.rbc, list):
            if isinstance(lab, list):
                lab = lab[0]
            for rbc in self.rbc:
                assay_rbc = f"hi-{rbc}"
                mrg = f"{self.subtype}-{assay_rbc}-{lab}.ace"
                # print(f">>>> {mrg} {Path('merges', mrg).exists()}")
                if Path("merges", mrg).exists():
                    return assay_rbc
            return f"hi-{self.rbc}"
        elif self.rbc:
            return f"{self.assay or 'hi'}-{self.rbc}"
        else:
            return self.assay or "hi"

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
