Wetterstation
====

Ziel dieses Projeks ist eine Python basierte Umsetzung, die Daten des Adafruit DTH 22 Temperatur-Sensors auf einem 4 Zeilen LCD-Display darzustellen.

## Voraussetzungen

* Raspberry Pi Model B (mindestens)
* HD44780 4x20 Zeichen Display
* Python 2.7 fuer den Raspberry Pie

## Verlauf

* Sensordaten aufnehmen (Shellscript basiert) &#x2713;
* Ausgabe auf dem Display (Zeit, Temperatur, Luftfeutigkeit) &#x2713;
* Lauftext in die 4. Zeile setzen &#x2713;
* Optionale Moeglichkeiten fuer die 4. Zeile einrichten (z.B. Temp-Differenz,...)
* Einfaches Konfigurationsscrip fuer "Modulauswahl"
* Umstellung der Sensordatenerfassung auf Python