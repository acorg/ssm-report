import logging; module_logger = logging.getLogger(__name__)

# ======================================================================

T_Head = r"""%no-eol%
% !TEX encoding = UTF-8 Unicode
% generated by %$0% on %now%
%documentclass%
\pagestyle{empty}
%\usepackage[margin=2.0cm,top=2.0cm]{geometry}
\usepackage[cm]{fullpage}
\usepackage{verbatim}
\usepackage[table]{xcolor}

\usepackage{graphicx}           % multiple pdfs per page
\usepackage[export]{adjustbox}  % frame in \includegraphics
\usepackage{grffile}            % to allow .a.pdf in \includegraphics
\usepackage{pdfpages}           % phylogenetic tree
\usepackage{fancyhdr}           % keep page numbers in embedded phylogenetic tree
\usepackage{calc}
\usepackage{hyperref}           % ToC entries as links
\usepackage{tocloft}            % \cftsetindents
\usepackage[toc,page]{appendix} % Appendice
\usepackage{titletoc}           % ToC entries without numbers
\usepackage[T1]{fontenc}        % fonts
\usepackage{times}              % font
%usepackage%
"""

# ----------------------------------------------------------------------

T_Setup = r"""%no-eol%
% ----------------------------------------------------------------------
% remove section numbering
% ----------------------------------------------------------------------

%% http://www.ehow.com/how_8085363_hide-section-numbers-latex.html
\setcounter{secnumdepth}{-1}

% ----------------------------------------------------------------------
% ToC table of contents
% ----------------------------------------------------------------------

%% ToC http://tex.stackexchange.com/questions/163986/format-table-of-contents-with-latex
\titlecontents{section}[0cm]{\bfseries}{\\}{\\}{}
\titlecontents{subsection}[1em]{}{}{}{\titlerule*[5pc]{}\vspace{0.8ex}\thecontentspage}
\contentsmargin{120pt}

% table of content indentation
% http://tex.stackexchange.com/questions/50471/question-about-indent-lengths-in-toc
\cftsetindents{section}{0.5in}{0.5in}

%% http://tex.stackexchange.com/questions/80113/hide-section-numbers-but-keep-numbering
% \renewcommand{\thesection}{}
% \makeatletter
% \def\@seccntformat#1{\csname #1ignore\expandafter\endcsname\csname the#1\endcsname\quad}
% \let\sectionignore\@gobbletwo
% \let\latex@numberline\numberline
% \def\numberline#1{\if\relax#1\relax\else\latex@numberline{#1}\fi}
% \makeatother
% \renewcommand{\thesubsection}{\arabic{subsection}}

% ----------------------------------------------------------------------
%
% ----------------------------------------------------------------------
\newcommand{\ColorCodedByRegion}{%
{\color{NorthAmerica}DarkBlue = NorthAmerica},
{\color{SouthAmerica}LightBlue = SouthAmerica},
{\color{Europe}Green = Europe},
{\color{Africa}Orange = Africa},
{\color{MiddleEast}Purple = MiddleEast},
{\color{Russia}Maroon = Russia},
{\color{Asia}Red = E SE Asia},
{\color{AustraliaOceania}Pink = Oceania},
{\color{Unknown}Grey = unknown}.
}

\newcommand{\ColorCodedByLineage}{%
{\color{Yamagata}Red = Yamagata},
{\color{Victoria}Blue = Victoria}.
{\color{Victoria}Green = Victoria deletion mutants}.
}

\newcommand{\ColorCodedByLineageVicDelMut}{%
{\color{Yamagata}Red = Yamagata},
{\color{Victoria}Blue = Victoria},
{\color{Victoria}Cyan = Victoria deletion mutants}.
}

\newcommand{\ColorCodedByYear}{%
{\color{YearGrey}Grey - before 2012},
{\color{YearOrange}Orange - 2012},
{\color{YearBlue}Blue - 2013},
{\color{YearMagenta}Magenta - 2014}.
}

% ----------------------------------------------------------------------
% Table with antigenic maps
% ----------------------------------------------------------------------
\def \AntigenicMapTableMapSize {(\textheight-20pt) * 9 / 30} % size of an embedded antigenic map
\def \AntigenicMapTableMapSmallSize {(\textheight-20pt) * 17 / 60} % size of an embedded antigenic map

\newenvironment{AntigenicMapTable}{
  \setlength{\tabcolsep}{7pt}
  \renewcommand{\arraystretch}{3.5}
  \newcommand{\AntigenicMap}[1]{\includegraphics[width=\AntigenicMapTableMapSize,frame]{##1}}
  \newcommand{\AntigenicMapSmall}[1]{\includegraphics[width=\AntigenicMapTableMapSmallSize,frame]{##1}}
  \begin{center}
    \begin{tabular}{c c}
}{\end{tabular}\end{center}\par}

\newenvironment{AntigenicMapTableWithSep}[3]{
  \setlength{\tabcolsep}{#1}
  \renewcommand{\arraystretch}{#2}
  \newcommand{\AntigenicMap}[1]{\includegraphics[width={(\textheight-20pt) * {#3}},frame]{##1}}
  \begin{center}
    \begin{tabular}{c c}
}{\end{tabular}\end{center}\par}

% ----------------------------------------------------------------------
% Table with statistics
% ----------------------------------------------------------------------
\newcommand{\WhoccStatisticsTableCellOne}[1]{#1 & & & &}
\newcommand{\WhoccStatisticsTableCellTwo}[2]{#1 & ( & #2 & ) &}
% \newcommand{\WhoccStatisticsTableCellTwoTotal}[2]{\textbf{#1} & \textbf{(} & \textbf{#2} & \textbf{)} & }
\newcommand{\WhoccStatisticsTableCellTwoTotal}[2]{\color{WhoccStatisticsTableTotal}#1 & \color{WhoccStatisticsTableTotal}( & \color{WhoccStatisticsTableTotal}#2 & \color{WhoccStatisticsTableTotal}) & }

\newenvironment{WhoccStatisticsTable}{
  \setlength{\tabcolsep}{0pt}
  \definecolor{AlternativeRow}{HTML}{F0F0F0}
  \rowcolors{2}{AlternativeRow}{}
  \renewcommand{\arraystretch}{1.5}
  \newcommand{\ContinentHeading}[1]{\multicolumn{5}{>{\hspace{0.3em}}c<{\hspace{0.3em}}}{##1}}
  \newcommand{\ContinentHeadingTotal}[1]{\multicolumn{5}{>{\hspace{0.3em}}c<{\hspace{0.3em}}}{\color{WhoccStatisticsTableTotal}##1}}
  \newcommand{\ContinentHeadingLast}[1]{\multicolumn{5}{>{\hspace{0.3em}}c<{\hspace{0.3em}}|}{##1}}
  \newcommand{\PeriodHeading}[1]{\multicolumn{1}{|c}{##1}}
  \scriptsize
  \begin{center}
    \begin{tabular}{|>{\hspace{0.3em}}l<{\hspace{0.3em}} *{12}{>{\hspace{0.6em}}r >{\hspace{0.3em}}lrl r<{\hspace{0.5em}}}|} % >{\hspace{0.3em}\bfseries}r >{\hspace{0.3em}}lrl r<{\hspace{0.3em}} *{2}{>{\hspace{0.3em}}r >{\hspace{0.3em}}lrl r<{\hspace{0.3em}}}}
}{\end{tabular}\end{center}\par}

% ----------------------------------------------------------------------
% Phylogenetic tree
% ----------------------------------------------------------------------
\newenvironment{PhylogeneticTreeEnv}{
   \noindent
   \begin{center}
}{\end{center}\par}
\newcommand{\PhylogeneticTree}[1]{\begin{PhylogeneticTreeEnv}\pagestyle{empty} \includepdf[pages=-,pagecommand={\thispagestyle{fancy}}]{#1}\end{PhylogeneticTreeEnv}}
\newcommand{\PhylogeneticTreeFit}[1]{\begin{PhylogeneticTreeEnv}\includegraphics[page=1,scale=0.9]{#1}\end{PhylogeneticTreeEnv}}
\newcommand{\PhylogeneticTreeTwoToc}[3]{
  \begin{PhylogeneticTreeEnv}
    \includepdf[pages=-,pagecommand={\pagestyle{fancy}}]{#1}
    \addcontentsline{toc}{subsection}{#2}
    \includepdf[pages=-,pagecommand={\pagestyle{fancy}}]{#3}
  \end{PhylogeneticTreeEnv}}

% ----------------------------------------------------------------------
% Signature page
% ----------------------------------------------------------------------
\newenvironment{SignaturePageEnv}{
   \noindent
   \begin{center}
}{\end{center}\par}
\newcommand{\SignaturePageFit}[1]{\begin{SignaturePageEnv}\resizebox{!}{0.98\textheight}{\includegraphics[page=1]{#1}}\end{SignaturePageEnv}}
\newcommand{\SignaturePage}[1]{\begin{SignaturePageEnv}\includegraphics[page=1]{#1}\end{SignaturePageEnv}}

% ----------------------------------------------------------------------
% Antigenic-genetic maps
% ----------------------------------------------------------------------
\def \AntigenicGeneticMapSingleMapSize {\textheight*21/30}
\newcommand{\AntigenicGeneticMapSingle}[1]{\begin{center}\includegraphics[width=\AntigenicGeneticMapSingleMapSize,frame]{#1}\end{center}}

% ----------------------------------------------------------------------
% Overview maps
% ----------------------------------------------------------------------
\def \OverviewMapSingleMapSize {\textheight*21/30}
\newcommand{\OverviewMapSingle}[1]{\begin{center}\includegraphics[width=\OverviewMapSingleMapSize,frame]{#1}\end{center}}

% ----------------------------------------------------------------------
% Table with geographic maps
% ----------------------------------------------------------------------
\def \GeographicMapsTableMapSize {\textheight * 18 / 30} % size of an embedded geographic map
\newenvironment{GeographicMapsTable}{
  \renewcommand{\arraystretch}{2.5}
  \newcommand{\GeographicMap}[1]{\includegraphics[width=\GeographicMapsTableMapSize,frame]{##1}}
  \begin{center}
    \begin{tabular}{c}
}{\end{tabular}\end{center}\par}

% ----------------------------------------------------------------------
% Blank page (http://tex.stackexchange.com/questions/36880/insert-a-blank-page-after-current-page)
% ----------------------------------------------------------------------
\newcommand\blankpage{%
  \newpage
  \vspace*{100pt}
  \thispagestyle{empty}%
  \newpage}
"""

# ----------------------------------------------------------------------

T_ColorsBW = r"""%no-eol%
% ----------------------------------------------------------------------
% Continent colors for time series
% ----------------------------------------------------------------------
\definecolor{NorthAmerica}{HTML}{000000}
\definecolor{Europe}{HTML}{000000}
\definecolor{MiddleEast}{HTML}{000000}
\definecolor{NorthAmerica}{HTML}{000000}
\definecolor{SouthAmerica}{HTML}{000000}
\definecolor{CentralAmerica}{HTML}{000000}
\definecolor{Africa}{HTML}{000000}
\definecolor{Asia}{HTML}{000000}
\definecolor{Russia}{HTML}{000000}
\definecolor{AustraliaOceania}{HTML}{000000}
\definecolor{Antarctica}{HTML}{000000}
\definecolor{ChinaSouth}{HTML}{000000}
\definecolor{ChinaNorth}{HTML}{000000}
\definecolor{ChinaUnknown}{HTML}{000000}
\definecolor{Unknown}{HTML}{000000}

% ----------------------------------------------------------------------
% Point colors
% ----------------------------------------------------------------------
\definecolor{Vaccine}{HTML}{000000}
\definecolor{PreviousVaccine}{HTML}{000000}
\definecolor{Serology}{HTML}{000000}

\definecolor{YearGrey}{HTML}{000000}
\definecolor{YearOrange}{HTML}{000000}
\definecolor{YearMagenta}{HTML}{000000}
\definecolor{YearBlue}{HTML}{000000}

\definecolor{Yamagata}{HTML}{000000}
\definecolor{Victoria}{HTML}{000000}

% ----------------------------------------------------------------------
% Other colors
% ----------------------------------------------------------------------
\definecolor{WhoccStatisticsTableTotal}{HTML}{008000}
"""

# ----------------------------------------------------------------------

T_ColorsColors = r"""%no-eol%
% ----------------------------------------------------------------------
% Continent colors for time series
% ----------------------------------------------------------------------
\definecolor{NorthAmerica}{HTML}{000080}
\definecolor{Europe}{HTML}{00FF00}
\definecolor{MiddleEast}{HTML}{8000FF}
\definecolor{NorthAmerica}{HTML}{00008B}
\definecolor{SouthAmerica}{HTML}{40E0D0}
\definecolor{CentralAmerica}{HTML}{AAF9FF}
\definecolor{Africa}{HTML}{FF8000}
\definecolor{Asia}{HTML}{FF0000}
\definecolor{Russia}{HTML}{B03060}
\definecolor{AustraliaOceania}{HTML}{FF69B4}
\definecolor{Antarctica}{HTML}{808080}
\definecolor{ChinaSouth}{HTML}{FF0000}
\definecolor{ChinaNorth}{HTML}{6495ED}
\definecolor{ChinaUnknown}{HTML}{808080}
\definecolor{Unknown}{HTML}{808080}

% ----------------------------------------------------------------------
% Point colors
% ----------------------------------------------------------------------
\definecolor{Vaccine}{HTML}{FF0000}
\definecolor{PreviousVaccine}{HTML}{0000FF}
\definecolor{Serology}{HTML}{FFA500}

\definecolor{YearGrey}{HTML}{B0B0B0}
\definecolor{YearOrange}{HTML}{FFA500}
\definecolor{YearMagenta}{HTML}{FF00FF}
\definecolor{YearBlue}{HTML}{0000FF}

\definecolor{Yamagata}{HTML}{FF0000}
\definecolor{Victoria}{HTML}{0000FF}

% ----------------------------------------------------------------------
% Other colors
% ----------------------------------------------------------------------
\definecolor{WhoccStatisticsTableTotal}{HTML}{008000}
"""

# ----------------------------------------------------------------------

T_Begin = r"""%no-eol%
% ****************************************************************************************************
% Document
% ----------------------------------------------------------------------

\begin{document}
\rmfamily
"""

# ----------------------------------------------------------------------

T_NoPageNumbering = r" \pagenumbering{gobble} "

# ----------------------------------------------------------------------

T_Cover = r"""%no-eol%
% ----------------------------------------------------------------------
% Cover
% ----------------------------------------------------------------------

\thispagestyle{empty}

{%cover_quotation%
\vspace*{%cover_top_space%}
{
\fontsize{22}{26} \selectfont
\noindent
\textbf{Information for the WHO Consultation\\ on the Composition of Influenza Vaccines\\ for the %report_hemisphere% Hemisphere %report_year%}
\par
}

\vspace{90pt}
{
\fontsize{19}{24} \selectfont
\noindent
%teleconference%

\vspace{10pt}
\noindent
%addendum%

\vspace{50pt}
\noindent
%meeting_date%
\par
}

\vspace{%cover_after_meeting_date_space%}
{
\large
\noindent
Center for Pathogen Evolution

% \vspace{10pt}
% \noindent
% WHO Collaborating Center for Modeling, Evolution, and Control of Emerging Infectious Diseases

\vspace{10pt}
\noindent
University of Cambridge, United Kingdom
% do not remove two empty lines below


% do not remove two empty lines above!
}
}
"""

# ----------------------------------------------------------------------

T_TOC = r"""%no-eol%
% ----------------------------------------------------------------------
% ToC
% ----------------------------------------------------------------------

\newpage
\tableofcontents
"""

# ----------------------------------------------------------------------

T_Section = r"""%no-eol%
% ----------------------------------------------------------------------
% {subtype}
% ----------------------------------------------------------------------
\newpage
\section{{{title}}}
"""

# ----------------------------------------------------------------------

T_Subsection = r"""%no-eol%
% ----------------------------------------------------------------------
% {subtype} {lab}
% ----------------------------------------------------------------------
\subsection{{{title}}}
"""

# ----------------------------------------------------------------------

T_AntigenicTimeSeriesFrontPage = r"""%no-eol%
\vspace{3em}
\noindent
Month-by-month time series from %time_series_start% to %time_series_end%

\vspace{1em}
\noindent
Grid indicates 1 unit of antigenic distance, a 2-fold dilution in HI titer.

\vspace{1em}
\noindent
Reference antigens and antisera no fill. Epi strains (small dots)
colored by region: \ColorCodedByRegion

\vspace{1em}
\noindent
Small antigen dots indicate strains also in previous report, larger
antigen dots indicate strains added since previous report.

\vspace{1em}
\noindent
The large red dot marks the current {\color{Vaccine}vaccine strain},
large blue dot marks {\color{PreviousVaccine}previous vaccine strain},
large orange dots mark {\color{Serology}candidate serology antigens}.

\vspace{1em}
\noindent
Circles represent 4 fold titer reductions from homologous titer for
antisera. Blue circle, {\color{PreviousVaccine}previous vaccine strain
antiserum}; red circle, {\color{Vaccine}current vaccine strain
antiserum}.
"""

# ----------------------------------------------------------------------

T_AntigenicTsDescription = r"""%no-eol%
\vspace{3em}
\noindent
Month-by-month time series from %time_series_start% to %time_series_end%.
"""

# ----------------------------------------------------------------------

T_AntigenicGridDescription = r"""%no-eol%
\vspace{1em}
\noindent
Grid indicates 1 unit of antigenic distance, a 2-fold dilution in HI titer.
"""

T_NeutGridDescription = r"""%no-eol%
\vspace{1em}
\noindent
Grid indicates 1 unit of antigenic distance.
"""

# ----------------------------------------------------------------------

T_AntigenicBigSmallDotsDescription = r"""%no-eol%
\vspace{1em}
\noindent
Small antigen dots indicate strains also in previous report, larger
antigen dots indicate strains added since previous report.
"""

# ----------------------------------------------------------------------

T_AntigenicColoredByRegionDescription = r"""%no-eol%
\vspace{1em}
\noindent
Reference antigens and antisera no fill. Epi strains (small dots)
colored by region: \ColorCodedByRegion
"""

# ----------------------------------------------------------------------

T_AntigenicVaccineSerologyDescription = r"""%no-eol%
\vspace{1em}
\noindent
The large red dot marks the current {\color{Vaccine}vaccine strain},
large blue dot marks {\color{PreviousVaccine}previous vaccine strain},
large orange dots mark {\color{Serology}candidate serology antigens}.
"""

# ----------------------------------------------------------------------

T_AntigenicSerumCircleDescription = r"""%no-eol%
\vspace{1em}
\noindent
Circles represent 4 fold titer reductions from homologous titer for
antisera. Blue circle, {\color{PreviousVaccine}previous vaccine strain
antiserum}; red circle, {\color{Vaccine}current vaccine strain
antiserum}.
"""

# ----------------------------------------------------------------------

T_AntigenicOverviewDescription = r"""%no-eol%
%\vspace{1em}
%\noindent
"""

# ----------------------------------------------------------------------

T_PhylogeneticTreeDescription = r"""%no-eol%
\vspace{3em}
\noindent
The phylogenetic tree is color coded by region: \ColorCodedByRegion
The month in which recent strains in the tree were isolated is indicated
by horizontal bars to the right of the tree drawn at the same vertical
position as the position of the strain in the tree. The horizontal bars
are also colored by region. This tree is zoomable, and when zoomed the
strain names and dates on which they were isolated can be read.

\vspace{1em}
\noindent
Nucleotide sequences of the HA1 domain of the HA were aligned. MODELTEST was run
on the aligned sequences and GTR+I+gamma4 was determined to be the most
appropriate evolutionary model for phylogenetic tree construction. Initial
tree construction was performed using RAxML v8.2.8 under the GTRGAMMAI
model. Global optimization of branch topology was then performed on the tree
with the best likelihood score from RAxML using GARLI v2.1 under the model
parameters determined by MODELTEST. Garli was run for 1,000,000 generations.
"""

T_PhylogeneticTreeDescription_H3_142 = r"""%no-eol%
\vspace{3em}
\noindent
The phylogenetic tree is color coded by amino-acid at position 142:
DarkGreen = G, Orange = K, Turquoise = N, Purple = R, Pink = E, DarkGrey = X.
The month in which recent strains in the tree were isolated is indicated
by horizontal bars to the right of the tree drawn at the same vertical
position as the position of the strain in the tree. The horizontal bars
are also colored by amino-acid at position 142. This tree is zoomable, and when zoomed the
strain names and dates on which they were isolated can be read.

\vspace{1em}
\noindent
Nucleotide sequences of the HA1 domain of the HA were aligned. MODELTEST was run
on the aligned sequences and GTR+I+gamma4 was determined to be the most
appropriate evolutionary model for phylogenetic tree construction. Initial
tree construction was performed using RAxML v8.2.8 under the GTRGAMMAI
model. Global optimization of branch topology was then performed on the tree
with the best likelihood score from RAxML using GARLI v2.1 under the model
parameters determined by MODELTEST. Garli was run for 1,000,000 generations.
"""

T_PhylogeneticTreeDescription_BVicDeletion = r"""%no-eol%
\vspace{1em}
\noindent
Light grey short horizontal lines at the bottom part of the tree between tree
and time series mark deletion mutants, i.e. strains having deletion at
positions 162 and 163. Dark grey short horizontal lines above them mark triple
deletion mutants, i.e. the strains having deletions at positions 163, 164, 165.
"""

# ----------------------------------------------------------------------

T_PhylogeneticTree = r"\PhylogeneticTreeFit{{{image}}}"

# ----------------------------------------------------------------------

T_SignaturePage = r"\SignaturePageFit{{{image}}}"

# ----------------------------------------------------------------------

T_OverviewMap = r"\OverviewMapSingle{{{image}}}"

# ----------------------------------------------------------------------

T_GeographicDataDescription = r"""%no-eol%
\vspace{3em}
\noindent
Month-by-month geographic time series from %time_series_start% to %time_series_end%.

\vspace{1em}
\noindent
Strains colored by region: \ColorCodedByRegion

\vspace{1em}
\noindent
Each dot indicates the isolation location for a strain that has been measured in
an HI table. Thus these figures can be interpreted as a virologically-confirmed
epidemiological spatial timeseries (modulo the usual caveats about surveillance
biases).
"""

# ----------------------------------------------------------------------

T_GeographicDataH3ColoredByCladeDescription = r"""%no-eol%
\vspace{3em}
\noindent
Month-by-month geographic time series from %time_series_start% to %time_series_end%.

\vspace{1em}
\noindent
Strains colored by clade: 3C2/3C3=Blue, 3C2a=Red, 3C2a1=DarkRed, 3C3a=Green, 3C3b=DarkBlue, unsequenced=Grey

\vspace{1em}
\noindent
Each dot indicates the isolation location for a strain that has been measured in
an HI table. Thus these figures can be interpreted as a virologically-confirmed
epidemiological spatial timeseries (modulo the usual caveats about surveillance
biases).
"""

# ----------------------------------------------------------------------

T_GeographicVicYamDataDescription = r"""%no-eol%
\vspace{3em}
\noindent
Month-by-month geographic time series from %time_series_start% to %time_series_end%.

\vspace{1em}
\noindent
Strains colored by lineage: \ColorCodedByLineage

\vspace{1em}
\noindent
Each dot indicates the isolation location for a strain that has been measured in
an HI table. Thus these figures can be interpreted as a virologically-confirmed
epidemiological spatial timeseries (modulo the usual caveats about surveillance
biases).
"""

# ----------------------------------------------------------------------

T_GeographicVicDelMutYamDataDescription = r"""%no-eol%
\vspace{3em}
\noindent
Month-by-month geographic time series from %time_series_start% to %time_series_end%.

\vspace{1em}
\noindent
Strains colored by lineage: \ColorCodedByLineageVicDelMut

\vspace{1em}
\noindent
Each dot indicates the isolation location for a strain that has been measured in
an HI table. Thus these figures can be interpreted as a virologically-confirmed
epidemiological spatial timeseries (modulo the usual caveats about surveillance
biases).
"""

# ----------------------------------------------------------------------

T_Appendices = r"""%no-eol%
\newpage % appendix
\appendix
\appendixpage
"""

# ----------------------------------------------------------------------

T_SerumCirclesDescription = r"""%no-eol%
\subsection{Marking low-reactors: serum sector/circle description}

\small
\noindent
(This is the same description as in the last report.)

\vspace{1em}
\noindent
Strains outside a serum circle are $>$4-fold low-reactors to the homologous
titer for the serum.

\vspace{1em}
\noindent
Here we describe why serum circles have different radii. One might expect the
serum circle delimiting $>$4-fold low-reactors to have radius 2. However, this
would only be the case when the homologous titer is the same as the maximum
titer for a serum - and this is not always the case.

\vspace{1em}
\noindent
The theoretical (or "target") distance in an antigenic map from serum S to a
antigen A is $\log_2$ (max titer for serum S against any antigen) - $\log_2$
(titer for serum S against antigen A). In other words, the number of 2-folds
between the maximum titer for serum S, and the titer of serum S to antigen A.

\vspace{1em}
\noindent
Thus the theoretical distance between a serum and antigen is dependent on both
the maximum titer observed for the serum and its homologous titer.

\vspace{1em}
\noindent
If low reactors were defined as $>$4-fold from the max titer for a serum then
the theoretical radius for all serum circles would be 2 units, and this text
would not be necessary. But low reactors are defined as $>$4-fold from the
homologous titer, hence the radius is 2 units plus the number of 2-folds
between max titer and the homologous titer for a serum. Saying the same thing
mathematically the theoretical radius for a serum circle is 2 + $\log_2$ (max
titer for serum S against any antigen A) - $\log_2$ (homologous titer for
serum S).

\vspace{1em}
\noindent
In addition to the theoretical serum circle radius, we also calculate an
empirical radius. The difference is that the theoretical radius is calculated
from the target distance between sera and antigens as specified by the HI
titers, whereas the empirical radius is determined from the antigenic map and
thus the actual distances in the antigenic map between the sera and antigens.
There are some extra details about the empirical calculation but they are not
central, and are omitted here.

\vspace{1em}
\noindent
Both the theoretical and empirical results are shown at the bottom of any
timeseries webpage. The theoretical and empirical radii are similar to each
other, and are on average only about 0.25 antigenic units different. The
empirical radius is the one shown on the antigenic maps.

\vspace{1em}
\noindent
The center of a serum circle for serum S is at the serum point in the map
for serum S.
"""

# ----------------------------------------------------------------------

T_Tail = r"""%no-eol%
% ---------------------------------------------------------
\end{document}
"""

# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
