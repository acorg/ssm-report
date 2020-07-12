import inspect
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

class toc:

    def latex(self):
        return [latex.T_TOC]


# ----------------------------------------------------------------------

class section_title:

    def __init__(self, title):
        self.title = title

    def latex(self):
        return [substitute(latex.T_Section, title=self.title)]


# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
