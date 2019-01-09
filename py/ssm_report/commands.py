import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import re, subprocess, shutil, pprint

from .map import make_map, make_map_for_lab, make_ts, make_map_information, make_index_html as maps_make_index_html, make_index_clade_html
from .stat import make_stat
from .geographic import make_geographic
from .signature_page import tree_make, tree_make_aa_pos, signature_page_make, trees_get_from_albertine

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
            make_index_clade_html(self.r_dir(""))

    def init(self):
        """initialize ssm report data directory structure"""
        self._init_git()
        self._get_dbs()
        self._get_merges()
        self._use_dir("tree")
        self.r_dir("sp")
        from .settings import make_settings
        make_settings(force=self._force)

    def init_git(self):
        self._init_git()

    def list(self):
        """list available commands"""
        from inspect import ismethod
        for cmdname in dir(self):
            if cmdname[0] != "_" and cmdname[-1] != "_":
                cmd = getattr(self, cmdname)
                if ismethod(cmd):
                    print(cmdname, "-", cmd.__doc__)

    def remake_seqdb(self):
        """Re-generate seqdb from from fasta files"""
        seqdb_filename = self._seqdb_file()
        if seqdb_filename.exists():
            from acmacs_base.files import backup_file
            backup_file(seqdb_filename)
            seqdb_filename.unlink()
        self._get_seqdb()

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
        make_stat(stat_dir=self.r_dir("stat"), hidb_dir=self._db_dir(), force=self._force)

    def geo(self):
        """make geographic time series"""
        make_geographic(geo_dir=self.r_dir("geo"), db_dir=self._db_dir(), force=self._force)

        # ----------------------------------------------------------------------

    def map_settings(self):
        self.h1_map_settings()
        self.h3_map_settings()
        self.h3neut_map_settings()
        self.bvic_map_settings()
        self.byam_map_settings()

    def h1_map_settings(self):
        from .settings import make_map_settings
        make_map_settings(virus_type='h1', assay='hi', force=self._force)

    def h3_map_settings(self):
        from .settings import make_map_settings
        make_map_settings(virus_type='h3', assay='hi', force=self._force)

    def h3neut_map_settings(self):
        from .settings import make_map_settings
        make_map_settings(virus_type='h3', assay='neut', force=self._force)

    def bvic_map_settings(self):
        from .settings import make_map_settings
        make_map_settings(virus_type='bvic', assay='hi', force=self._force)

    def byam_map_settings(self):
        from .settings import make_map_settings
        make_map_settings(virus_type='byam', assay='hi', force=self._force)

        # ----------------------------------------------------------------------

    def get_trees_from_albertine(self):
        trees_get_from_albertine(tree_dir=self._use_dir("tree"))

    def tree(self):
        """Generate tree images for all subtypes."""
        self.h1_tree()
        self.h3_tree()
        self.bvic_tree()
        self.byam_tree()

    def h1_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h1", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def h1_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="h1", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def h3_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h3", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def h3_tree_142(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h3", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"), tree_infix=".142")

    def bv_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="bv", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))
    bvic_tree = bv_tree

    def by_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="by", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))
    byam_tree = by_tree

    def h1_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="h1", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def h3_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="h3", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def bv_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="bv", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))
    bvic_tree_aa = bv_tree_aa

    def by_tree_aa(self):
        """instructions on making phylogenetic trees"""
        tree_make_aa_pos(subtype="by", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))
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
        self._tree_information("bvic")

    def byam_tree_information(self):
        self._tree_information("byam")

    def _tree_information(self, virus_type):

        tree_dir = self._use_dir("tree")
        from .signature_page import tree_make_information_settings
        tree_make_information_settings(virus_type=virus_type, tree_dir=tree_dir)
        tree_make(subtype=virus_type, tree_dir=tree_dir, seqdb=self._seqdb_file(), output_dir=self.r_dir("information", link_dir="i"), settings_infix="information")

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
        self.serology(virus_type="bvic", assay="hi")()
        #self.bvic_serum_sectors()
        self.bvic_ts()
    bv = bvic

    def byam(self):
        self.byam_clade()
        self.byam_geography()
        self.serology(virus_type="byam", assay="hi")()
        #self.byam_serum_sectors()
        self.byam_ts()
    by = byam

    def report(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=self.r_dir(""), output_dir=self.r_dir("report"))

    def report_abbreviated(self):
        from .report import make_report_abbreviated
        make_report_abbreviated(source_dir=Path(".").resolve(), source_dir_2=self.r_dir(""), output_dir=self.r_dir("report"))

    def report_serumcoverage(self):
        from .report import make_report_serumcoverage
        make_report_serumcoverage(source_dir=Path(".").resolve(), source_dir_2=self.r_dir(""), output_dir=self.r_dir("report"))

    def addendum(self):
        from .report import make_signature_page_addendum
        make_signature_page_addendum(source_dir=self.r_dir("sp"), output_dir=self.r_dir("report"))

    def report_3(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=self.r_dir(""), output_dir=self.r_dir("report"), report_settings_file="report-addendum-3.json")

    def report_4(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=self.r_dir(""), output_dir=self.r_dir("report"), report_settings_file="report-addendum-4.json")

    def report_5(self):
        from .report import make_report
        make_report(source_dir=Path(".").resolve(), source_dir_2=self.r_dir(""), output_dir=self.r_dir("report"), report_settings_file="report-addendum-5.json")

    def update_merges(self):
        target_dir = self._merges_dir()
        module_logger.info("Updating merges in " + repr(str(target_dir)))
        from acmacs_whocc import acmacs
        acmacs.get_recent_merges(target_dir, force=True)

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
        self._clade(virus_type="h1", assay="hi")
    h1_clades = h1_clade

    def h1_serology(self):
        self.serology(virus_type="h1", assay="hi")

    def h1_geography(self):
        self._geography(virus_type="h1", assay="hi")
    h1_geo = h1_geography

    def h1_ts(self, lab=None):
        make_ts(virus_type="h1", assay="hi", lab=lab, output_dir=self.r_dir("h1-hi"), force=self._force)

    def h1_information(self):
        make_map_information(virus_type="h1", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

    # ----------------------------------------------------------------------
    # H3 HI

    def h3_clade(self):
        self._clade(virus_type="h3", assay="hi")
        self._clade_6m(virus_type="h3", assay="hi")
        self._clade_12m(virus_type="h3", assay="hi")
    h3_clades = h3_clade

    def h3_aa_at_142(self):
        self._aa_at(virus_type="h3", assay="hi", positions=[142])

    def h3_geography(self):
        self._geography(virus_type="h3", assay="hi")
    h3_geo = h3_geography

    def h3_ts(self, lab=None):
        make_ts(virus_type="h3", assay="hi", lab=lab, output_dir=self.r_dir("h3-hi"), force=self._force)

    def h3_serology(self):
        self.serology(virus_type="h3", assay="hi")

    def h3_serum_sectors(self):
        self._serum_sectors(virus_type="h3", assay="hi")

    def h3_information(self):
        make_map_information(virus_type="h3", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

    # ----------------------------------------------------------------------
    # H3 Neut

    def h3neut_clade(self):
        self._clade(virus_type="h3", assay="neut")
        self._clade_6m(virus_type="h3", assay="neut")
        self._clade_12m(virus_type="h3", assay="neut")
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
        make_ts(virus_type="h3", assay="neut", lab=lab, output_dir=self.r_dir("h3-neut"), force=self._force)
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
        output_dir = self.r_dir(virus_type + "-" + assay)
        for mod in ["clade", "clade_6m", "clade_12m", "aa_at_142", "geography", "serology"]:
            make_map_for_lab(prefix=mod.replace("_", "-"), virus_type=virus_type, assay=assay, lab=lab, infix=infix, mod=mod, output_dir=output_dir, settings_files=settings_files, open_image=self._open_image)
        make_ts(virus_type=virus_type, assay=assay, lab=lab, output_dir=output_dir, infix=infix, force=self._force)
        from . import map as map_m
        map_m.sDirsForIndex.add(output_dir)
    h3n_niid_oseltamivir = h3neut_niid_oseltamivir

    def h3neut_serum_sectors(self):
        self._serum_sectors(virus_type="h3", assay="neut")

    def h3neut_information(self):
        make_map_information(virus_type="h3", assay="neut", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

    # ----------------------------------------------------------------------
    # BVIC HI

    def bvic_clade(self):
        self._clade(virus_type="bvic", assay="hi")
        self._clade_6m(virus_type="bvic", assay="hi")
        self._clade_12m(virus_type="bvic", assay="hi")
    bv_clade = bvic_clade
    bv_clades = bvic_clade
    bvic_clades = bvic_clade

    def bvic_geography(self):
        self._geography(virus_type="bvic", assay="hi")
    bv_geo = bvic_geography
    bvic_geo = bvic_geography

    def bvic_ts(self, lab=None):
        make_ts(virus_type="bvic", assay="hi", lab=lab, output_dir=self.r_dir("bvic-hi"), force=self._force)
    bv_ts = bvic_ts

    def bvic_serology(self):
        self.serology(virus_type="bvic", assay="hi")
    bv_serology = bvic_serology

    def bvic_information(self):
        make_map_information(virus_type="bvic", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)
    bv_information = bvic_information

    # ----------------------------------------------------------------------
    # BYAM HI

    def byam_clade(self):
        self._clade(virus_type="byam", assay="hi")
        self._clade_6m(virus_type="byam", assay="hi")
        self._clade_12m(virus_type="byam", assay="hi")
    byam_clades = byam_clade
    by_clades = byam_clade
    by_clade = byam_clade

    def byam_geography(self):
        self._geography(virus_type="byam", assay="hi")
    byam_geo = byam_geography
    by_geo = byam_geography

    def byam_ts(self, lab=None):
        make_ts(virus_type="byam", assay="hi", lab=lab, output_dir=self.r_dir("byam-hi"), force=self._force)
    by_ts = byam_ts

    def byam_serology(self):
        self.serology(virus_type="byam", assay="hi")
    by_serology = byam_serology

    def byam_information(self):
        make_map_information(virus_type="byam", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)
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
        self.sp_bvic_cdc()
        self.sp_bvic_melb()
        self.sp_bvic_niid()
        self.sp_bvic_nimr()

    def sp_byam(self):
        self.sp_byam_cdc()
        self.sp_byam_melb()
        self.sp_byam_niid()
        self.sp_byam_nimr()

    def _make_sp_makers(self):
        def mf(virus_type, assay, lab):
            return lambda: signature_page_make(virus_type=virus_type, assay=assay, lab=lab, sp_source_dir=self._sp_source_dir(), sp_output_dir=self._sp_output_dir(),
                                                   tree_dir=self._use_dir("tree"), merge_dir=self._merges_dir(), seqdb=self._seqdb_file())
        for lab in ["cdc", "melb", "niid", "nimr"]:
            for virus_type, assay in [["h3", "hi"], ["h3", "neut"], ["h1", "hi"], ["bvic", "hi"], ["byam", "hi"]]:
                setattr(self, "sp_{}{}_{}".format(virus_type, assay if assay != "hi" else "", lab), mf(virus_type=virus_type, assay=assay, lab=lab))
        for virus_type, assay, lab in [["h1", "hi", "all"]]:
            setattr(self, "sp_{}{}_{}".format(virus_type, assay if assay != "hi" else "", lab), mf(virus_type=virus_type, assay=assay, lab=lab))

    # ----------------------------------------------------------------------
    # Serum coverage

    def serumcoverage_init(self):
        output_dir = self._use_dir("serumcoverage")
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
            make_serum_coverage_maps(virus_type=virus_type, assay=assay, lab=lab, output_dir=self.r_dir(virus_type + "-" + assay))
        finally:
            make_serum_coverage_index(virus_type=virus_type, assay=assay, lab=lab, output_dir=self.r_dir(""), pdf_dir=self.r_dir(virus_type + "-" + assay))

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
    #     tree_dir = self._use_dir("tree")
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
        make_map(prefix="clade", virus_type=virus_type, assay=assay, lab=lab, mod="clade", output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)
    _clade = clade

    def _clade_6m(self, virus_type, assay, lab=None):
        make_map(prefix="clade-6m", virus_type=virus_type, assay=assay, lab=lab, mod="clade_6m", output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)
    clade6m = _clade_6m

    def _clade_12m(self, virus_type, assay, lab=None):
        make_map(prefix="clade-12m", virus_type=virus_type, assay=assay, lab=lab, mod="clade_12m", output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)
    clade12m = _clade_12m

    def _aa_at(self, virus_type, assay, positions):
        mod = "aa_at_" + "_".join(str(pos) for pos in positions)
        make_map(prefix=mod.replace("_", "-"), virus_type=virus_type, assay=assay, mod=mod, output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def _geography(self, virus_type, assay):
        make_map(prefix="geography", virus_type=virus_type, assay=assay, mod="geography", output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    def serology(self, virus_type, assay, lab=None):
        make_map(prefix="serology", virus_type=virus_type, assay=assay, lab=lab, mod="serology", output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)
    _serology = serology

    def _serum_sectors(self, virus_type, assay):
        make_map(prefix="serumsectors", virus_type=virus_type, assay=assay, mod="serum_sectors", output_dir=self.r_dir(self.sVirusTypeOutputDir[virus_type] + "-" + assay), force=self._force, open_image=self._open_image)

    # ----------------------------------------------------------------------

    def _get_dbs(self):
        self._get_locdb()
        self._get_hidb()
        self._get_seqdb()

    def _get_hidb(self):
        target_dir = self._db_dir()
        module_logger.info("Updating hidb in " + repr(str(target_dir)))
        subprocess.check_call("rsync -av 'albertine:AD/data/hidb5.*.{{json.xz,hidb5b}}' '{}'".format(target_dir), shell=True)

    def _get_locdb(self):
        target_dir = self._db_dir()
        module_logger.info("Updating locdb in " + repr(str(target_dir)))
        locdb_file = target_dir.joinpath("locationdb.json.xz")
        if not locdb_file.exists():
            locdb_file.symlink_to(Path("~/AD/data/locationdb.json.xz").expanduser().resolve())

    def _get_seqdb(self):
        seqdb_filename = self._seqdb_file()
        shutil.copy(Path("~/AD/data/seqdb.json.xz").expanduser().resolve(), seqdb_filename)

    # def _get_seqdb_before_2019(self):
    #     seqdb_filename = self._seqdb_file()
    #     module_logger.info("Updating seqdb in " + repr(str(seqdb_filename)))
    #     fasta_files = sorted(Path("~/ac/tables-store/sequences").expanduser().resolve().glob("*.fas.*"))
    #     seqdb_mtime = seqdb_filename.exists() and seqdb_filename.stat().st_mtime
    #     if not seqdb_mtime or any(ff.stat().st_mtime >= seqdb_mtime for ff in fasta_files):
    #         module_logger.info("Creating seqdb from " + str(len(fasta_files)) + " fasta files")
    #         subprocess.check_call("seqdb-create --db '{seqdb_filename}' --hidb-dir '{hidb_dir}' --match-hidb --clades --save-not-found-locations '{not_found_locations}' {verbose} '{fasta_files}'".format(
    #             seqdb_filename=seqdb_filename, hidb_dir=self._db_dir(), not_found_locations=self._log_dir().joinpath("not-found-locations.txt"), verbose="-v" if self._verbose else "",
    #             fasta_files="' '".join(str(f) for f in fasta_files)), shell=True)
    #     else:
    #         module_logger.info('seqdb is up to date')

    def _seqdb_file(self):
        return self._db_dir().joinpath("seqdb.json.xz")

    def _get_merges(self):
        target_dir = self._merges_dir()
        module_logger.info("Updating merges in " + repr(str(target_dir)))
        from acmacs_whocc import acmacs
        acmacs.get_recent_merges(target_dir)
        self.h1_overlay()

    @classmethod
    def _use_dir(cls, name, mkdir=True):
        target_dir = Path(name).resolve(strict=False)
        if name and mkdir:
            target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir

    @classmethod
    def r_dir(cls, name, mkdir=True, link_dir=None):
        if Path("/r/ramdisk-id").exists():
            target_dir = Path("/r/ssm-report", Path(".").resolve().name, name)
            if mkdir:
                target_dir.mkdir(parents=True, exist_ok=True)
            if name:
                if link_dir is None:
                    link_dir = name
                if not Path(link_dir).exists():
                    print(target_dir, link_dir)
                    Path(link_dir).symlink_to(target_dir)
        else:
            target_dir = cls._use_dir(name, mkdir=mkdir)
        return target_dir

    @classmethod
    def _db_dir(cls):
        return cls._use_dir("db")

    @classmethod
    def _merges_dir(cls):
        return cls._use_dir("merges")

    @classmethod
    def _log_dir(cls):
        return cls.r_dir("log")

    @classmethod
    def _sp_output_dir(cls):
        cls._sp_source_dir()
        sp_dir = cls.r_dir("sp")
        from .signature_page import signature_page_output_dir_init
        signature_page_output_dir_init(sp_dir)
        return sp_dir

    @classmethod
    def _sp_source_dir(cls):
        sp_dir = cls._use_dir("sp")
        # module_logger.warning("sp_source_dir {}".format(sp_dir))
        from .signature_page import signature_page_source_dir_init
        signature_page_source_dir_init(sp_dir)
        return sp_dir

    def _init_git(self):
        project_git_dir = Path(".").resolve().name + ".git"
        module_logger.info("init_git {}".format(project_git_dir))
        # remote
        if not subprocess.call("ssh albertine '[[ -f who-reports/{p}/HEAD ]]'".format(p=project_git_dir), shell=True):
            module_logger.info("Remote git repo exists")
        elif not subprocess.call("ssh albertine '[[ -e who-reports/{p} ]]'".format(p=project_git_dir), shell=True):
            raise RuntimeError("albertine:who-reports/{p} present but it is not a git repository".format(p=project_git_dir))
        else:
            module_logger.info("Creating remote git repo")
            subprocess.check_call("ssh albertine 'mkdir who-reports/{p} && cd who-reports/{p} && git init --bare'".format(p=project_git_dir), shell=True)

        # local
        if not Path(".gitignore").exists():
            open(".gitignore", "w").write("bvic-hi\nbyam-hi\ndb\ngeo\nh1-hi\nh3-hi\nh3-neut\nlog\nmerges\nreport\nstat\n.backup\n*.pdf\n*.ace\n*.acd1.xz\n*.acd1.bz2\n*.save\n*.save.xz\n.#*\n")
        if not Path("rename-report-on-server").exists():
            open("rename-report-on-server", "w").write("#! /bin/bash\ncd $(dirname $0) &&\nssh i19 \"cd $(pwd); if [[ -d report && -f report/report.pdf ]]; then mv report/report.pdf report/report.\$(stat -c %y report/report.pdf | sed 's/\..*//g; s/-//g; s/://g; s/ /-/g').pdf; else echo no report dir; fi\"\n")
            Path("rename-report-on-server").chmod(0o700)
        if not Path("rr").exists():
            open("rr", "w").write("#! /bin/bash\ncd $(dirname $0) &&\n$ACMACSD_ROOT/bin/ssm-report --working-dir . report &&\n./rename-report-on-server &&\n./sy\n")
            Path("rr").chmod(0o700)
        if not Path("sy").exists():
            # open("sy", "w").write("#! /bin/bash\ncd $(dirname $0) &&\ngit add --all &&\nif git commit --dry-run; then git commit -m 'sy'; fi &&\ngit fetch &&\n( git merge --no-commit --no-ff || ( echo && echo Use '\"git merge\"' to merge, then edit merged file && echo && false ) ) &&\ngit push &&\nsyput -f \"--exclude bvic-hi --exclude byam-hi --exclude geo --exclude h1-hi --exclude h3-hi --exclude h3-neut --exclude log --exclude report --exclude sp --exclude stat --exclude .backup\" &&\nsyput /r/ssm-report/\"$(basename ${PWD})\" \"${PWD#$HOME/}\"")
            open("sy", "w").write("#! /bin/bash\ncd $(dirname $0) &&\ngit add --all &&\nif git commit --dry-run; then git commit -m 'sy'; fi &&\ngit fetch &&\n( git merge --no-commit --no-ff || ( echo && echo Use '\"git merge\"' to merge, then edit merged file && echo && false ) ) &&\ngit push &&\nsyput")
            Path("sy").chmod(0o700)
        index_html = self.r_dir("").joinpath("index.html")
        if not index_html.exists():
            index_html.open("w").write(sRootIndexHtml)

        if Path(".git").is_dir():
            module_logger.info("local repository present")
        elif Path(".git").exists():
            raise RuntimeError(".git exists and it is not a directory")
        else:
            subprocess.check_call("git init && git add rr .gitignore && git commit -m 'ssm-report init_git' && git remote add origin ssh://albertine/home/eu/who-reports/{p} && git push --set-upstream origin master".format(p=project_git_dir), shell=True)

# ----------------------------------------------------------------------

sRootIndexHtml = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <title>WHO VCM 2018 Southern Northern Hemisphere</title>
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
    <h1>TC1 , WHO VCM 2018 Southern Northern Hemisphere</h1>
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
      <li><a href="bvic-hi/index.html">B/Vic</a> (<a href="bvic-hi/index.safari.html">Safari</a>)</li>
      <li><a href="byam-hi/index.html">B/Yam</a> (<a href="byam-hi/index.safari.html">Safari</a>)</li>
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
