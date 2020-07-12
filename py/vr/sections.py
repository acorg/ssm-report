import inspect, json, lzma, re, collections, pprint
import logging; module_logger = logging.getLogger(__name__)
from . import latex
from .report import generate, substitute

# ----------------------------------------------------------------------

class cover:

    def __init__(self,
                 cover_top_space="130pt",
                 cover_after_meeting_date_space="180pt",
                 cover_quotation="\\quotation",
                 report_hemisphere="Southern",
                 report_year="2021",
                 teleconference="Teleconference 1",
                 addendum="",
                 meeting_date="11th August 2020"
    ):
        self.args = inspect.getargvalues(inspect.currentframe()).locals

    def latex(self):
        return [
            substitute(latex.T_Cover,
                       **self.args
                       )
            ]

# ----------------------------------------------------------------------

class _single_latex_entry:

    def __init__(self, latex_ref, **args):
        self.latex_ref = latex_ref
        self.args = args

    def latex(self):
        try:
            return [substitute(self.latex_ref, **self.args)]
        except Exception as err:
            module_logger.error(f"args: {self.args}")
            raise
# toc()
class toc (_single_latex_entry):
    def __init__(self): super().__init__(latex.T_TOC)

# new_page()
class new_page (_single_latex_entry):
    def __init__(self): super().__init__(latex.T_NewPage)

# vspace(1)
class vspace (_single_latex_entry):
    def __init__(self, em=1): super().__init__(latex.T_VSpace, em=em)

# text_no_indent("text")
class text_no_indent (_single_latex_entry):
    def __init__(self, text): super().__init__(latex.T_Text_NoIndent, text=text)

# section_title("H1N1pdm09")
class section_title (_single_latex_entry):
    def __init__(self, title): super().__init__(latex.T_Section, title=title)

# subsection_title("H1N1pdm09 geographic data")
class subsection_title (_single_latex_entry):
    def __init__(self, title): super().__init__(latex.T_Subsection, title=title)

# ----------------------------------------------------------------------

# geographic_ts(Path("geo").glob("H1-geographic-*.pdf"))
# geographic_ts(Path("geo").glob("H3-geographic-*.pdf"))
# geographic_ts(Path("geo").glob("B-geographic-*.pdf"))
class geographic_ts:

    def __init__(self, pdfs):
        self.pdfs = sorted(pdfs)

    def latex(self):
        result = []
        no = 0
        for image in self.pdfs:
            if image.exists():
                if (no % 3) == 0:
                    if no:
                        result.append("\\end{GeographicMapsTable}")
                    result.append("\\newpage")
                    result.append("\\begin{GeographicMapsTable}")
                result.append("  \\GeographicMap{{{}}} \\\\".format(image.resolve()))
                no += 1
        if no:
            result.append("\\end{GeographicMapsTable}")
        return result

# ----------------------------------------------------------------------

class statistics_table:

    sLabsForGetStat = {"CDC": ["CDC"], "NIMR": ["Crick", "CRICK", "NIMR"], "CRICK": ["Crick", "CRICK", "NIMR"], "MELB": ["VIDRL", "MELB"], "VIDRL": ["VIDRL", "MELB"]}

    sContinents = ['ASIA', 'AUSTRALIA-OCEANIA', 'NORTH-AMERICA', 'EUROPE', 'RUSSIA', 'AFRICA', 'MIDDLE-EAST', 'SOUTH-AMERICA', 'CENTRAL-AMERICA', 'all', 'sera', 'sera_unique']

    sHeader = {'ASIA': 'Asia', 'AUSTRALIA-OCEANIA': 'Oceania', 'NORTH-AMERICA': 'N Amer', 'EUROPE': 'Europe', 'RUSSIA': 'Russia', 'AFRICA': 'Africa',
               'MIDDLE-EAST': 'M East', 'SOUTH-AMERICA': 'S Amer', 'CENTRAL-AMERICA': 'C Amer', 'all': 'TOTAL', 'month': 'Year-Mo', 'year': 'Year',
               'sera': 'Sera', 'sera_unique': 'Sr Uniq'}

    sReYearMonth = {'month': re.compile(r'^\d{6}$', re.I), 'year': re.compile(r'^\d{4}$', re.I)}

    def __init__(self, **args):
        self.period = "month"
        for k, v in args.items():
            setattr(self, k, v)

    def latex(self):
        data = json.load(lzma.LZMAFile(self.current, "rb"))
        data_antigens = self.get_for_lab(data['antigens'][self.subtype])
        data_sera_unique = self.get_for_lab(data['sera_unique'].get(self.subtype, {}))
        data_sera = self.get_for_lab(data['sera'].get(self.subtype, {}))
        if self.previous:
            previous_data = json.load(lzma.LZMAFile(self.previous, "rb"))
            previous_data_antigens = self.get_for_lab(previous_data['antigens'].get(self.subtype, {}))
            previous_data_sera_unique = self.get_for_lab(previous_data['sera_unique'].get(self.subtype, {}))
            previous_data_sera = self.get_for_lab(previous_data['sera'].get(self.subtype, {}))
            previous_sum = collections.defaultdict(int)
        else:
            previous_sum, previous_data_antigens, previous_data_sera_unique, previous_data_sera = {}, {}, {}, {}

        heading = ' & '.join('\\ContinentHeading{{{}}}'.format(n) for n in (self.sHeader[nn] for nn in self.sContinents))
        heading = heading.replace('{TOTAL}', 'Total{TOTAL}').replace('{Sr Unique}', 'Last{Sr Unique}').replace('{Sr Uniq}', 'Last{Sr Uniq}')
        result = [
            r"\begin{WhoccStatisticsTable}  \hline",
            r"\PeriodHeading{Month} & " + heading + r"\\",
            r"\hline",
        ]
        for date in self.make_dates(data_antigens):
            result.append(self.make_line(date, data_antigens=data_antigens.get(date, {}), data_sera=data_sera.get(date, {}), data_sera_unique=data_sera_unique.get(date, {}), previous_data_antigens=previous_data_antigens.get(date, {}), previous_data_sera=previous_data_sera.get(date, {}).get('all', 0), previous_data_sera_unique=previous_data_sera_unique.get(date, {}).get('all', 0)))
            if previous_data_antigens:
                for continent in self.sContinents[:-2]:
                    previous_sum[continent] += previous_data_antigens.get(date, {}).get(continent, 0)
                previous_sum['sera'] += previous_data_sera.get(date, {}).get('all', 0)
                previous_sum['sera_unique'] += previous_data_sera_unique.get(date, {}).get('all', 0)
        result.extend([
            r"\hline",
            self.make_line('all', data_antigens=data_antigens.get('all', {}), data_sera=data_sera.get('all', {}), data_sera_unique=data_sera_unique.get('all', {}), previous_data_antigens=previous_sum, previous_data_sera=previous_sum.get('sera'), previous_data_sera_unique=previous_sum.get('sera_unique')),
            r"\hline",
            r"\end{WhoccStatisticsTable}",
        ])
        return result

    def get_for_lab(self, source):
        for try_lab in self.sLabsForGetStat.get(self.lab, [self.lab]):
            r = source.get(try_lab)
            if r is not None:
                return r
        return {}

    def make_line(self, date, data_antigens, data_sera, data_sera_unique, previous_data_antigens, previous_data_sera, previous_data_sera_unique):

        def diff_current_previous(continent):
            diff = data_antigens.get(continent, 0) - previous_data_antigens.get(continent, 0)
            if diff < 0:
                module_logger.error('{} {}: Current: {} Previous: {}'.format(self.format_date(date), continent, data_antigens.get(continent, 0), previous_data_antigens.get(continent, 0)))
                diff = 0
            return diff

        data = [self.format_date(date)]
        if previous_data_antigens:
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
            data.extend(['\WhoccStatisticsTableCellOne{{{}}}'.format(data_antigens.get(continent, 0)) for continent in self.sContinents[:-2]])
            data.append( '\WhoccStatisticsTableCellOne{{{}}}'.format(data_sera.get('all', 0)))
            data.append( '\WhoccStatisticsTableCellOne{{{}}}'.format(data_sera_unique.get('all', 0)))
        return '  ' + ' & '.join(data) + ' \\\\'

    def make_dates(self, data, **sorting):
        rex = self.sReYearMonth[self.period]
        start = None
        end = None
        # if self.period == 'month':
        #     start = self.start and self.start.strftime('%Y%m')
        #     end = self.end and self.end.strftime('%Y%m')
        return sorted((date for date in data if rex.match(date) and (not start or date >= start) and (not end or date < end)), **sorting)

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
