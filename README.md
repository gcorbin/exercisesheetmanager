# ExerciseSheetManager

## Was ist das? 
* Ein kleines Python Programm, das unnötige Arbeit beim Erstellen von Übungsblättern vermeidet. 
* Latex-code für Aufgaben und Lösungen ist zentral in einer Aufgabensammlung organisiert. 
* Der ESM erzeugt vollständige Übungsblätter (Latex code und .pdf) aus den vorhandenen Aufgaben. 
* Metadaten zur aktuellen Veranstaltung und das Design der Blätter sind unabhängig von den Aufgaben
* Das Skript ist speziell für den Übungsbetrieb im Fachbereich Mathematik entwickelt worden. 

## Benutzung
* Im Ordner des aktuellen Semesters, z.B. EWP/WS1920/ einen Symlink zum sheet manager erstellen:
   ln -s ../../../exercisesheetmanager/wrapper/create_sheet.py create_sheet.py
* Dann in diesem Ordner z.B. python create_sheet.py sheet1.ini ausführen
* Flags:
    * -e (--exercise): Erstellt das Übungsblatt für die Studierenden
    * -s (--solution): Erstellt das Übungsblatt mit Lösung (für die Studierenden)
    * -a (--annotation): Erstellt das Übungsblatt mit Lösung und Hinweisen zur Punktevergabe (für Übungsleitende)
* Die Punkteverteilung kann für jedes Blatt und jede Aufgabe angegeben werden. Dazu muss im aktuellen Ordner z.B. die Datei sheet5_ex3.tex liegen.

# exercise pool
An exercise pool is a collection of exercises. Usually, an exercise sheet includes a subset of those exercises. Each exercise pool has its own folder with the following content:
* a subfolder for each exercise 
    * In this folder the Latex-code of the task is given in `task.tex`.
    * The solution can be provided optinally in `solution.tex`.
* literature.bib
    * Literatur in bibtex formated used by exercises in the pool.
    * Create an empty file if no literature is given.
* usermacros.tex
    * User defined marcos or additional usepackages required for exercises in the pool. 
    * Create an empty file if you do not need this.
* .search_index
    * Serach index for the pool. This folder is created by `exsec.py -u`.
    * There is no need to edit any information in this folder



