import logging; module_logger = logging.getLogger(__name__)
from pathlib import Path
import sys, re, subprocess, datetime, collections, itertools

from acmacs_base.json import read_json
from . import latex
from .map import sLabDisplayName

# ======================================================================

def make_report(source_dir, source_dir_2, output_dir):
    report_settings = read_json("report.json")
    report = LatexReport(source_dir=source_dir, source_dir_2=source_dir_2, output_dir=output_dir, output_name="report.tex", settings=report_settings)
    report.make()
    report.compile(update_toc=True)
    report.view()

# ----------------------------------------------------------------------

def make_report_abbreviated(source_dir, source_dir_2, output_dir):
    report_settings = read_json("report-abbreviated.json")
    report = LatexReport(source_dir=source_dir, source_dir_2=source_dir_2, output_dir=output_dir, output_name="report-abbreviated.tex", settings=report_settings)
    report.make()
    report.compile(update_toc=True)
    report.view()

# ----------------------------------------------------------------------

def make_report_serumcoverage(source_dir, source_dir_2, output_dir):
    report_settings = read_json("report-serumcoverage.json")
    report = LatexSerumCoverageAddendum(source_dir=source_dir, source_dir_2=source_dir_2, output_dir=output_dir, output_name="report-serumcoverage.tex", settings=report_settings)
    report.make()
    report.compile(update_toc=True)
    report.view()

# ----------------------------------------------------------------------

def make_signature_page_addendum(source_dir, output_dir):
    report_settings = read_json("report.json")
    addendum = LatexSignaturePageAddendum(source_dir=source_dir, output_dir=output_dir, settings=report_settings)
    addendum.make()
    addendum.compile(update_toc=True)
    addendum.view()

# ----------------------------------------------------------------------

class LatexReportError (Exception):
    pass

# ----------------------------------------------------------------------

class LatexReport:

    sLatexCommand = "cd '{run_dir}' && pdflatex -interaction=nonstopmode -file-line-error '{latex_source}'"
    sViewCommand = "open '{output}'"

    def __init__(self, source_dir, source_dir_2, output_dir, output_name, settings):
        self.source_dir = source_dir
        self.source_dir_2 = source_dir_2
        self.latex_source = output_dir.joinpath(output_name)
        self.settings = settings
        self.data = []
        settings_dates = settings["time_series"]["date"]
        self.start = datetime.datetime.strptime(settings_dates["start"], "%Y-%m-%d").date()
        self.end = datetime.datetime.strptime(settings_dates["end"], "%Y-%m-%d").date() # - datetime.timedelta(days=1)
        LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
        self.substitute = {
            "time_series_start": self.start.strftime("%B %Y"),
            "time_series_end": (self.end - datetime.timedelta(days=1)).strftime("%B %Y"),
            "documentclass": "\documentclass[a4paper,12pt]{article}",
            "cover_top_space": "130pt",
            "cover_after_meeting_date_space": "180pt",
            "usepackage": "",
            "cover_quotation": "\\quotation",
            "now": datetime.datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M %Z"),
            "$0": sys.argv[0],
            }
        self._make_ts_dates()

    def make(self):
        self.data.extend([latex.T_Head, latex.T_ColorsBW, latex.T_Setup, latex.T_Begin])
        if not self.settings.get("page_numbering", True):
            self.data.append(latex.T_NoPageNumbering)
        for page in self.settings["pages"]:
            if isinstance(page, dict):
                if not page.get("type") and (page.get("?type") or page.get("type?")):
                    pass                     # commented out
                elif page["type"][0] != "?":    # ? in front to comment out
                    if page.get("lab") and not page.get("lab_display"):
                        page["lab_display"] = sLabDisplayName[page["lab"].upper()]
                    getattr(self, "make_" + page["type"])(page)
            elif isinstance(page, str):
                if page[0] != "?":
                    getattr(self, "make_" + page)({"type": page})
            else:
                raise LatexReportError('Unrecognized page description: {!r}'.format(page))
        if self.data[-1].endswith("\\newpage"):
            self.data[-1] = self.data[-1][:-8] + "\\par\\vspace*{\\fill}\\tiny{Report generated: %now%}\n\\newpage"
        self.data.append(latex.T_Tail)
        self.write()

    def compile(self, update_toc=True):
        cmd = self.sLatexCommand.format(run_dir=self.latex_source.parent, latex_source=str(self.latex_source))
        for i in range(2):
            module_logger.info('Executing {}'.format(cmd))
            stdout = self.latex_source.parent.joinpath("latex.log").open("w")
            if subprocess.run(cmd, shell=True, stdout=stdout, stderr=stdout).returncode:
                raise LatexReportError('Compilation failed')

    def view(self):
        cmd = self.sViewCommand.format(output=str(self.latex_source.parent.joinpath(self.latex_source.stem + '.pdf')))
        module_logger.info('Executing {}'.format(cmd))
        if subprocess.run(cmd, shell=True).returncode:
            raise LatexReportError('Viewer failed')

    # ----------------------------------------------------------------------

    def make_cover(self, page):
        self.data.append(latex.T_Cover)
        self.substitute.update({
            "report_hemisphere": self.settings["cover"]["hemisphere"],
            "report_year": self.settings["cover"]["year"],
            "teleconference": self.settings["cover"]["teleconference"],
            "meeting_date": self.settings["cover"]["meeting_date"],
            })

    def make_toc(self, page):
        self.data.append(latex.T_TOC)

    def make_section_begin(self, page):
        self.data.append(latex.T_Section.format(title=page["title"], subtype=page.get("subtype", "")))

    def make_subsection_begin(self, page):
        self.data.append(latex.T_Subsection.format(subtype=page["subtype"], lab=page.get("lab", ""), title=page.get("title", page["subtype"])))

    def make_new_page(self, page=None):
        self.data.append("\\newpage")

    def make_blank_page(self, page=None):
        self.data.append("\\blankpage")

    def make_appendices(self, page=None):
        self.data.append(latex.T_Appendices)

    def make_serum_circle_description(self, page=None):
        self.data.append(latex.T_SerumCirclesDescription)

    # ----------------------------------------------------------------------

    def make_geographic_data_description(self, page):
        if page["coloring"] == "h3_clade":
            self.data.append(latex.T_GeographicDataH3ColoredByCladeDescription)
        elif page["coloring"] == "b_lineage":
            self.data.append(latex.T_GeographicVicYamDataDescription)
        elif page["coloring"] == "b_lineage_vic_deletion_mutants":
            self.data.append(latex.T_GeographicVicDelMutYamDataDescription)
        elif page["coloring"] == "continents":
            self.data.append(latex.T_GeographicDataDescription)
        else:
            raise ValueError("Unrecognized \"coloring\" for \"geographic\" page: " + repr(page["coloring"]))

    def make_geographic_ts(self, page):
        no = 0
        for image in (self.source_dir.joinpath("geo", "{}-geographic-{}.pdf".format(page["subtype"].upper(), d)) for d in self.ts_dates):
            if image.exists():
                if (no % 3) == 0:
                    if no:
                        self.data.append("\\end{GeographicMapsTable}")
                    self.data.append("\\newpage")
                    self.data.append("\\begin{GeographicMapsTable}")
                self.data.append("  \\GeographicMap{{{}}} \\\\".format(image))
                no += 1
        if no:
            self.data.append("\\end{GeographicMapsTable}")

    # ----------------------------------------------------------------------

    def make_antigenic_ts_description(self, page):
        self.data.append(latex.T_AntigenicTsDescription)
        self.data.append(latex.T_AntigenicGridDescription)
        if page["coloring"] == "continents":
            self.data.append(latex.T_AntigenicColoredByRegionDescription)
        else:
            raise ValueError("Unrecognized \"coloring\" for antigenic_ts page: " + repr(page["coloring"]))
        self.data.append(latex.T_AntigenicBigSmallDotsDescription)

    def make_neut_ts_description(self, page):
        self.data.append(latex.T_AntigenicTsDescription)
        self.data.append(latex.T_NeutGridDescription)
        if page["coloring"] == "continents":
            self.data.append(latex.T_AntigenicColoredByRegionDescription)
        else:
            raise ValueError("Unrecognized \"coloring\" for antigenic_ts page: " + repr(page["coloring"]))
        self.data.append(latex.T_AntigenicBigSmallDotsDescription)

    def make_statistics_table(self, page):
        self.data.append(StatisticsTableMaker(
            subtype=page["subtype"],
            lab=page.get("lab", ""),
            source=self.source_dir.joinpath("stat", "stat.json.xz"),
            previous_source=self._previous_stat_source(),
            start=self.start,
            end=self.end,
            period='month'
            ).make())

    def make_antigenic_ts(self, page):
        # {"type": "antigenic_ts", "lab": "CDC", "subtype": "H3", "assay": "HI"}
        image_dir = self.source_dir.joinpath("{}-{}".format(page["subtype"].lower(), page["assay"].lower()))
        images = [image for image in (image_dir.joinpath("ts-{}-{}.pdf".format(page["lab"].lower(), date)) for date in self.ts_dates) if image.exists()]
        for page_no, images_on_page in enumerate(itertools.zip_longest(*([iter(images)] * 6))):
            if page_no:
                self.make_new_page()
            self._antigenic_map_table(images_on_page)

    def make_phylogenetic_description(self, page):
        self.data.append(latex.T_PhylogeneticTreeDescription)

    def make_phylogenetic_tree(self, page):
        image = self.source_dir.joinpath("tree", page["subtype"].lower() + ".tree.pdf")
        if not image.exists() and self.source_dir_2:
            image = self.source_dir_2.joinpath("tree", page["subtype"].lower() + ".tree.pdf")
        module_logger.info("Phylogenetic tree {}".format(image))
        if image.exists():
            self.data.append(latex.T_PhylogeneticTree.format(image=image))

    def make_description(self, page):
        self.data.append(page["text"])

    def make_map(self, page):
        image = self.source_dir.joinpath("{}-{}".format(page["subtype"].lower(), page["assay"].lower()), "{}-{}.pdf".format(page["map_type"], page["lab"].lower()))
        if image and image.exists():
            self.data.append(latex.T_OverviewMap.format(image=image))

    def make_maps(self, page):
        for page_no, images_on_page in enumerate(itertools.zip_longest(*([iter(image and Path(image).resolve() for image in page["images"])] * 6))):
            if page_no:
                self.make_new_page()
            self._antigenic_map_table(images_on_page)

    def make_map_with_title(self, page):
        image = Path(page["image"]).resolve()
        tabcolsep = page.get("tabcolsep", 1.0)
        arraystretch = page.get("arraystretch", 2.5)
        image_scale = page.get("scale", "16 / 60")
        title = page.get("title")
        if image and image.exists():
            self.data.append("\\begin{AntigenicMapTableWithSep}{%fpt}{%f}{%s}" % (tabcolsep, arraystretch, image_scale))
            if title:
                self.data.append("%s \\\\" % title)
            self.data.append("\\AntigenicMap{%s}" % image)
            self.data.append("\\end{AntigenicMapTableWithSep}")

    # ----------------------------------------------------------------------

    def write(self):
        text = self.do_substitute('\n\n'.join(self.data))
        # utility.backup_file(self.latex_source)
        with self.latex_source.open('w') as f:
            f.write(text)

    def do_substitute(self, text):
        text = text.replace('%no-eol%\n', '')
        for option, value in self.substitute.items():
            if isinstance(value, (str, int, float)):
                text = text.replace('%{}%'.format(option), str(value))
        return text

    def _make_ts_dates(self):
        self.ts_dates = []
        d = self.start
        while d < self.end:
            self.ts_dates.append(d.strftime('%Y-%m'))
            if d.month == 12:
                d = datetime.date(year=d.year + 1, month=1, day=1)
            else:
                d = datetime.date(year=d.year, month=d.month+1, day=1)
        module_logger.debug('make_ts_dates {} - {}: {}'.format(self.start, self.end, self.ts_dates))

    # def _ts_date_pairs(self):
    #     for no in range(0, len(self.ts_dates), 2):
    #         if no < (len(self.ts_dates) - 1):
    #             yield self.ts_dates[no], self.ts_dates[no+1]
    #         else:
    #             yield self.ts_dates[no], None

    def _antigenic_map_table(self, images):
        self.data.append("\\begin{AntigenicMapTable}")
        for no in range(0, len(images), 2):
            if images[no] and images[no + 1]:
                self.data.append("\\AntigenicMap{%s} & \\AntigenicMap{%s} \\\\" % (images[no], images[no + 1]))
            elif images[no]:
                self.data.append("\\AntigenicMap{%s} & \\\\" % (images[no], ))
            elif images[no+1]:
                self.data.append("& \\AntigenicMap{%s} \\\\" % (images[no + 1], ))
        self.data.append("\\end{AntigenicMapTable}")

    def _previous_stat_source(self):
        previous_dir = self.settings.get("previous")
        if previous_dir:
            previous_dir = Path(previous_dir).resolve()
            source = previous_dir.joinpath("stat", "stat.json.xz")
            if not source.exists():
                source = previous_dir.joinpath("maps", "stat", "stat.pydata.bz2")
                if not source.exists():
                    raise ValueError("No previous stat data found under " + str(previous_dir))
        else:
            source = None
        return source

# ----------------------------------------------------------------------

class LatexSignaturePageAddendum (LatexReport):

    def __init__(self, source_dir, output_dir, settings):
        super().__init__(source_dir, None, output_dir, "addendum.tex", settings)
        # self.latex_source = output_dir.joinpath("addendum.tex")
        self.substitute.update({
            "documentclass": "\documentclass[a4paper,landscape,12pt]{article}",
            "cover_top_space": "40pt",
            "cover_after_meeting_date_space": "100pt",
            #"usepackage": "\\usepackage[noheadfoot,nomarginpar,margin=0pt,bottom=20pt,paperheight=1400.0pt,paperwidth=900.0pt]{geometry}",
            "usepackage": "\\usepackage[noheadfoot,nomarginpar,margin=0pt,bottom=10pt,paperheight=900.0pt,paperwidth=565.0pt]{geometry}",
            "cover_quotation": "\\quotation",
            })

    def make(self):
        self.data.extend([latex.T_Head, latex.T_Setup, latex.T_Begin])
        self.make_cover()
        self.make_blank_page()
        self.add_pdfs()
        self.data.append(latex.T_Tail)
        self.write()

    def make_cover(self):
        self.data.append(latex.T_Cover)
        self.substitute.update({
            "report_hemisphere": self.settings["cover"]["hemisphere"],
            "report_year": self.settings["cover"]["year"],
            "teleconference": "Addendum",
            "meeting_date": self.settings["cover"]["meeting_date"],
            })

    def add_pdfs(self):
        from .stat import sLabOrder
        self.add_pdf(subtype="h1", assay="hi", lab="all")
        for lab in sLabOrder:
            self.add_pdf(subtype="h3", assay="hi", lab=lab.lower())
            self.add_pdf(subtype="h3", assay="neut", lab=lab.lower())
        for subtype in ["bvic", "byam"]:
            for lab in sLabOrder:
                # if not (subtype == "byam" and lab == "NIMR"):
                self.add_pdf(subtype=subtype, assay="hi", lab=lab.lower())

    def add_pdf(self, subtype, assay, lab):
        filename = self.source_dir.joinpath("{}-{}-{}.pdf".format(subtype, lab, assay))
        if filename.exists():
            self.data.append(latex.T_SignaturePage.format(image=filename))

# ----------------------------------------------------------------------

class LatexSerumCoverageAddendum (LatexReport):

    def __init__(self, source_dir, source_dir_2, output_dir, output_name, settings):
        super().__init__(source_dir, source_dir_2, output_dir, output_name, settings)
        self.substitute.update({
            # "documentclass": "\documentclass[a4paper,landscape,12pt]{article}",
            # "cover_top_space": "40pt",
            # "cover_after_meeting_date_space": "100pt",
            #"usepackage": "\\usepackage[noheadfoot,nomarginpar,margin=0pt,bottom=20pt,paperheight=1400.0pt,paperwidth=900.0pt]{geometry}",
            #"usepackage": "\\usepackage[noheadfoot,nomarginpar,margin=0pt,bottom=10pt,paperheight=900.0pt,paperwidth=565.0pt]{geometry}",
            "usepackage": "\\usepackage[noheadfoot,nomarginpar,margin=1pt,bottom=10pt]{geometry}",
            "cover_quotation": "\\quotation",
            })

    def make_cover(self, *args):
        self.data.append(latex.T_Cover)
        self.substitute.update({
            "report_hemisphere": self.settings["cover"]["hemisphere"],
            "report_year": self.settings["cover"]["year"],
            "teleconference": "Addendum",
            "meeting_date": self.settings["cover"]["meeting_date"],
            })

# ----------------------------------------------------------------------

class StatisticsTableMaker:

    sSubtypeForStatistics = {'h3': 'A(H3N2)', 'h1': 'A(H1N1)', 'bvic': "BVICTORIA", 'byam': "BYAMAGATA"}
    sFluTypePrevious = {'h3': 'H3', 'h1': 'H1PDM', 'bvic': "BVICTORIA", 'byam': "BYAMAGATA"}
    sContinents = ['ASIA', 'AUSTRALIA-OCEANIA', 'NORTH-AMERICA', 'EUROPE', 'RUSSIA', 'AFRICA', 'MIDDLE-EAST', 'SOUTH-AMERICA', 'CENTRAL-AMERICA', 'all', 'sera', 'sera_unique']

    sHeader = {'ASIA': 'Asia', 'AUSTRALIA-OCEANIA': 'Oceania', 'NORTH-AMERICA': 'N Amer', 'EUROPE': 'Europe', 'RUSSIA': 'Russia', 'AFRICA': 'Africa',
               'MIDDLE-EAST': 'M East', 'SOUTH-AMERICA': 'S Amer', 'CENTRAL-AMERICA': 'C Amer', 'all': 'TOTAL', 'month': 'Year-Mo', 'year': 'Year',
               'sera': 'Sera', 'sera_unique': 'Sr Uniq'}

    sReYearMonth = {'month': re.compile(r'^\d{6}$', re.I), 'year': re.compile(r'^\d{4}$', re.I)}

    def __init__(self, subtype, lab, source, previous_source=None, start=None, end=None, period='month'):
        self.subtype = subtype.lower()
        self.lab = lab
        self.data = self._read_data(source)
        self.previous_data = self._read_data(previous_source)
        self.start = start
        self.end = end
        self.period = period

    def _read_data(self, path):
        module_logger.info('reading stat data from {}'.format(path))
        if not path:
            data = None
        elif path.suffixes == [".json", ".xz"]:
            data = read_json(path)
        # elif path.suffixes == [".pydata", ".bz2"]:
        #     data = utility.read_pydata(path)
        else:
            raise ValueError("Cannot read stat data from " + str(path))
        return data

    def make(self):
        module_logger.info('Statistics table for {} {}'.format(self.lab, self.subtype))
        flu_type = self.sSubtypeForStatistics[self.subtype]
        lab = self.lab if self.lab == 'all' else self.lab.upper()
        data_antigens = self.data['antigens'][flu_type][lab]
        data_sera_unique = self.data['sera_unique'].get(flu_type, {}).get(lab, {})
        data_sera = self.data['sera'].get(flu_type, {}).get(lab, {})
        if self.previous_data:
            if flu_type not in self.previous_data['antigens']:
                flu_type_previous = self.sFluTypePrevious[self.subtype]
            else:
                flu_type_previous  = flu_type
            previous_data_antigens = self.previous_data['antigens'][flu_type_previous][lab]
            previous_data_sera_unique = self.previous_data['sera_unique'].get(flu_type_previous, {}).get(lab, {})
            previous_data_sera = self.previous_data['sera'].get(flu_type_previous, {}).get(lab, {})
            previous_sum = collections.defaultdict(int)
        else:
            previous_data_antigens, previous_data_sera_unique, previous_data_sera = {}, {}, {}
        r = [self.make_header()]
        for date in self.make_dates(data_antigens):
            r.append(self.make_line(date, data_antigens=data_antigens.get(date, {}), data_sera=data_sera.get(date, {}), data_sera_unique=data_sera_unique.get(date, {}), previous_data_antigens=previous_data_antigens.get(date, {}), previous_data_sera=previous_data_sera.get(date, {}).get('all', 0), previous_data_sera_unique=previous_data_sera_unique.get(date, {}).get('all', 0)))
            if self.previous_data:
                for continent in self.sContinents[:-2]:
                    previous_sum[continent] += previous_data_antigens.get(date, {}).get(continent, 0)
                previous_sum['sera'] += previous_data_sera.get(date, {}).get('all', 0)
                previous_sum['sera_unique'] += previous_data_sera_unique.get(date, {}).get('all', 0)
        total_line = self.make_line('all', data_antigens=data_antigens.get('all', {}), data_sera=data_sera.get('all', {}), data_sera_unique=data_sera_unique.get('all', {}), previous_data_antigens=previous_sum, previous_data_sera=previous_sum['sera'], previous_data_sera_unique=previous_sum['sera_unique'])
        r.extend([
            self.make_separator(),
            total_line,
            self.make_separator(),
            self.make_footer()
            ])
        return '\n'.join(r)

    def make_header(self):
        r = ''.join(('\\vspace{3em}\\begin{WhoccStatisticsTable}\n  \\hline\n  ',
                     '\\PeriodHeading{{{}}} & {} \\\\\n'.format(self.period.capitalize(), ' & '.join('\\ContinentHeading{{{}}}'.format(n) for n in (self.sHeader[nn] for nn in self.sContinents))),
                     '  \\hline'))
        r = r.replace('{TOTAL}', 'Total{TOTAL}').replace('{Sr Unique}', 'Last{Sr Unique}').replace('{Sr Uniq}', 'Last{Sr Uniq}')
        return r

    def make_line(self, date, data_antigens, data_sera, data_sera_unique, previous_data_antigens, previous_data_sera, previous_data_sera_unique):

        def diff_current_previous(continent):
            diff = data_antigens.get(continent, 0) - previous_data_antigens.get(continent, 0)
            if diff < 0:
                module_logger.error('{} {}: Current: {} Previous: {}'.format(self.format_date(date), continent, data_antigens.get(continent, 0), previous_data_antigens.get(continent, 0)))
                diff = 0
            return diff

        data = [self.format_date(date)]
        if self.previous_data:
            if date == 'all':
                data.extend(['\WhoccStatisticsTableCellTwoTotal{{{}}}{{{}}}'.format(data_antigens.get(continent, 0), diff_current_previous(continent)) for continent in self.sContinents[:-3]])
                data.append( '\WhoccStatisticsTableCellTwoTotal{{{}}}{{{}}}'.format(data_antigens.get('all', 0), diff_current_previous('all')))
                data.append( '\WhoccStatisticsTableCellTwoTotal{{{}}}{{{}}}'.format(data_sera.get('all', 0), data_sera.get('all', 0) - previous_data_sera))
                data.append( '\WhoccStatisticsTableCellTwoTotal{{{}}}{{{}}}'.format(data_sera_unique.get('all', 0), data_sera_unique.get('all', 0) - previous_data_sera_unique))
            else:
                data.extend(['\WhoccStatisticsTableCellTwo{{{}}}{{{}}}'.format(data_antigens.get(continent, 0), diff_current_previous(continent)) for continent in self.sContinents[:-3]])
                data.append( '\WhoccStatisticsTableCellTwoTotal{{{}}}{{{}}}'.format(data_antigens.get(self.sContinents[-3], 0), diff_current_previous(self.sContinents[-3])))
                data.append( '\WhoccStatisticsTableCellTwo{{{}}}{{{}}}'.format(data_sera.get('all', 0), data_sera.get('all', 0) - previous_data_sera))
                data.append( '\WhoccStatisticsTableCellTwo{{{}}}{{{}}}'.format(data_sera_unique.get('all', 0), data_sera_unique.get('all', 0) - previous_data_sera_unique))
        else:
            data.extend(['\WhoccStatisticsTableCellTwo{{{}}}{{{}}}'.format(data_antigens.get(continent, 0)) for continent in self.sContinents[:-2]])
            data.append( '\WhoccStatisticsTableCellTwo{{{}}}{{{}}}'.format(data_sera.get('all', 0)))
            data.append( '\WhoccStatisticsTableCellTwo{{{}}}{{{}}}'.format(data_sera_unique.get('all', 0)))
        return '  ' + ' & '.join(data) + ' \\\\'

    def make_dates(self, data, **sorting):
        rex = self.sReYearMonth[self.period]
        start = None
        end = None
        # if self.period == 'month':
        #     start = self.start and self.start.strftime('%Y%m')
        #     end = self.end and self.end.strftime('%Y%m')
        return sorted((date for date in data if rex.match(date) and (not start or date >= start) and (not end or date < end)), **sorting)

    def make_separator(self):
        return '  \\hline'

    def make_footer(self):
        return '\\end{WhoccStatisticsTable}\n'

    def format_date(self, date):
        if date[0] == '9':
            result = 'Unknown'
        elif date == 'all':
            result = '\\color{WhoccStatisticsTableTotal} TOTAL'
        elif len(date) == 4 or date[4:] == '99':
            if self.period == 'month':
                result = '{}-??'.format(date[:4])
            else:
                result = '{}'.format(date[:4])
        else:
            result = '{}-{}'.format(date[:4], date[4:])
        return result

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
