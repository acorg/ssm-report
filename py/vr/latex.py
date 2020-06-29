T_Head = r"""% !TEX encoding = UTF-8 Unicode
% generated by %program% on %now%
%documentclass%
\pagestyle{empty}
% \usepackage[margin=0,top=0]{geometry}
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
"""

# ----------------------------------------------------------------------

T_Tail = r"""
% ---------------------------------------------------------
\end{document}
"""

# ----------------------------------------------------------------------

T_RemoveSectionNumbering = r"""
% ----------------------------------------------------------------------
% remove section numbering
% ----------------------------------------------------------------------

%% http://www.ehow.com/how_8085363_hide-section-numbers-latex.html
\setcounter{secnumdepth}{-1}

"""

# ----------------------------------------------------------------------

T_ColorCodedBy = r"""
% ----------------------------------------------------------------------
% ColorCodedBy
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
{\color{Victoria}Cyan = Victoria 2-del mutants},
{\color{Victoria}Purple = Victoria 3-del mutants}.
}

\newcommand{\ColorCodedByYear}{%
{\color{YearGrey}Grey - before 2012},
{\color{YearOrange}Orange - 2012},
{\color{YearBlue}Blue - 2013},
{\color{YearMagenta}Magenta - 2014}.
}
"""

# ----------------------------------------------------------------------

T_WhoccStatisticsTable = r"""
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
"""

# ----------------------------------------------------------------------

T_AntigenicMapTable = r"""
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
"""

# ----------------------------------------------------------------------

T_PhylogeneticTree = r"""
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

"""

# ----------------------------------------------------------------------

T_SignaturePage = r"""
% ----------------------------------------------------------------------
% Signature page
% ----------------------------------------------------------------------
\newenvironment{SignaturePageEnv}{
   \noindent
   \begin{center}
}{\end{center}\par}
\newcommand{\SignaturePageFit}[1]{\begin{SignaturePageEnv}\resizebox{!}{0.98\textheight}{\includegraphics[page=1]{#1}}\end{SignaturePageEnv}}
\newcommand{\SignaturePage}[1]{\begin{SignaturePageEnv}\includegraphics[page=1]{#1}\end{SignaturePageEnv}}
"""

# ----------------------------------------------------------------------

T_AntigenicGeneticMapSingle = r"""
% ----------------------------------------------------------------------
% Antigenic-genetic maps
% ----------------------------------------------------------------------
\def \AntigenicGeneticMapSingleMapSize {\textheight*21/30}
\newcommand{\AntigenicGeneticMapSingle}[1]{\begin{center}\includegraphics[width=\AntigenicGeneticMapSingleMapSize,frame]{#1}\end{center}}
"""

# ----------------------------------------------------------------------

T_OverviewMapSingle = r"""
% ----------------------------------------------------------------------
% Overview maps
% ----------------------------------------------------------------------
\def \OverviewMapSingleMapSize {\textheight*21/30}
\newcommand{\OverviewMapSingle}[1]{\begin{center}\includegraphics[width=\OverviewMapSingleMapSize,frame]{#1}\end{center}}
"""

# ----------------------------------------------------------------------

T_GeographicMapsTable = r"""
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
"""

# ----------------------------------------------------------------------

T_BlankPage = r"""
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

T_TableOfContents = r"""
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
"""

# ----------------------------------------------------------------------

T_ = r"""
"""

# ----------------------------------------------------------------------

T_ColorsBW = r"""
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

T_ColorsColors = r"""
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

T_Begin = r"""
% ****************************************************************************************************
% Document
% ----------------------------------------------------------------------

\begin{document}
\rmfamily
"""

# ----------------------------------------------------------------------

T_NoPageNumbering = r" \pagenumbering{gobble} "

# ----------------------------------------------------------------------


# ======================================================================
### Local Variables:
### eval: (if (fboundp 'eu-rename-buffer) (eu-rename-buffer))
### End:
