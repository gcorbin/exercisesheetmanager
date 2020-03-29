% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% LATEX-Klasse für Übungsblätter, Design für den Fachbereich Mathematik
%	Autor:	Andreas Roth
%			KOMMS, FB Mathematik
%			TU Kaiserslautern
%			roth@mathematik.uni-kl.de
%			Tel.: 0631 205 4496
%			Raum 48-557
%
%   Maintainer: Gregor Corbin, 
%               AGTM, FB Mathematik
%               TU Kaiserslautern
%               corbin@mathematik.uni-kl.de
%               
%               Matthias Andres, 
%               AGTM, FB Mathematik
%               TUK,
%               mandres@mathematik.uni-kl.de
% 
%	Die Nutzung ist jedem zur Verwendung in beliebigen Veranstaltungen des
%	Fachbereichs gestattet. Die Gestaltung ist an das Corporate Design der
%	Uni Kaiserslautern angelehnt.
% BENUTZUNG
% Diese Klasse erbt von exercisesheet.cls
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% WEITERE BEFEHLE:
%
%	- \Hinweis{Text}:
%		Eine mit Blattnummer nummerierte, blaue Hinweisbox
%
%	- \hervor{Text}:
%		Kursiv und farbig hervorgehobener Text
%
%	- \codi{Text}:
%		Quelltext im Fließtext
%
%	- \codif{Text}:
%		Quelltext im kursiven Fließtext
%
%	- \bild{Text}
%		Ersetzt \caption{} in Figures
%
%	- \bildref{label}
%		Referenziere im Text auf eine Abbildung mit label label
%
%	- \lstref{label}
%		Referenziere im Text auf Listing mit label label
%
%	- \weblink{url}{beschreibung}
%		Farbiger Hyperlink mit Text beschreibung auf Seite url
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% EINBINDEN VON QUELLTEXT
%
% 	Weil das vorliegende Stylefile für Einführung in wiss. Programmieren
% 	gemacht wurde, kann man recht einfach Quelltext einbinden. Dazu benutzt
%	man die Umgebung lstlisting aus dem Paket listings. Einige Einstellungen
%	sind schon gesetzt, man muss vor der Benutzung allerdings noch die
%	gewünschte Sprache einstellen mit
%
%		\lstset{language=Matlab} oder
%		\lstset{language=C} oder ...
%
%	Quelltext einbinden:
%		\begin{lstlisting}[title=\lstcap{<Titeltext>\label{<listlabel>}}]
%		... Quelltext ...
%		\end{lstlisting}
%
%	Titel ist optional. Auf Labels kann mit \lstfref{} referenziert werden!
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %


\LoadClassWithOptions{exercisesheet}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fbmatheblatt}[2020/03/26 Uebungsblatt FB Mathematik]

\ProcessOptions\relax


\usepackage[]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[]{amsmath}
\usepackage[]{amsfonts}
\usepackage[]{amssymb}
\usepackage[]{amsthm}
\usepackage{bm}
\usepackage[]{eurosym}
\usepackage[]{graphicx}
\usepackage[]{subfig}
\usepackage[]{caption}
\usepackage[]{alltt}
\usepackage[]{colortbl}
\usepackage[]{stmaryrd}
\usepackage[]{enumerate}
\usepackage[]{tikz}
\usepackage[]{pgfplots}
\usepackage{nicefrac}
\usepackage{empheq}
\usepackage{makecell}
\usepackage{listings} % code embedding
\usepackage{enumerate} % change style of enumerate

% bibliography stuff
\usepackage{natbib}
\usepackage{bibentry}
\bibliographystyle{plain}
\nobibliography*


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DISPLAY names
\newcommand{\esm@disphint}{Hinweis}
\newcommand{\esm@dispfigure}{Abbildung}
\newcommand{\esm@displisting}{Listing}

\ifenglish
\renewcommand{\esm@disphint}{Hint}
\renewcommand{\esm@dispfigure}{Figure}
\renewcommand{\esm@displisting}{Listing}
\fi

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

% enumerate convention a), b)
\renewcommand{\theenumi}{\alph{enumi}}
\renewcommand{\labelenumi}{\theenumi)}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DISCLAIMER
\renewenvironment{disclaimer}{%
	\begin{center}%
		\begin{minipage}{0.9\textwidth}%
			\color{tuklrot}
		}{%
	\end{minipage}
\end{center}
}


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEFEHLE FÜR BILDER
\newcounter{esmfigurecounter}
% Ersetzt caption
\newcommand{\bild}[1]{
	\refstepcounter{esmfigurecounter}
	\caption*{
		\textit{\textcolor{tuklblau!80}{\esm@dispfigure{} \theesmfigurecounter :} #1}
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
\newcounter{esmlistingcounter}[esmsheetnumber]
\renewcommand{\theesmlistingcounter}{
	\theesmsheetnumber.\arabic{mylistings}
}

% Befehl um Listing-Titel zu schreiben [title=\lstcap{...}]
\newcommand{\lstcap}[1]{\refstepcounter{mylistings}\color{tuklblau!80}\itshape \esm@displisting{} \theesmlistingcounter: #1
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
% HINWEISBOX
\newcounter{esmhintcounter}[esmsheetnumber]
\renewcommand{\theesmhintcounter}{\theesmsheetnumber.\arabic{esmhintcounter}}
\newcommand{\Hinweis}[1]{
	\refstepcounter{esmhintcounter}
	\begin{center}
		\colorbox{tuklblau!10}{
		\begin{minipage}{0.85\textwidth}
			\begin{center}
			\textcolor{tuklblau}{
				\textbf{\Large \esm@disphint{} \theesmhintcounter}}\\ \textcolor{black}{#1}
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
