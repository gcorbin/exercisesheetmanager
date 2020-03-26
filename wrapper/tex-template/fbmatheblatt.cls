% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% LATEX-Klasse für Übungsblätter, Fachbereich Mathematik
%
%	Version vom 29.04.2016
%
%	Autor:	Andreas Roth
%			KOMMS, FB Mathematik
%			TU Kaiserslautern
%			roth@mathematik.uni-kl.de
%			Tel.: 0631 205 4496
%			Raum 48-557
%
%   modifiziert:
%   -20.10.2018, Matthias Andres, TUK, mandres@mathematik.uni-kl.de; manueller Übungsblattname (Präsenz, Hausübung)
%     																										 manueller Name der deadline,
%																											 loesungen interface
%   -Gregor Corbin, TUK, corbin@mathematik.uni-kl.de
%
%	Die Nutzung ist jedem zur Verwendung in beliebigen Veranstaltungen des
%	Fachbereichs gestattet. Die Gestaltung ist an das Corporate Design der
%	Uni Kaiserslautern angelehnt.
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BENUTZUNG:
%
% 	Man erstelle ein .tex-File und führe die folgenden Schritte durch:
%
%	1. \documentclass{fbmatheblatt}
%
%	2. Veranstaltungsdaten setzen:
%		\Veranstaltung{<Veranstaltungsname>}
%       \Semester{<Semester>}
%		\Dozenten{<Name1>\\<Name2>}
%        ...
%
%	3. \begin{document}
%
%	4. Neues Blatt anlegen:
%		4.2 Blatt anlegen mit Umgebung:
%			\begin{Blatt}%
%				4.2.1 Aufgaben einbinden mit Umgebung:
%					\begin{Aufgabe}{<Titel>}{<Punkte>}
%
%						... Text ...
%					\end{Aufgabe}
%
%				Wiederhole 4.2.1 bis genügend Aufgaben vorhanden!
%
%			\end{Blatt}
%
%	Wiederhole 4, bis genügend Blätter vorhanden!
%
%	5. \end{document}
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DEFINIERTE BEFEHLE:
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
% UMGEBUNGEN:
% 
%	- Blatt
% 	- Disclaimer (Ein roter Text, der auf Formalitäten zur Abgabe hinweist)
%   - Aufgabe (Für Präsenzübungen o.ä., hat keine Punkte)
% 	- Hausaufgabe (für Hausaufgaben o.ä., hat ein extra Argument, um in Klammern die Punkte anzuzeigen)
% 	- Loesung (wird mit der Klassenoption 'Loesungen' aktiviert, ansonsten auskommentiert)
% 	- Punkte (Um Bepunktungshinweise für Tutoren zu geben, ist nur aktiv, wenn die Optionen 'Loesungen' und 'Punkte' gegeben sind)
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


\LoadClass{scrartcl}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fbmatheblatt}[2019/12/10 Uebungsblatt FB Mathematik]

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% PAKETE
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
\RequirePackage{verbatim} % für die macros \comment und \endcomment

\newif\ifenglish
\englishfalse %Default: german

\DeclareOption{English}{\englishtrue}
\DeclareOption{German}{\englishfalse}


\newif\ifloesung
\loesungfalse
\DeclareOption{Loesungen}{\loesungtrue}

\newif\ifpunkte
\punktefalse
\DeclareOption{Punkte}{\punktetrue}


\ProcessOptions\relax

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Anzeigenamen für Umbegungen
\newcommand{\theBlattname}{Blatt}
\newcommand{\Aufgabenname}{Aufgabe}
\newcommand{\Hausaufgabenname}{Hausaufgabe}
\newcommand{\Loesungsname}{L\"{o}sung}
\newcommand{\Punktename}{Punktevergabe}
\newcommand{\Hinweisname}{Hinweis}
\newcommand{\Seitenname}{Seite}
\newcommand{\Bildname}{Abbildung}
\newcommand{\Listingname}{Listing}
\newcommand{\Abgabedatumname}{Abgabe bis}

\ifenglish
\renewcommand{\theBlattname}{Sheet}
\renewcommand{\Aufgabenname}{Exercise}
\renewcommand{\Hausaufgabenname}{Homework}
\renewcommand{\Loesungsname}{Solution}
\renewcommand{\Punktename}{Grading}
\renewcommand{\Hinweisname}{Hint}
\renewcommand{\Seitenname}{Page}
\renewcommand{\Bildname}{Figure}
\renewcommand{\Listingname}{Listing}
\newcommand{\Abgabedatumname}{Due date}
\fi

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DATEN FÜR VERANSTALTUNG
\newcommand{\theVeranstaltung}{}
\newcommand{\theSemester}{}
\newcommand{\theDozenten}{}
\newcommand{\theErscheinungsdatum}{}
\newcommand{\theAbgabedatum}{}

\newcommand{\Veranstaltung}[1]{\renewcommand{\theVeranstaltung}{#1}}
\newcommand{\Semester}[1]{\renewcommand{\theSemester}{#1}}
\newcommand{\Blattname}[1]{\renewcommand{\theBlattname}{#1}}
\newcommand{\Blattnummer}[1]{\setcounter{blatt}{\numexpr #1 -1}}
\newcommand{\Dozenten}[1]{\renewcommand{\theDozenten}{#1}}
\newcommand{\Erscheinungsdatum}[1]{\renewcommand{\theErscheinungsdatum}{#1}}
\newcommand{\Abgabedatum}[1]{\renewcommand{\theAbgabedatum}{#1}}

\newcommand{\setzeHeader}{
	\ihead{\theVeranstaltung\\ \theBlattname{} \theblatt}
	\ifoot{\theDozenten}
	\ohead{\theSemester, \theErscheinungsdatum\\ \Seitenname \pagemark /\pageref{LastPage}}
	\ofoot{
		\begin{tabular}{l}
			\Abgabedatumname{}:\\
			\theAbgabedatum
		\end{tabular}
	}
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% EIGENE COUNTER

% Blattcounter
\newcounter{blatt}
% Gleichungscounter
\numberwithin{equation}{blatt}
% Aufgabencounter
\newcounter{aufgaben}[blatt]
\renewcommand{\theaufgaben}{\theblatt.\arabic{aufgaben}}
\newcounter{hausaufgaben}[blatt]
\renewcommand{\thehausaufgaben}{\theblatt.\arabic{hausaufgaben}}
\newcounter{loesungen}[blatt]
\renewcommand{\theloesungen}{\theblatt.\arabic{loesungen}}

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
% Figurecounter soll Blattzahl enthalten
\newcounter{bilder}[blatt]
\renewcommand{\thebilder}{\theblatt.\arabic{bilder}}

% Ersetzt caption
\newcommand{\bild}[1]{
	\refstepcounter{bilder}
	\caption*{
		\textit{\textcolor{tuklblau!80}{\Bildname{} \thebilder :} #1}
	}
}
% Referenz auf Bild
\newcommand{\bildref}[1]{
	\textcolor{tuklblau!80}{\Bildname{} \ref{#1}}
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
\newcounter{mylistings}[blatt]
\renewcommand{\themylistings}{
	\theblatt.\arabic{mylistings}
}

% Befehl um Listing-Titel zu schreiben [title=\lstcap{...}]
\newcommand{\lstcap}[1]{\refstepcounter{mylistings}\color{tuklblau!80}\itshape \Listingname{} \themylistings: #1
}

% Befehl, um auf Listings zu referenzieren
\newcommand{\lstref}[1]{
	\textcolor{tuklblau!80}{\Listingname{} \ref{#1}}
}

% Quelltext im Fließtext hervorheben mit:
\newcommand{\codi}[1]{\texttt{#1}}
% Im kursiv gedruckten Kontext:
\newcommand{\codif}[1]{\normalfont\texttt{#1}}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEFEHL FÜR BLATT
\newenvironment{Blatt}[1]{
	\refstepcounter{blatt}
	\setzeHeader
	\section*{\centering \LARGE \theBlattname{} \theblatt}
}{\newpage}

\newcommand{\disclaimerStil}{\color{tuklrot}}
\newenvironment{Disclaimer}{%
	\begin{center}%
		\begin{minipage}{0.9\textwidth}%
			\disclaimerStil
		}{%
		\end{minipage}
	\end{center}
}

\newcommand{\pathToResource}{.}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEFEHL FÜR AUFGABE
\newenvironment{Aufgabe}[1]{
	\refstepcounter{aufgaben}
	\par\hrulefill
	\subsection*{\Aufgabenname{} \theaufgaben: \textit{#1 }}
}{}

\newenvironment{Hausaufgabe}[2]{
	\refstepcounter{hausaufgaben}
	\par\hrulefill
	\subsection*{\Hausaufgabenname{} \thehausaufgaben: \textit{#1%
		\ifx#2%
		\else%
		(#2)%
		\fi%
	}}
}{}


\newenvironment{Loesung}{\comment}{\endcomment}
\newenvironment{Punkte}{\comment}{\endcomment}

\ifloesung
	\renewenvironment{Loesung}{%
		\refstepcounter{loesungen}
		\subsection*{\Loesungsname{}}
	}{}%
	\ifpunkte
		\renewenvironment{Punkte}{
			\subsection*{\Punktename{}}
		}{}%
	\fi
\fi

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Gekapselte befehle für Aufgaben

\newcommand{\inputInclass}[2]{%
    \begin{Aufgabe}{#2}
        \renewcommand{\pathToResource}{#1}
        \input{#1/exercise.tex}
    \end{Aufgabe}
}

\newcommand{\inputHomework}[3]{%
    \begin{Hausaufgabe}{#2}{#3}
        \renewcommand{\pathToResource}{#1}
        \input{#1/exercise.tex}
    \end{Hausaufgabe}
}

\newcommand{\inputSolution}[1]{%
    \begin{Loesung}
        \renewcommand{\pathToResource}{#1}
        \input{#1/solution.tex}
    \end{Loesung}
}

\newcommand{\inputAnnotation}[1]{%
    \begin{Punkte}
        \input{#1}
    \end{Punkte}
}


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% HINWEISBOX
\newcounter{hinweise}[blatt]
\renewcommand{\thehinweise}{\theblatt.\arabic{hinweise}}
\newcommand{\Hinweis}[1]{
	\refstepcounter{hinweise}
	\begin{center}
		\colorbox{tuklblau!10}{
		\begin{minipage}{0.85\textwidth}
			\begin{center}
			\textcolor{tuklblau}{
				\textbf{\Large \Hinweisname{} \thehinweise}}\\ \textcolor{black}{#1}
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
