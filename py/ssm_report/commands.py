import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import subprocess

from .map import make_map, make_ts, make_map_information, make_index_html as maps_make_index_html, make_index_clade_html
from .stat import make_stat
from .geographic import make_geographic
from .signature_page import tree_make, signature_page_make, trees_get_from_albertine

# ======================================================================

class Error (RuntimeError): pass

# ----------------------------------------------------------------------

def process_commands(commands, verbose, force):
    try:
        Processor(verbose=verbose, force=force)._process(commands)
    except Error as err:
        module_logger.error("ERROR: " + str(err))
        return 1
    return 0

# ----------------------------------------------------------------------

class Processor:

    def __init__(self, verbose, force):
        self._verbose = verbose
        self._force = force
        self._make_sp_makers()

    def _process(self, commands):
        if not commands:
            self.list()
        else:
            for command in commands:
                command = command.replace("-", "_").lower()
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

    def h3_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="h3", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def bvic_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="bvic", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def byam_tree(self):
        """instructions on making phylogenetic trees"""
        tree_make(subtype="byam", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("tree", link_dir="t"))

    def tree_information(self):
        """Generate tree images for all subtypes."""
        self.h1_tree_information()
        self.h3_tree_information()
        self.bvic_tree_information()
        self.byam_tree_information()

    def h1_tree_information(self):
        tree_make(subtype="h1", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("information", link_dir="i"), settings_infix="information")

    def h3_tree_information(self):
        tree_make(subtype="h3", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("information", link_dir="i"), settings_infix="information")

    def bvic_tree_information(self):
        tree_make(subtype="bvic", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("information", link_dir="i"), settings_infix="information")

    def byam_tree_information(self):
        tree_make(subtype="byam", tree_dir=self._use_dir("tree"), seqdb=self._seqdb_file(), output_dir=self.r_dir("information", link_dir="i"), settings_infix="information")

        # ----------------------------------------------------------------------

    def h3(self):
        self.h3_clade()
        self.h3_ts()
        self.h3_geography()
        self.h3_serology()
        # #self.h3_serum_sectors()
        self.h3_serum_coverage()

    def h3neut(self):
        self.h3neut_clade()
        self.h3neut_ts()
        self.h3neut_geography()
        self.h3neut_serology()
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
        self.bvic_serology()
        #self.bvic_serum_sectors()
        self.bvic_ts()

    def byam(self):
        self.byam_clade()
        self.byam_geography()
        self.byam_serology()
        #self.byam_serum_sectors()
        self.byam_ts()

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
        from . import acmacs
        acmacs.get_recent_merges(target_dir, force=True)

    def h1_overlay(self):
        target_dir = self._merges_dir()
        from . import acmacs
        acmacs.make_h1pdm_overlay(target_dir, log_dir=self._log_dir(), force=True)

    def update_hidb(self):
        self._get_hidb()

    # ----------------------------------------------------------------------
    # H1 HI

    def h1_clade(self):
        self._clade(virus_type="h1", assay="hi")
    h1_clades = h1_clade

    def h1_serology(self):
        self._serology(virus_type="h1", assay="hi")

    def h1_geography(self):
        self._geography(virus_type="h1", assay="hi")
    h1_geo = h1_geography

    def h1_ts(self):
        self._ts(virus_type="h1", assay="hi")

    def h1_information(self):
        make_map_information(virus_type="h1", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

    # ----------------------------------------------------------------------
    # H3 HI

    def h3_clade(self):
        self._clade(virus_type="h3", assay="hi")
        self._clade_6m(virus_type="h3", assay="hi")
        self._clade_12m(virus_type="h3", assay="hi")
    h3_clades = h3_clade

    def h3_serology(self):
        self._serology(virus_type="h3", assay="hi")

    def h3_geography(self):
        self._geography(virus_type="h3", assay="hi")
    h3_geo = h3_geography

    def h3_ts(self):
        self._ts(virus_type="h3", assay="hi")

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

    def h3neut_serology(self):
        self._serology(virus_type="h3", assay="neut")
    h3n_serology = h3neut_serology

    def h3neut_geography(self):
        self._geography(virus_type="h3", assay="neut")
    h3neut_geo = h3neut_geography
    h3n_geo = h3neut_geography

    def h3neut_ts(self):
        self._ts(virus_type="h3", assay="neut")
    h3n_ts = h3neut_ts

    def h3neut_serum_sectors(self):
        self._serum_sectors(virus_type="h3", assay="neut")

    def h3neut_information(self):
        make_map_information(virus_type="h3", assay="neut", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

    # ----------------------------------------------------------------------
    # BVIC HI

    def bvic_clade(self):
        self._clade(virus_type="bvic", assay="hi")
    bvic_clades = bvic_clade

    def bvic_serology(self):
        self._serology(virus_type="bvic", assay="hi")

    def bvic_geography(self):
        self._geography(virus_type="bvic", assay="hi")
    bvic_geo = bvic_geography

    def bvic_ts(self):
        self._ts(virus_type="bvic", assay="hi")

    def bvic_information(self):
        make_map_information(virus_type="bvic", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

    # ----------------------------------------------------------------------
    # BYAM HI

    def byam_clade(self):
        self._clade(virus_type="byam", assay="hi")
        self._clade_6m(virus_type="byam", assay="hi")
        self._clade_12m(virus_type="byam", assay="hi")
    byam_clades = byam_clade

    def byam_serology(self):
        self._serology(virus_type="byam", assay="hi")

    def byam_geography(self):
        self._geography(virus_type="byam", assay="hi")
    byam_geo = byam_geography

    def byam_ts(self):
        self._ts(virus_type="byam", assay="hi")

    def byam_information(self):
        make_map_information(virus_type="byam", assay="hi", output_dir=self.r_dir("information", link_dir="i"), force=self._force)

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
        from .map import make_serum_coverage_maps, make_serum_coverage_index
        make_serum_coverage_maps(virus_type=virus_type, assay=assay, lab=lab, output_dir=self.r_dir(virus_type + "-" + assay))
        make_serum_coverage_index(virus_type=virus_type, assay=assay, lab=lab, output_dir=self.r_dir(""), pdf_dir=self.r_dir(virus_type + "-" + assay))

    def serumcoverage_cdc_h3_hi(self): self._serumcoverage(lab="cdc", virus_type="h3", assay="hi")
    def serumcoverage_cdc_h3_neut(self): self._serumcoverage(lab="cdc", virus_type="h3", assay="neut")
    def serumcoverage_melb_h3_hi(self): self._serumcoverage(lab="melb", virus_type="h3", assay="hi")
    def serumcoverage_melb_h3_neut(self): self._serumcoverage(lab="melb", virus_type="h3", assay="neut")
    def serumcoverage_niid_h3_neut(self): self._serumcoverage(lab="niid", virus_type="h3", assay="neut")
    def serumcoverage_nimr_h3_hi(self): self._serumcoverage(lab="nimr", virus_type="h3", assay="hi")
    def serumcoverage_nimr_h3_neut(self): self._serumcoverage(lab="nimr", virus_type="h3", assay="neut")

    def serumcoverage_h3_hi(self):
        self.serumcoverage_cdc_h3_hi()
        self.serumcoverage_melb_h3_hi()
        self.serumcoverage_nimr_h3_hi()
    h3_cov = serumcoverage_h3_hi

    def serumcoverage_h3_neut(self):
        self.serumcoverage_cdc_h3_neut()
        self.serumcoverage_melb_h3_neut()
        self.serumcoverage_niid_h3_neut()
        self.serumcoverage_nimr_h3_neut()
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

    def _clade(self, virus_type, assay):
        make_map(prefix="clade", virus_type=virus_type, assay=assay, mod="clade", output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

    def _clade_6m(self, virus_type, assay):
        make_map(prefix="clade-6m", virus_type=virus_type, assay=assay, mod="clade_6m", output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

    def _clade_12m(self, virus_type, assay):
        make_map(prefix="clade-12m", virus_type=virus_type, assay=assay, mod="clade_12m", output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

    def _geography(self, virus_type, assay):
        make_map(prefix="geography", virus_type=virus_type, assay=assay, mod="geography", output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

    def _serology(self, virus_type, assay):
        make_map(prefix="serology", virus_type=virus_type, assay=assay, mod="serology", output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

    def _serum_sectors(self, virus_type, assay):
        make_map(prefix="serumsectors", virus_type=virus_type, assay=assay, mod="serum_sectors", output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

    def _ts(self, virus_type, assay):
        make_ts(virus_type=virus_type, assay=assay, output_dir=self.r_dir(virus_type + "-" + assay), force=self._force)

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
        module_logger.info("Updating seqdb in " + repr(str(seqdb_filename)))
        fasta_files = sorted(Path("~/ac/tables-store/sequences").expanduser().resolve().glob("*.fas.bz2"))
        seqdb_mtime = seqdb_filename.exists() and seqdb_filename.stat().st_mtime
        if not seqdb_mtime or any(ff.stat().st_mtime >= seqdb_mtime for ff in fasta_files):
            module_logger.info("Creating seqdb from " + str(len(fasta_files)) + " fasta files")
            subprocess.check_call("ad seqdb-create --db '{seqdb_filename}' --hidb-dir '{hidb_dir}' --match-hidb --clades --save-not-found-locations '{not_found_locations}' {verbose} '{fasta_files}'".format(
                seqdb_filename=seqdb_filename, hidb_dir=self._db_dir(), not_found_locations=self._log_dir().joinpath("not-found-locations.txt"), verbose="-v" if self._verbose else "",
                fasta_files="' '".join(str(f) for f in fasta_files)), shell=True)
        else:
            module_logger.info('seqdb is up to date')

    def _seqdb_file(self):
        return self._db_dir().joinpath("seqdb.json.xz")

    def _get_merges(self):
        target_dir = self._merges_dir()
        module_logger.info("Updating merges in " + repr(str(target_dir)))
        from . import acmacs
        acmacs.get_recent_merges(target_dir)
        acmacs.make_h1pdm_overlay(target_dir, log_dir=self._log_dir())

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
            open(".gitignore", "w").write("bvic-hi\nbyam-hi\ndb\ngeo\nh1-hi\nh3-hi\nh3-neut\nlog\nmerges\nreport\nstat\n.backup\n")
        if not Path("rr").exists():
            open("rr", "w").write("#! /bin/bash\ncd $(dirname $0) &&\n$ACMACSD_ROOT/bin/ssm-report --working-dir . report &&\n./sy\n")
            Path("rr").chmod(0o700)
        if not Path("sy").exists():
            open("sy", "w").write("#! /bin/bash\ncd $(dirname $0) &&\ngit add --all &&\nif git commit --dry-run; then git commit -m 'sy'; fi &&\ngit fetch &&\n( git merge --no-commit --no-ff || ( echo && echo Use '\"git merge\"' to merge, then edit merged file && echo && false ) ) &&\ngit push &&\nsyput -f \"--exclude bvic-hi --exclude byam-hi --exclude geo --exclude h1-hi --exclude h3-hi --exclude h3-neut --exclude log --exclude report --exclude sp --exclude stat --exclude .backup\" &&\nsyput /r/ssm-report/\"$(basename ${PWD})\" \"${PWD#$HOME/}\"")
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
    <h2>Antigenic maps</h2>
    <ul>
      <li><a href="h3-hi/index.html">H3 HI</a></li>
      <li><a href="h3-neut/index.html">H3 Neut</a></li>
      <li><a href="h1-hi/index.html">H1</a></li>
      <li><a href="bvic-hi/index.html">B/Vic</a></li>
      <li><a href="byam-hi/index.html">B/Yam</a></li>
    </ul>
    <h2>Signature pages</h2>
    <ul>
      <li><a href="sp/index.html">H3, H3 neut, H1, B/Vic, B/Yam</a></li>
    </ul>
  </body>
</html>
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
