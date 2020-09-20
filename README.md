Einge Hinweise zu unserer Implementierung:

#########################################

Zur Ausführung wird benötigt:

- eine aktuelle Version von Python3 (3.8)
- eine aktuelle Version von pyboolector (3.2.1)
- zum Ausführen der Testfälle: eine aktuelle Version von pytest (5.4.3)

Am einfachsten sind diese dependencies in einer neuen venv zu installieren mittels:
pip install -r requirements.txt

#########################################

 Die Testfälle können entweder manuell mit
 ` pytest TESTDATEI.py `
 ausgeführt werden, dabei kann optional '-s'
 angegeben damit alle Ausgaben angezeigt werden. 

Einfacher ist es allerdings das bereitgestellte
Test-Skript ` test.sh` im test-Ordner auszuführen.
Dies führt alle Testfälle direkt aus.

Alle Testfälle liegen in einer seperaten Datei.
Dabei wird für jede getestet Funktion eine seperate Liste angelegt,
die die Eingabe(n) und die erwareteten Ausgabewerte erhält.
Je nach Funktion kann die erwartete Ausgabe sowohl eine weitere
Zahl aber auch SAT/UNSAT sein. Dies sollte sich aus dem Kontext
der jeweiligen Funktion ergeben.

Unsere Implementierung befindet sich in der Datei `FBoolector.py`, die
Interfaces, die für den Benutzer gedacht sind befinden sich (der
Übersichtlichkeit halber) in der seperaten Datei `FBoolectorInterface.py`.
In beiden Dateien sind die Funktionen, ihre Eingabe und Ausgabe jeweils
entsprechend dokumentiert.

Die Datei `quadratic_equation_test.py` beinhaltet ein kleines Bespielprogramm,
das die Nullstellen einer Funktion berechnet.
Die Datei `presenation.py` zeigt vergleicht zwei Möglichkeiten wie die Wurzel
einer Zahl berechnet werden kann.
Beide Beispielprogramme können mit `python -m examples.FILENAME` (ohne .py)
ausgeführt werden.
