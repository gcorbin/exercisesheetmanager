\LoadClass{scrartcl}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{exercisesheet}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% PACKAGES
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[ngerman]{babel}
\RequirePackage{amsfonts,amsmath,amssymb,amsthm}
\RequirePackage{graphicx}
\RequirePackage{color}
\RequirePackage{PTSans}
\RequirePackage{textcomp}
\RequirePackage{hyperref}
\RequirePackage{enumerate}
\RequirePackage{algorithm, algpseudocode}
\RequirePackage{lastpage}
\RequirePackage{tikz}
\RequirePackage{scrlayer-scrpage}
\RequirePackage{listings}
\RequirePackage{xifthen}
\RequirePackage{verbatim} % for the macros \comment und \endcomment

\newif\ifenglish
\englishtrue %Default: english

\DeclareOption{english}{\englishtrue}
\DeclareOption{german}{\englishfalse}

\newif\ifsolutions
\solutionsfalse
\DeclareOption{solutions}{\solutionstrue}

\newif\ifannotations
\annotationsfalse
\DeclareOption{annotations}{\annotationstrue}


\ProcessOptions\relax

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Anzeigenamen für Umbegungen
\newcommand{\esm@dispsheet}{\esmsheetnumber}
\newcommand{\esm@dispinclass}{Aufgabe}
\newcommand{\esm@disphomework}{Hausaufgabe}
\newcommand{\esm@dispsolution}{L\"{o}sung}
\newcommand{\esm@dispannotation}{Punktevergabe}
\newcommand{\esm@disphint}{Hinweis}
\newcommand{\esm@disppage}{Seite}
\newcommand{\esm@dispfigure}{Abbildung}
\newcommand{\esm@displisting}{Listing}
\newcommand{\esm@dispduedate}{Abgabe bis}

\ifenglish
\renewcommand{\esm@dispsheet}{Sheet}
\renewcommand{\esm@dispinclass}{Exercise}
\renewcommand{\esm@disphomework}{Homework}
\renewcommand{\esm@dispsolution}{Solution}
\renewcommand{\esm@dispannotation}{Grading}
\renewcommand{\esm@disphint}{Hint}
\renewcommand{\esm@disppage}{Page}
\renewcommand{\esm@dispfigure}{Figure}
\renewcommand{\esm@displisting}{Listing}
\newcommand{\esm@dispduedate}{Due date}
\fi

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DATEN FÜR VERANSTALTUNG
\newcommand{\esm@thelecture}{}
\newcommand{\esm@thesemester}{}
\newcommand{\esm@thelecturer}{}
\newcommand{\esm@thereleasedate}{}
\newcommand{\esm@thedeadline}{}

\newcommand{\lecture}[1]{\renewcommand{\esm@thelecture}{#1}}
\newcommand{\semester}[1]{\renewcommand{\esm@thesemester}{#1}}
\newcommand{\sheetname}[1]{\renewcommand{\esm@dispsheet}{#1}}
\newcommand{\sheetno}[1]{\setcounter{esmsheetnumber}{\numexpr #1 -1}}
\newcommand{\lecturer}[1]{\renewcommand{\esm@thelecturer}{#1}}
\newcommand{\releasedate}[1]{\renewcommand{\esm@thereleasedate}{#1}}
\newcommand{\deadline}[1]{\renewcommand{\esm@thedeadline}{#1}}

\newcommand{\esm@setheaderfooter}{
	\ihead{\esm@thelecture\\ \esm@dispsheet{} \theesmsheetnumber}
	\ifoot{\esm@thelecturer}
	\ohead{\esm@thesemester, \esm@thereleasedate\\ \esm@disppage \pagemark /\pageref{LastPage}}
	\ofoot{
		\begin{tabular}{l}
			\esm@dispduedate{}:\\
			\esm@thedeadline
		\end{tabular}
	}
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% EIGENE COUNTER

% \esmsheetnumbercounter
\newcounter{esmsheetnumber}
% Gleichungscounter
\numberwithin{equation}{esmsheetnumber}
% Aufgabencounter
\newcounter{inclasscounter}[esmsheetnumber]
\renewcommand{\theinclasscounter}{\theesmsheetnumber.\arabic{inclasscounter}}
\newcounter{homeworkcounter}[esmsheetnumber]
\renewcommand{\thehomeworkcounter}{\theesmsheetnumber.\arabic{homeworkcounter}}
\newcounter{solutioncounter}[esmsheetnumber]
\renewcommand{\thesolutioncounter}{\theesmsheetnumber.\arabic{solutioncounter}}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% FARBDEFINITIONEN
\definecolor{tuklblau}{RGB}{0,95,140}
\definecolor{warmgrau}{RGB}{122,114,106}
\definecolor{tuklrot}{RGB}{185,40,25}
\definecolor{kaltgrau}{RGB}{102,128,128}
\definecolor{tuklmathematik}{RGB}{254,192,0}

\definecolor{purpel}{rgb}{0.5,0,0.5}
\definecolor{grun}{rgb}{0.0,0.4,0.0}
\definecolor{lgrau}{rgb}{0.9,0.9,0.9}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% MATHEMATIK- UND UNI-LOGO
\pagestyle{scrheadings}

\chead{%\includegraphics[width=5.1cm]{Logos/Mathematik.png}
	\begin{tikzpicture}
		\draw[draw=none,fill=tuklblau] (0,0) -- ++(0,-1.36) arc (-180:-90:0.1) -- ++(4.9,0) arc (-90:0:0.1) -- ++(0,1.36) ;
		\node[anchor=north] (MATHWRT) at (2.6,-0.43) {
			\textcolor{white}{\textup{\textbf{\LARGE MATHEMATIK}}}
		};
	\end{tikzpicture}%\includegraphics[width=5.1cm]{Logos/TUKL_LOGO_FELD_UNTEN_4C.pdf}
}
\cfoot{\includegraphics[width=5.1cm]{TUKL_LOGO_FELD_UNTEN_4C.pdf}}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% GEOMETRIE setzen
\RequirePackage[hmargin=2cm,
			head=1.6cm,
			%headsep=0.1cm,
			tmargin=2.3cm,
			bmargin=2.7cm]{geometry}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% ALLGEMEINE EINSTELLUNGEN

% Überschriften färben
\addtokomafont{sectioning}{\color{tuklblau!80}}

% Einzug am Beginn neuer Absätze auf 0 setzen
\setlength{\parindent}{0em}

% Schriftart PT Sans
\renewcommand{\familydefault}{\sfdefault}


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEFEHLE FÜR BILDER
% Figurecounter soll esmsheetnumberzahl enthalten
\newcounter{bilder}[esmsheetnumber]
\renewcommand{\thebilder}{\theesmsheetnumber.\arabic{bilder}}

% Ersetzt caption
\newcommand{\bild}[1]{
	\refstepcounter{bilder}
	\caption*{
		\textit{\textcolor{tuklblau!80}{\esm@dispfigure{} \thebilder :} #1}
	}
}
% Referenz auf Bild
\newcommand{\bildref}[1]{
	\textcolor{tuklblau!80}{\esm@dispfigure{} \ref{#1}}
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% CODE HIGHLIGHTING MIT LSTLISTING

% Courier als Standardfont
\def\codefont{\fontfamily{pcr}\selectfont}

% Macht Captions nach links?
\RequirePackage{caption}
\captionsetup[lstlisting]{singlelinecheck=off}

% Globale Eigenschaften für Codefenster
\lstset{
	basicstyle=\codefont,
	showstringspaces=false,
	tabsize=4,
	mathescape=true,escapechar=§,
	upquote=true,
	columns=fixed,
	keywordstyle=\color{blue}\codefont,
	stringstyle=\color{purpel}\codefont,
	commentstyle=\color{grun}\codefont,
	morecomment=[l][\color{grun}]{\#}
}

% Zähler für Listings
\newcounter{mylistings}[esmsheetnumber]
\renewcommand{\themylistings}{
	\theesmsheetnumber.\arabic{mylistings}
}

% Befehl um Listing-Titel zu schreiben [title=\lstcap{...}]
\newcommand{\lstcap}[1]{\refstepcounter{mylistings}\color{tuklblau!80}\itshape \esm@displisting{} \themylistings: #1
}

% Befehl, um auf Listings zu referenzieren
\newcommand{\lstref}[1]{
	\textcolor{tuklblau!80}{\esm@displisting{} \ref{#1}}
}

% Quelltext im Fließtext hervorheben mit:
\newcommand{\codi}[1]{\texttt{#1}}
% Im kursiv gedruckten Kontext:
\newcommand{\codif}[1]{\normalfont\texttt{#1}}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% SHEET
\newenvironment{sheet}[1]{
	\refstepcounter{esmsheetnumber}
	\esm@setheaderfooter
	\section*{\centering \LARGE \esm@dispsheet{} \theesmsheetnumber}
}{\newpage}

%\newcommand{\disclaimerStil}{\color{tuklrot}}
\newenvironment{disclaimer}{%
	\begin{center}%
		\begin{minipage}{0.9\textwidth}%
			\color{red!50!black}
		}{%
		\end{minipage}
	\end{center}
}

\newcommand{\pathToResource}{.}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% TASKS
\newenvironment{inclass}[1]{
	\refstepcounter{inclasscounter}
	\par\hrulefill
	\subsection*{\esm@dispinclass{} \theinclasscounter: \textit{#1 }}
}{}

\newenvironment{homework}[2]{
	\refstepcounter{homeworkcounter}
	\par\hrulefill
	\subsection*{\esm@disphomework{} \thehomeworkcounter: \textit{#1%
		\ifx#2%
		\else%
		(#2)%
		\fi%
	}}
}{}

\newenvironment{solution}{\comment}{\endcomment}
\newenvironment{annotation}{\comment}{\endcomment}

\ifsolutions
	\renewenvironment{solution}{%
		\refstepcounter{solutioncounter}
		\subsection*{\esm@dispsolution{}}
	}{}%
	\ifannotations
		\renewenvironment{annotation}{
			\subsection*{\esm@dispannotation{}}
		}{}%
	\fi
\fi

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% interface to the exercise sheet manager scripts

\newcommand{\inputAufgabe}[2]{%
    \begin{inclass}{#2}
        \renewcommand{\pathToResource}{#1}
        \input{#1/exercise.tex}
    \end{inclass}
}

\newcommand{\inputHausaufgabe}[3]{%
    \begin{homework}{#2}{#3}
        \renewcommand{\pathToResource}{#1}
        \input{#1/exercise.tex}
    \end{homework}
}

\newcommand{\inputLoesung}[1]{%
    \begin{solution}
        \renewcommand{\pathToResource}{#1}
        \input{#1/solution.tex}
    \end{solution}
}

\newcommand{\inputPunkte}[1]{%
    \begin{annotation}
        \input{#1}
    \end{annotation}
}


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% HINWEISBOX
\newcounter{hinweise}[esmsheetnumber]
\renewcommand{\thehinweise}{\theesmsheetnumber.\arabic{hinweise}}
\newcommand{\Hinweis}[1]{
	\refstepcounter{hinweise}
	\begin{center}
		\colorbox{tuklblau!10}{
		\begin{minipage}{0.85\textwidth}
			\begin{center}
			\textcolor{tuklblau}{
				\textbf{\Large \esm@disphint{} \thehinweise}}\\ \textcolor{black}{#1}
			\end{center}
		\end{minipage}}
	\end{center}
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% SONSTIGE BEFEHLE

% Links
\newcommand{\weblink}[2]{
	\href{#1}{\textcolor{tuklblau}{%
			\ifx#2{}%
				#2%
			\else 
				#1%
			\fi}}
}

% Referenz auf einen Aufgabenteil
\newcommand{\teilref}[1]{
	\ref{#1}) %
}

% Texthervorhebung
\newcommand{\hervor}[1]{
	\textcolor{tuklblau!90}{
		\textit{#1}
	}
}
