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

