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
%   20.10.2018, Matthias Andres, TUK, mandres@mathematik.uni-kl.de; manueller Übungsblattname (Präsenz, Hausübung)
%     																										 manueller Name der deadline,
%																											 loesungen interface
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
%		\Veranstaltung{<Veranstaltungsname Semester>}
%		\Dozenten{<Name1>\\<Name2>}
%
%	3. \begin{document}
%
%	4. Neues Blatt anlegen:
%		4.1 Optional Abgabedaten setzen:
%			\Daten{Erscheinungsdatum}{Abgabedatum\\Abgabezeit}{Name der deadline}{Manueller Blattname}{Manuelle Blattnummer}
%       z.B. \Daten{10.04.2018}{17.04.2018}{Abgabe am: }{Pr\"{a}senzblatt }{1}
%
%		4.2 Blatt anlegen mit Umgebung:
%			\begin{Blatt}{<TexFile mit Hinweisen>}
%
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
%	- \bemerkung{Text}:
%		Eine mit Blattnummer nummerierte, blaue Bemerkungsbox
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
%	- \figureref{label}
%		Referenziere im Text auf eine Abbildung mit label label
%
%	- \lstref{label}
%		Referenziere im Text auf Listing mit label label
%
%	- \myhref{url}{beschreibung}
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


\LoadClass{scrartcl}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fbmatheblattEWP}[2016/04/29 Uebungsblatt FB Mathematik]

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

\newif\ifloesung
\loesungfalse
\newenvironment{Loesung}{\comment}{\endcomment}
\DeclareOption{Loesungen}{%
	\renewenvironment{Loesung}{%
		\refstepcounter{loesungen}
		\subsection*{L\"{o}sung}
	}{}%
	\loesungtrue
}

\newif\ifpunkte
\punktefalse
\newenvironment{Punkte}{\comment}{\endcomment}
\newcommand{\punkte}[1]{}
\DeclareOption{Punkte}{%
	\ifloesung%
		\renewenvironment{Punkte}{
			\subsection*{Punktevergabe}
		}{}%
		\renewcommand{\punkte}[1]{\hfill \mbox{#1 Punkte}}
		\punktetrue
	\fi
}
\ProcessOptions\relax

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
\newcounter{myfigures}[blatt]
\renewcommand{\themyfigures}{\theblatt.\arabic{myfigures}}

% Ersetzt caption
\newcommand{\bild}[1]{
	\refstepcounter{myfigures}
	\caption*{
		\textit{\textcolor{tuklblau!80}{Abbildung \themyfigures :} #1}
	}
}
% Referenz auf Bild
\newcommand{\figureref}[1]{
	\textcolor{tuklblau!80}{Abbildung \ref{#1}}
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
\newcommand{\lstcap}[1]{\refstepcounter{mylistings}\color{tuklblau!80}\itshape Listing \themylistings: #1
}

% Befehl, um auf Listings zu referenzieren
\newcommand{\lstref}[1]{
	\textcolor{tuklblau!80}{Listing \ref{#1}}
}

% Quelltext im Fließtext hervorheben mit:
\newcommand{\codi}[1]{\texttt{#1}}
% Im kursiv gedruckten Kontext:
\newcommand{\codif}[1]{\normalfont\texttt{#1}}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEFEHL FÜR BLATT
\newenvironment{Blatt}[1]{
	\refstepcounter{blatt}
	\section*{\centering \LARGE \Blattname \theblatt}
	\begin{center}
		\begin{minipage}{0.9\textwidth}
			\color{tuklrot}\input{#1}
		\end{minipage}
	\end{center}
}{\newpage}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEFEHL FÜR AUFGABE
\newenvironment{Aufgabe}[1]{
	\refstepcounter{aufgaben}
	\par\hrulefill
	\subsection*{Aufgabe \theaufgaben: \textit{#1 }}
}{}

\newenvironment{Hausaufgabe}[2]{
	\refstepcounter{hausaufgaben}
	\par\hrulefill
	\subsection*{Hausaufgabe \thehausaufgaben: \textit{#1%
		\ifx#2%
		\else%
		(#2)%
		\fi%
	}}
}{}


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% BEMERKUNGSBOX
% Bemerkungsbox
\newcounter{remarks}[blatt]
\renewcommand{\theremarks}{\theblatt.\arabic{remarks}}
% Box
\newcommand{\bemerkung}[1]{
	\refstepcounter{remarks}
	\begin{center}
		\colorbox{tuklblau!10}{
		\begin{minipage}{0.85\textwidth}
			\begin{center}
			\textcolor{tuklblau}{
				\textbf{\Large Hinweis \theremarks}}\\ \textcolor{black}{#1}
			\end{center}
		\end{minipage}}
	\end{center}
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DATEN FÜR VERANSTALTUNG
\newcommand{\Veranstaltung}[1]{
	\ihead{#1\\ \Blattname \theblatt}
}

\newcommand{\Dozenten}[1]{
	\ifoot{#1}
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% DATEN FÜR BLATT SETZEN
\newcommand{\Daten}[5]{
	\ohead{#1\\Seite \pagemark /\pageref{LastPage}}
	\ofoot{\begin{tabular}{ll}
					\makecell{#3} & \makecell{#2}
					\end{tabular}}\setcounter{blatt}{\numexpr #5 -1} \newcommand{\Blattname}{#4 }
}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% SONSTIGE BEFEHLE

% Links
\newcommand{\myhref}[2]{
	\href{#1}{\textcolor{tuklblau}{#2}}
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
