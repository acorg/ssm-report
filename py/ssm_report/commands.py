import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import re, subprocess, shutil, pprint

from .map import make_map, make_map_for_lab, make_ts, make_map_information, make_index_html as maps_make_index_html
from .stat import make_stat
from .geographic import make_geographic
from .signature_page import tree_make, tree_make_aa_pos, signature_page_make, trees_get_from_albertine
from .init import init_git, get_dbs, init_dirs, init_settings

# ======================================================================

class Error (RuntimeError): pass

# ----------------------------------------------------------------------

sLabName = {"vidrl": "melb", "crick": "nimr", "c": "cdc", "m": "melb", "j": "niid", "e": "nimr"}
sLabsPattern = "(cdc|cnic|melb|niid|nimr|vidrl|crick|c|m|j|e)"

def make_lab(text):
    global sLabName
    text = text.lower()
    return sLabName.get(text, text)

sVirusType = {"h3n": "h3", "h3neut": "h3", "bv": "bvic", "by": "byam", "v": "bvic", "y": "byam", "n": "h3", "h": "h3", "1": "h1", "3": "h3"}
sVirusTypePattern = "(h1|h3|h3n|h3neut|bv|by|bvic|byam|v|y)"

def make_virus_type(text):
    text = text.lower()
    return sVirusType.get(text, text)

sAssay = {"n": "neut", "h3n": "neut", "h3neut": "neut"}

def make_assay(text):
    text = text.lower()
    return sAssay.get(text, "hi")

sReCommand = re.compile(f"{sVirusTypePattern}_([a-z0-9]+)_{sLabsPattern}$", re.I)

# ----------------------------------------------------------------------

def process_commands(commands, verbose, force, open_image):
    try:
        Processor(verbose=verbose, force=force, open_image=open_image)._process(commands)
    except Error as err:
        module_logger.error("ERROR: " + str(err))
        return 1
    return 0

# ----------------------------------------------------------------------

class Processor:

    def __init__(self, verbose, force, open_image):
        self._verbose = verbose
        self._force = force
        self._open_image = open_image
        self._make_sp_makers()

    def _process(self, commands):
        if not commands:
            self.list()
        else:
            for command in commands:
                command = command.replace("-", "_").lower()
                m = sReCommand.match(command)
                if m:
                    # module_logger.debug(f"virus_type={make_virus_type(m.group(1))} assay={make_assay(m.group(1))} lab={make_lab(m.group(3))}")
                    getattr(self, m.group(2))(virus_type=make_virus_type(m.group(1)), assay=make_assay(m.group(1)), lab=make_lab(m.group(3)))
                else:
                    getattr(self, command)()
            maps_make_index_html()
            self.merges_make_index_html()

    def init(self):
        """initialize ssm report data directory structure"""
        init_git()
        get_dbs()
        init_dirs()
        init_settings()
        # self._get_merges()

    def list(self):
        """list available commands"""
        from inspect import ismethod
        for cmdname in dir(self):
            if cmdname[0] != "_" and cmdname[-1] != "_":
                cmd = getattr(self, cmdname)
                if ismethod(cmd):
                    print(cmdname, "-", cmd.__doc__)

    # def remake_seqdb(self):
    #     """Re-generate seqdb from from fasta files"""
    #     seqdb_filename = self._seqdb_file()
    #     if seqdb_filename.exists():
    #         from acmacs_base.files import backup_file
    #         backup_file(seqdb_filename)
    #         seqdb_filename.unlink()
    #     get_dbs()

    def all(self):
        "Generate stat, geographic maps and antigenic maps for all subtypes"
        self.stat()
        self.geo()
        self.h3()
        self.h3neut()
        self.h1()
        self.bvic()
        self.byam()

    def stat(self):
        """make statistics for antigens and sera found in WHO CC HI tables"""
        make_stat(stat_dir=Path("stat"), hidb_dir=self._db_dir(), force=self._force)

    def geo(self):
        """make geographic time series"""
        make_geographic(geo_dir=Path("geo"), db_dir=self._db_dir(), force=self._force)

        # ----------------------------------------------------------------------

    # def map_settings(self):
    #     self.h1_map_settings()
    #     self.h3_map_settings()
    #     self.h3neut_map_settings()
    #     self.bvic_map_settings()
    #     self.byam_map_settings()

    # def h1_map_settings(self):
    #     from .settings import make_map_settings
    #     make_map_settings(virus_type='h1', assay='hi', force=self._force)

    # def h3_map_settings(self):
    #     from .settings import make_map_settings
    #     make_map_settings(virus_type='h3', assay='hi', force=self._force)

    # def h3neut_map_settings(self):
    #     from .settings import make_map_settings
    #     make_map_settings(virus_type='h3', assay='neut', force=self._force)

    # def bvic_map_settings(self):
    #     from .settings import make_map_settings
    #     make_map_settings(virus_type='bvic', assay='hi', force=self._force)

    # def byam_map_settings(self):
    #     from .settings import make_map_settings
    #     make_map_settings(virus_type='byam', assay='hi', force=self._force)

        # ----------------------------------------------------------------------

    def get_trees_from_albertine(self):
        trees_get_from_albertine(tree_dir=Path("tree"))

    def tree(self):
        """Generate tree images for all subtypes."""
        self.h1_tree()
        self.h3_tree()
        self.bvic_tree()
        self.byam_tree()

    def h1_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h1", tree_dir=Path("tree"), seqdb=self._seqdb_file())

    def h1_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="h1", tree_dir=Path("tree"), seqdb=self._seqdb_file())

    def h3_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h3", tree_dir=Path("tree"), seqdb=self._seqdb_file())

    def h3_tree_142(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h3", tree_dir=Path("tree"), seqdb=self._seqdb_file(), tree_infix=".142")

    def bv_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="bv", tree_dir=Path("tree"), seqdb=self._seqdb_file())
    bvic_tree = bv_tree

    def by_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="by", tree_dir=Path("tree"), seqdb=self._seqdb_file())
    byam_tree = by_tree

    def h1_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="h1", tree_dir=Path("tree"), seqdb=self._seqdb_file())

    def h3_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="h3", tree_dir=Path("tree"), seqdb=self._seqdb_file())

    def bv_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="bv", tree_dir=Path("tree"), seqdb=self._seqdb_file())
    bvic_tree_aa = bv_tree_aa

    def by_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="by", tree_dir=Path("tree"), seqdb=self._seqdb_file())
    byam_tree_aa = by_tree_aa

    def tree_information(self):
        """Generate tree images for all subtypes."""
        self.h1_tree_information()
        self.h3_tree_information()
        self.bvic_tree_information()
        self.byam_tree_information()

    def h1_tree_information(self):
        self._tree_information("h1")

    def h3_tree_information(self):
        self._tree_information("h3")

    def bvic_tree_information(self):
        self._tree_information("bv")

    def byam_tree_information(self):
        self._tree_information("by")

    def _tree_information(self, virus_type):
        tree_dir = Path("tree")
        from .signature_page import tree_make_information_settings
        tree_make_information_settings(virus_type=virus_type, tree_dir=tree_dir, output_dir=Path("information"))
        tree_make(subtype=virus_type, tree_dir=tree_dir, seqdb=self._seqdb_file(), output_dir=Path("information"), settings_infix="information")

        # ----------------------------------------------------------------------

    def h3(self):
        self.h3_clade()
        self.h3_ts()
        self.h3_geography()
        self.serology(virus_type="h3", assay="hi")()
        # #self.h3_serum_sectors()
        self.h3_serum_coverage()

    def h3neut(self):
        self.h3neut_clade()
        self.h3neut_ts()
        self.h3neut_geography()
        self.serology(virus_type="h3", assay="neut")()
        #self.h3neut_serum_sectors()
        self.h3neut_serum_coverage()

    def h1(self):
        self.h1_clade()
        # self.h1_geography()
        self.h1_serology()
        self.h1_ts()


    def bvic(self):
        self.bvic_clade()
        self.bvic_geography()
        self.serology(virus_type="bv", assay="hi")()
        #self.bvic_serum_sectors()
        self.bvic_ts()
    bv = bvic

    def byam(self):
        self.byam_clade()
        self.byam_geography()
        self.serology(virus_type="by", assay="hi")()
        #self.byam_serum_sectors()
        self.byam_ts()
    by = byam

    def report(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def report_abbreviated(self):
        from .report import make_report_abbreviated
        make_report_abbreviated(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def report_serumcoverage(self):
        from .report import make_report_serumcoverage
        make_report_serumcoverage(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"))

    def sp_addendum(self):
        from .report import make_signature_page_addendum
        make_signature_page_addendum(source_dir=Path("sp"), output_dir=Path("report"))

    def addendum_3(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-3", report_settings_file="report-addendum-3.json")

    def addendum_4(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-4", report_settings_file="report-addendum-4.json")

    def addendum_5(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=Path(""), output_dir=Path("report"), report_name="addendum-5", report_settings_file="report-addendum-5.json")

    def update_merges(self):
        target_dir = self._merges_dir()
        module_logger.info("Updating merges in " + repr(str(target_dir)))
        from acmacs_whocc import acmacs
        acmacs.get_recent_merges(target_dir)

    def h1_overlay(self):
        module_logger.info("Making h1 overlay")
        merges_dir = self._merges_dir()
        from acmacs_whocc.h1_overlay import h1_overlay_relax
        h1_overlay_relax(sorted(merges_dir.glob("[cmn]*-h1-hi.ace")), merges_dir.joinpath("all-h1-hi.ace"), log_file=self._log_dir().joinpath("h1-overlay.log"))

    def update_hidb(self):
        self._get_hidb()

    # ----------------------------------------------------------------------
    # H1 HI

    def h1_clade(self):
        self.clade(virus_type="h1", assay="hi")
    h1_clades = h1_clade

    def h1_clade_labs(self):
        self.clade(virus_type="h1", assay="hi", lab=["cdc", "melb", "niid", "nimr"])

    def h1_serology(self):
        self.serology(virus_type="h1", assay="hi")

    def h1_serology_labs(self):
        self.serology(virus_type="h1", assay="hi", lab=["cdc", "melb", "niid", "nimr"])

    def h1_geography(self):
        self._geography(virus_type="h1", assay="hi")
    h1_geo = h1_geography

    def h1_ts(self, lab=None):
        make_ts(virus_type="h1", assay="hi", lab=lab, output_dir=Path("h1-hi"), force=self._force)

    def h1_ts_labs(self, lab=None):
        make_ts(virus_type="h1", assay="hi", lab=lab or ["cdc", "melb", "niid", "nimr"], output_dir=Path("h1-hi"), force=self._force)

    def h1_information(self):
        make_map_information(virus_type="h1", assay="hi", output_dir=Path("information"), force=self._force)

    # ----------------------------------------------------------------------
    # H3 HI

    def h3_clade(self):
        self.clade(virus_type="h3", assay="hi")
        self.clade_6m(virus_type="h3", assay="hi")
        self.clade_12m(virus_type="h3", assay="hi")
    h3_clades = h3_clade

    def h3_aa_at_142(self):
        self._aa_at(virus_type="h3", assay="hi", positions=[142])

    def h3_geography(self):
        self._geography(virus_type="h3", assay="hi")
    h3_geo = h3_geography

    def h3_ts(self, lab=None):
        make_ts(virus_type="h3", assay="hi", lab=lab, output_dir=Path("h3-hi"), force=self._force)

    def h3_serology(self):
        self.serology(virus_type="h3", assay="hi")

    def h3_serum_sectors(self):
        self._serum_sectors(virus_type="h3", assay="hi")

    def h3_information(self):
        make_map_information(virus_type="h3", assay="hi", output_dir=Path("information"), force=self._force)

    # ----------------------------------------------------------------------
    # H3 Neut

    def h3neut_clade(self):
        self.clade(virus_type="h3", assay="neut")
        self.clade_6m(virus_type="h3", assay="neut")
        self.clade_12m(virus_type="h3", assay="neut")
    h3neut_clades = h3neut_clade
    h3n_clades = h3neut_clade
    h3n_clade = h3neut_clade

    def h3neut_aa_at_142(self):
        self._aa_at(virus_type="h3", assay="neut", positions=[142])
    h3n_aa_at_142 = h3neut_aa_at_142

    def h3neut_geography(self):
        self._geography(virus_type="h3", assay="neut")
    h3neut_geo = h3neut_geography
    h3n_geo = h3neut_geography

    def h3neut_ts(self, lab=None):
        make_ts(virus_type="h3", assay="neut", lab=lab, output_dir=Path("h3-neut"), force=self._force)
    h3n_ts = h3neut_ts

    def h3neut_serology(self):
        self.serology(virus_type="h3", assay="neut")
    h3n_serology = h3neut_serology

    def h3neut_niid_oseltamivir(self):
        virus_type = "h3"
        assay = "neut"
        lab = "niid"
        infix = "-oseltamivir"
        settings_files = list(Path(".").glob(f"*{virus_type}-{assay}.json"))
        output_dir = Path(virus_type + "-" + assay)
        for mod in ["clade", "clade_6m", "clade_12m", "aa_at_142", "geography", "serology"]:
            make_map_for_lab(prefix=mod.replace("_", "-"), virus_type=virus_type, assay=assay, lab=lab, infix=infix, mod=mod, output_dir=output_dir, settings_files=settings_files, open_image=self._open_image)
        make_ts(virus_type=virus_type, assay=assay, lab=lab, output_dir=output_dir, infix=infix, force=self._force)
        from . import map as map_m
        map_m.sDirsForIndex.add(output_dir)
    h3n_niid_oseltamivir = h3neut_niid_oseltamivir

    def h3neut_serum_sectors(self):
        self._serum_sectors(virus_type="h3", assay="neut")

    def h3neut_information(self):
        make_map_information(virus_type="h3", assay="neut", output_dir=Path("information"), force=self._force)

    # ----------------------------------------------------------------------
    # BVIC HI

    def bvic_clade(self):
        self.clade(virus_type="bv", assay="hi")
        self.clade_6m(virus_type="bv", assay="hi")
        self.clade_12m(virus_type="bv", assay="hi")
    bv_clade = bvic_clade
    bv_clades = bvic_clade
    bvic_clades = bvic_clade

    def bvic_geography(self):
        self._geography(virus_type="bv", assay="hi")
    bv_geo = bvic_geography
    bvic_geo = bvic_geography

    def bvic_ts(self, lab=None):
        make_ts(virus_type="bv", assay="hi", lab=lab, output_dir=Path("bv-hi"), force=self._force)
    bv_ts = bvic_ts

    def bvic_serology(self):
        self.serology(virus_type="bv", assay="hi")
    bv_serology = bvic_serology

    def bvic_information(self):
        make_map_information(virus_type="bv", assay="hi", output_dir=Path("information"), force=self._force)
    bv_information = bvic_information

    # ----------------------------------------------------------------------
    # BYAM HI

    def byam_clade(self):
        self.clade(virus_type="by", assay="hi")
        self.clade_6m(virus_type="by", assay="hi")
        self.clade_12m(virus_type="by", assay="hi")
    byam_clades = byam_clade
    by_clades = byam_clade
    by_clade = byam_clade

    def byam_geography(self):
        self._geography(virus_type="by", assay="hi")
    byam_geo = byam_geography
    by_geo = byam_geography

    def byam_ts(self, lab=None):
        make_ts(virus_type="by", assay="hi", lab=lab, output_dir=Path("by-hi"), force=self._force)
    by_ts = byam_ts

    def byam_serology(self):
        self.serology(virus_type="by", assay="hi")
    by_serology = byam_serology

    def byam_information(self):
        make_map_information(virus_type="by", assay="hi", output_dir=Path("information"), force=self._force)
    by_information = byam_information

    # ----------------------------------------------------------------------
    # Signature pages

    def signature_page(self):
        """Generate all signature pages"""
        self.sp_h1()
        self.sp_h3()
        self.sp_h3neut()
        self.sp_bvic()
        self.sp_byam()

    sp = signature_page
    sigp = signature_page
    signature_pages = signature_page

    def sp_h1(self):
        self.sp_h1_all()
        # self.sp_h1_cdc()
        # self.sp_h1_melb()
        # self.sp_h1_niid()
        # self.sp_h1_nimr()

    def sp_h3(self):
        self.sp_h3_cdc()
        self.sp_h3_melb()
        self.sp_h3_nimr()

    def sp_h3neut(self):
        self.sp_h3neut_cdc()
        self.sp_h3neut_melb()
        self.sp_h3neut_niid()
        self.sp_h3neut_nimr()

    def sp_bvic(self):
        self.sp_bv_cdc()
        self.sp_bv_melb()
        self.sp_bv_niid()
        self.sp_bv_nimr()
    sp_bv = sp_bvic

    def sp_byam(self):
        self.sp_by_cdc()
        self.sp_by_melb()
        self.sp_by_niid()
        self.sp_by_nimr()
    sp_by = sp_byam

    def spsc(self):
        """Generate all signature pages with serum circles"""
        self.spsc_h1()
        self.spsc_h3()
        self.spsc_h3neut()
        self.spsc_bvic()
        self.spsc_byam()

    def spsc_h1(self):
        self.spsc_h1_all()
        # self.spsc_h1_cdc()
        # self.spsc_h1_melb()
        # self.spsc_h1_niid()
        # self.spsc_h1_nimr()

    def spsc_h3(self):
        self.spsc_h3_cdc()
        self.spsc_h3_melb()
        self.spsc_h3_nimr()

    def spsc_h3neut(self):
        self.spsc_h3neut_cdc()
        self.spsc_h3neut_melb()
        self.spsc_h3neut_niid()
        self.spsc_h3neut_nimr()

    def spsc_bv(self):
        self.spsc_bv_cdc()
        self.spsc_bv_melb()
        self.spsc_bv_niid()
        self.spsc_bv_nimr()

    def spsc_by(self):
        self.spsc_by_cdc()
        self.spsc_by_melb()
        self.spsc_by_niid()
        self.spsc_by_nimr()

    def _make_sp_makers(self):
        def sp_mf(virus_type, assay, lab):
            return lambda: signature_page_make(virus_type=virus_type, assay=assay, lab=lab, sp_source_dir=self._sp_source_dir(), sp_output_dir=self._sp_output_dir(),
                                                   tree_dir=Path("tree"), merge_dir=self._merges_dir(), seqdb=self._seqdb_file())
        def spsc_mf(virus_type, assay, lab):
            return lambda: signature_page_make(virus_type=virus_type, assay=assay, lab=lab, sp_source_dir=self._spsc_source_dir(), sp_output_dir=self._spsc_output_dir(),
                                                   tree_dir=Path("tree"), merge_dir=self._merges_dir(), seqdb=self._seqdb_file(), serum_circles=True)
        for lab in ["cdc", "melb", "niid", "nimr"]:
            for virus_type, assay in [["h3", "hi"], ["h3", "neut"], ["h1", "hi"], ["bv", "hi"], ["by", "hi"]]:
                setattr(self, "sp_{}{}_{}".format(virus_type, assay if assay != "hi" else "", lab), sp_mf(virus_type=virus_type, assay=assay, lab=lab))
                setattr(self, "spsc_{}{}_{}".format(virus_type, assay if assay != "hi" else "", lab), spsc_mf(virus_type=virus_type, assay=assay, lab=lab))
        for virus_type, assay, lab in [["h1", "hi", "all"]]:
            setattr(self, "sp_{}{}_{}".format(virus_type, assay if assay != "hi" else "", lab), sp_mf(virus_type=virus_type, assay=assay, lab=lab))
            setattr(self, "spsc_{}{}_{}".format(virus_type, assay if assay != "hi" else "", lab), spsc_mf(virus_type=virus_type, assay=assay, lab=lab))

    # ----------------------------------------------------------------------
    # Serum coverage

    def serumcoverage_init(self):
        output_dir = Path("serumcoverage")
        for assay in ["hi", "neut"]:
            for merge in self._merges_dir().glob("*-h3-" + assay + ".ace"):
                output_file = output_dir.joinpath(merge.stem + ".json")
                if not output_file.exists():
                    cmd = "chart-serum-circles '{merge}' --json '{json}'".format(merge=merge, json=output_file)
                    module_logger.info(cmd)
                    subprocess.check_call(cmd, shell=True)

    def _serumcircle_report(self, merge_name):
        cmd = "chart-serum-circles '{merge}'".format(merge=self._merges_dir().joinpath(merge_name.replace("_", "-") + ".ace"))
        module_logger.info(cmd)
        subprocess.check_call(cmd, shell=True)

    def serumcircle_report_cdc_h3_hi(self): self._serumcircle_report("cdc_h3_hi")
    def serumcircle_report_cdc_h3_neut(self): self._serumcircle_report("cdc_h3_neut")
    def serumcircle_report_melb_h3_hi(self): self._serumcircle_report("melb_h3_hi")
    def serumcircle_report_melb_h3_neut(self): self._serumcircle_report("melb_h3_neut")
    def serumcircle_report_niid_h3_neut(self): self._serumcircle_report("niid_h3_neut")
    def serumcircle_report_nimr_h3_hi(self): self._serumcircle_report("nimr_h3_hi")
    def serumcircle_report_nimr_h3_neut(self): self._serumcircle_report("nimr_h3_neut")

    def _serumcoverage(self, lab, virus_type, assay):
        from .serum_coverage import make_serum_coverage_maps, make_serum_coverage_index
        try:
            make_serum_coverage_maps(virus_type=virus_type, assay=assay, lab=lab, output_dir=Path(virus_type + "-" + assay))
        finally:
            make_serum_coverage_index(virus_type=virus_type, assay=assay, lab=lab, output_dir=Path(""), pdf_dir=Path(virus_type + "-" + assay))

    def serumcoverage_cdc_h3_hi(self): self._serumcoverage(lab="cdc", virus_type="h3", assay="hi")
    def serumcoverage_cdc_h3_neut(self): self._serumcoverage(lab="cdc", virus_type="h3", assay="neut")
    def serumcoverage_melb_h3_hi(self): self._serumcoverage(lab="melb", virus_type="h3", assay="hi")
    def serumcoverage_melb_h3_neut(self): self._serumcoverage(lab="melb", virus_type="h3", assay="neut")
    def serumcoverage_niid_h3_neut(self): self._serumcoverage(lab="niid", virus_type="h3", assay="neut")
    def serumcoverage_nimr_h3_hi(self): self._serumcoverage(lab="nimr", virus_type="h3", assay="hi")
    def serumcoverage_nimr_h3_neut(self): self._serumcoverage(lab="nimr", virus_type="h3", assay="neut")

    def serumcoverage_h3_hi(self):
        failed = []
        for cmd in ["serumcoverage_cdc_h3_hi", "serumcoverage_melb_h3_hi", "serumcoverage_nimr_h3_hi"]:
            try:
                getattr(self, cmd)()
            except Exception as err:
                failed.append(err)
        if failed:
            module_logger.error("Maps failed:\n{}".format(pprint.pformat(failed)))
            raise RuntimeError("Maps failed")
        # self.serumcoverage_cdc_h3_hi()
        # self.serumcoverage_melb_h3_hi()
        # self.serumcoverage_nimr_h3_hi()
    h3_cov = serumcoverage_h3_hi

    def serumcoverage_h3_neut(self):
        failed = []
        for cmd in ["serumcoverage_cdc_h3_neut", "serumcoverage_melb_h3_neut", "serumcoverage_niid_h3_neut", "serumcoverage_nimr_h3_neut"]:
            try:
                getattr(self, cmd)()
            except Exception as err:
                failed.append(err)
        if failed:
            module_logger.error("Maps failed:\n{}".format(pprint.pformat(failed)))
            raise RuntimeError("Maps failed")
    h3neut_cov = serumcoverage_h3_neut

    # ----------------------------------------------------------------------

    # def _make_tree(self, virus_type):
    #     tree_dir = Path("tree")
    #     tree = tree_dir.joinpath(virus_type + ".tree.json.xz")
    #     pdf = tree_dir.joinpath(virus_type + ".tree.pdf")
    #     settings = tree_dir.joinpath(virus_type + ".tree.settings.json")
    #     if not settings.exists():
    #         subprocess.check_call("~/AD/bin/sigp --seqdb '{seqdb}' --init-settings '{settings}' '{tree}' '{pdf}'".format(seqdb=self._seqdb_file(), settings=settings, tree=tree, pdf=pdf), shell=True)
    #     else:
    #         subprocess.check_call("~/AD/bin/sigp --seqdb '{seqdb}' -s '{settings}' '{tree}' '{pdf}'".format(seqdb=self._seqdb_file(), settings=settings, tree=tree, pdf=pdf), shell=True)

    # ----------------------------------------------------------------------

    sVirusTypeOutputDir = {"h1": "h1", "h3": "h3", "bvic": "bv", "bv": "bv", "byam": "by", "by": "by"}

    def clade(self, virus_type, assay, lab=None):
        make_map(prefix="clade", virus_type=virus_type, assay=assay, lab=lab, mod="clade", output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def clade_6m(self, virus_type, assay, lab=None):
        make_map(prefix="clade-6m", virus_type=virus_type, assay=assay, lab=lab, mod="clade_6m", output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def clade_12m(self, virus_type, assay, lab=None):
        make_map(prefix="clade-12m", virus_type=virus_type, assay=assay, lab=lab, mod="clade_12m", output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def _aa_at(self, virus_type, assay, positions):
        mod = "aa_at_" + "_".join(str(pos) for pos in positions)
        make_map(prefix=mod.replace("_", "-"), virus_type=virus_type, assay=assay, mod=mod, output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def _geography(self, virus_type, assay):
        make_map(prefix="geography", virus_type=virus_type, assay=assay, mod="geography", output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def serology(self, virus_type, assay, lab=None):
        make_map(prefix="serology", virus_type=virus_type, assay=assay, lab=lab, mod="serology", output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)
    _serology = serology

    def _serum_sectors(self, virus_type, assay):
        make_map(prefix="serumsectors", virus_type=virus_type, assay=assay, mod="serum_sectors", output_dir=Path(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    # ----------------------------------------------------------------------

    def _seqdb_file(self):
        return self._db_dir().joinpath("seqdb.json.xz")

    def _get_merges(self):
        target_dir = self._merges_dir()
        module_logger.info("Updating merges in " + repr(str(target_dir)))
        from acmacs_whocc import acmacs
        acmacs.get_recent_merges(target_dir)
        self.h1_overlay()

    # @classmethod
    # def _use_dir(cls, name, mkdir=True):
    #     target_dir = Path(name).resolve(strict=False)
    #     if name and mkdir:
    #         target_dir.mkdir(parents=True, exist_ok=True)
    #     return target_dir

    # @classmethod
    # def r_dir(cls, name, mkdir=True, link_dir=None):
    #     if Path("/r/ramdisk-id").exists():
    #         target_dir = Path("/r/ssm-report", Path(".").resolve().name, name)
    #         if mkdir:
    #             target_dir.mkdir(parents=True, exist_ok=True)
    #         if name:
    #             if link_dir is None:
    #                 link_dir = name
    #             if not Path(link_dir).exists():
    #                 print(target_dir, link_dir)
    #                 Path(link_dir).symlink_to(target_dir)
    #     else:
    #         target_dir = cls._use_dir(name, mkdir=mkdir)
    #     return target_dir

    @classmethod
    def _db_dir(cls):
        return Path("db").resolve()

    @classmethod
    def _merges_dir(cls):
        return Path("merges").resolve()

    @classmethod
    def _log_dir(cls):
        return Path("log").resolve()

    @classmethod
    def _sp_output_dir(cls):
        cls._sp_source_dir()
        sp_dir = Path("sp")
        from .signature_page import signature_page_output_dir_init
        signature_page_output_dir_init(sp_dir)
        return sp_dir

    @classmethod
    def _sp_source_dir(cls):
        sp_dir = Path("sp")
        # module_logger.warning("sp_source_dir {}".format(sp_dir))
        from .signature_page import signature_page_source_dir_init
        signature_page_source_dir_init(sp_dir)
        return sp_dir

    @classmethod
    def _spsc_output_dir(cls):
        cls._spsc_source_dir()
        spsc_dir = Path("spsc")
        from .signature_page import signature_page_output_dir_init
        signature_page_output_dir_init(spsc_dir)
        return spsc_dir

    @classmethod
    def _spsc_source_dir(cls):
        spsc_dir = Path("spsc")
        # module_logger.warning("spsc_source_dir {}".format(spsc_dir))
        from .signature_page import signature_page_source_dir_init
        signature_page_source_dir_init(spsc_dir)
        return spsc_dir

    def merges_make_index_html(self):
        if self._merges_dir().exists():
            ace_files = list(self._merges_dir().glob("*.ace"))
            if ace_files:
                filename = self._merges_dir().joinpath("index.html")
                recent_ace_mtime = max((pn.stat() for pn in ace_files), key=lambda st: st.st_mtime).st_mtime
                if not filename.exists() or filename.stat().st_mtime < recent_ace_mtime:
                    from .init import _template_dir
                    substs = {
                        "title": "Merges",
                        "entries": "\n".join(f"<li><a href='{name}?acv=html'>{name}</a></li>" for name in sorted(pn.name for pn in self._merges_dir().glob("*.ace")))
                    }
                    filename.open("w").write(_template_dir().joinpath("merges-index.html").open().read() % substs)

# ----------------------------------------------------------------------

sRootIndexHtml = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <title>WHO VCM 2019 Southern Northern Hemisphere</title>
    <style>
      h1 { color: #0000A0; }
      ol { list-style-type: hebrew; }
      body {
        height: 100%;
        border-left: 3em solid #ddf;
        padding: 1em 0 0 1em;
        margin: 0;
      }
    </style>
  </head>
  <body>
    <h1>TC1 , WHO VCM 2019 Southern Northern Hemisphere</h1>
    <h2>Report</h2>
    <ul>
      <li><a href="report/report.pdf">Report</a></li>
    </ul>
    <h2>Phylogenetic Trees</h2>
    <ul>
      <li><a href="tree/h1.tree.pdf">H1</a></li>
      <li><a href="tree/h3.tree.pdf">H3</a></li>
      <li><a href="tree/bvic.tree.pdf">B/Vic</a></li>
      <li><a href="tree/byam.tree.pdf">B/Yam</a></li>
    </ul>
    <h2>Phylogenetic Trees and splitting into HZ sections</h2>
    <ul>
      <li><a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/H1.html">H1</a> (<a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/H1.safari.html">Safari</a>)</li>
      <li><a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/H3.html">H3</a> (<a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/H3.safari.html">Safari</a>)</li>
      <li><a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/BV.html">B/Vic</a> (<a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/BV.safari.html">Safari</a>)</li>
      <li><a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/BY.html">B/Yam</a> (<a href="https://notebooks.antigenic-cartography.org/eu/results/whocc-tree/YYYY-MMDD/BY.safari.html">Safari</a>)</li>
    </ul>
    <h2>Antigenic maps</h2>
    <ul>
      <li><a href="h1-hi/index.html">H1</a> (<a href="h1-hi/index.safari.html">Safari</a>)</li>
      <li><a href="h3-hi/index.html">H3 HI</a> (<a href="h3-hi/index.safari.html">Safari</a>)</li>
      <li><a href="h3-neut/index.html">H3 Neut</a> (<a href="h3-neut/index.safari.html">Safari</a>)</li>
      <li><a href="bv-hi/index.html">B/Vic</a> (<a href="bv-hi/index.safari.html">Safari</a>)</li>
      <li><a href="by-hi/index.html">B/Yam</a> (<a href="by-hi/index.safari.html">Safari</a>)</li>
    </ul>
    <h2>Geographic maps</h2>
    <ul>
      <li><a href="geo/index.html">for Chrome</a></li>
      <li><a href="geo/index.safari.html">for Safari</a></li>
    </ul>
    <h2>Stat</h2>
    <ul>
      <li><a href="stat/index.html">Stat</a></li>
    </ul>
    <h2>Signature pages</h2>
    <ul>
      <li><a href="report/addendum.pdf">Pdf with all signature pages (Addendum)</a></li>
      <li><a href="sp/index.html">Web page with multiple pdfs, big and slow</a></li>
    </ul>
    <h2>Serum coverage</h2>
    <p>Please visit index pages linked below and read the instructions at the top of the pages.</p>
    <ul>
      <li><a href="index-serumcoverage-cdc-h3-hi.html">CDC H3 HI</a> (<a href="index-serumcoverage-cdc-h3-hi.safari.html">Safari</a>)</li>
      <li><a href="index-serumcoverage-nimr-h3-hi.html">Crick H3 HI</a> (<a href="index-serumcoverage-nimr-h3-hi.safari.html">Safari</a>)</li>
      <li><a href="index-serumcoverage-melb-h3-hi.html">VIDRL H3 HI</a> (<a href="index-serumcoverage-melb-h3-hi.safari.html">Safari</a>)</li>
      <br>
      <li><a href="index-serumcoverage-cdc-h3-neut.html">CDC H3 Neut</a> (<a href="index-serumcoverage-cdc-h3-neut.safari.html">Safari</a>)</li>
      <li><a href="index-serumcoverage-nimr-h3-neut.html">Crick H3 Neut</a> (<a href="index-serumcoverage-nimr-h3-neut.safari.html">Safari</a>)</li>
      <li><a href="index-serumcoverage-niid-h3-neut.html">NIID H3 Neut</a> (<a href="index-serumcoverage-niid-h3-neut.safari.html">Safari</a>)</li>
      <li><a href="index-serumcoverage-melb-h3-neut.html">VIDRL H3 Neut</a> (<a href="index-serumcoverage-melb-h3-neut.safari.html">Safari</a>)</li>
    </ul>
  </body>
</html>
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
