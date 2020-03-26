% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% USAGE:
%   1. Options: 
% 	solutions: toggle solution environment, if not given, the content of the environment is commented out
% 	annotations: toggle annotation environment, if not given, the content of the environment is commented out
%   german: set language to german
%   english: set language to english, default
%   
% EXAMPLE
%\documentclass[english, solutions, annotations]{exercisesheet}
%
% % set metadata
%\semester{SS2020}
%\lecture{Intro to ODEs}
%\sheetname{Assignments}
%\sheetno{1}
%\lecturer{Prof. M. Mustermann \\ Dr. M. Musterfrau} 
%\releasedate{01.01.2020}
%\deadline{08.01.2020, 12:00}
%
%\begin{document}%	
%	\begin{sheet}
%		\begin{disclaimer}
%			Solutions submitted after the deadline will not be graded!
%		\end{disclaimer}
%		
%		\begin{homework}{A simple task}{5 Points}
%       	Solve $\dot{x} = x$ for initial condition $x(0) = 1$. 
%       \end{homework}
%		\begin{solution}
%        	x = \exp(t)
%       \end{solution}
%       \begin{annotation}
%			All points or none. 
%		\end{annotation}
%	\end{sheet}
%\end{document}

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Environments:
% 
%	- sheet
% 	- disclaimer (for formalities concerning the exercise)
%   - inclass (for class exercises, no points)
% 	- homework (for homework tasks, has an optional argument to display number of points in brackets)
% 	- solution (for solutions to both inclass and homework tasks, has to be activated with the class option 'solutions')
% 	- annotation (extra annotations for tutors, has to be activated with the class option 'annotations' )
% 

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
% DISPLAY Names
\newcommand{\esm@dispsheet}{\esmsheetnumber}
\newcommand{\esm@dispinclass}{Aufgabe}
\newcommand{\esm@disphomework}{Hausaufgabe}
\newcommand{\esm@dispsolution}{L\"{o}sung}
\newcommand{\esm@dispannotation}{Punktevergabe}
\newcommand{\esm@disppage}{Seite}
\newcommand{\esm@dispduedate}{Abgabe bis}

\ifenglish
\renewcommand{\esm@dispsheet}{Sheet}
\renewcommand{\esm@dispinclass}{Exercise}
\renewcommand{\esm@disphomework}{Homework}
\renewcommand{\esm@dispsolution}{Solution}
\renewcommand{\esm@dispannotation}{Grading}
\renewcommand{\esm@disppage}{Page}
\renewcommand{\esm@dispduedate}{Due date}
\fi

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% METADATA
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
% COUNTER
\newcounter{esmsheetnumber}
\numberwithin{equation}{esmsheetnumber}
\newcounter{inclasscounter}[esmsheetnumber]
\renewcommand{\theinclasscounter}{\theesmsheetnumber.\arabic{inclasscounter}}
\newcounter{homeworkcounter}[esmsheetnumber]
\renewcommand{\thehomeworkcounter}{\theesmsheetnumber.\arabic{homeworkcounter}}
\newcounter{solutioncounter}[esmsheetnumber]
\renewcommand{\thesolutioncounter}{\theesmsheetnumber.\arabic{solutioncounter}}


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% SHEET
\newenvironment{sheet}[1]{
	\refstepcounter{esmsheetnumber}
	\esm@setheaderfooter
	\section*{\centering \LARGE \esm@dispsheet{} \theesmsheetnumber}
}{\newpage}

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
% ENVIRONMENTS FOR TASKS, SOLUTION, ANNOTATION
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

\ifsolutions
	\newenvironment{solution}{%
		\refstepcounter{solutioncounter}
		\subsection*{\esm@dispsolution{}}
	}{}%
\else
	\newenvironment{solution}{\comment}{\endcomment}
\fi

\ifannotations
	\newenvironment{annotation}{
		\subsection*{\esm@dispannotation{}}
	}{}%
\else
	\newenvironment{annotation}{\comment}{\endcomment}
\fi


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% INTERFACE to the exercise sheet manager scripts

\newcommand{\inputInclass}[2]{%
	\begin{inclass}{#2}
		\renewcommand{\pathToResource}{#1}
		\input{#1/exercise.tex}
	\end{inclass}
}

\newcommand{\inputHomework}[3]{%
	\begin{homework}{#2}{#3}
		\renewcommand{\pathToResource}{#1}
		\input{#1/exercise.tex}
	\end{homework}
}

\ifsolutions
	\newcommand{\inputSolution}[1]{%
		\begin{solution}
			\renewcommand{\pathToResource}{#1}
			\input{#1/solution.tex}
		\end{solution}
	}	
\else
	\newcommand{\inputSolution}[1]{}
\fi

\ifannotations
	\newcommand{\inputAnnotation}[1]{%
		\begin{annotation}
			\input{#1}
		\end{annotation}
	}
\else
	\newcommand{\inputAnnotation}[1]{}
\fi