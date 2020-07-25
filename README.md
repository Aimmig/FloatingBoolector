Einge Hinweise zu unserer Implementierung:

#########################################

Zur Ausführung wird benötigt:

- eine aktuelle Version von Python3 (3.8)
- eine aktuelle Version von pyboolector (3.2.1)
- zum Ausführen der Testfälle: eine aktuelle Version von pytest (5.4.3)

Am einfachsten sind diese dependencies via pip zu installieren

`pip install pyboolector pytest`

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
