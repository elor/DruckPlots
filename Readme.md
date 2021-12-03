# DruckPlots

## Beschreibung

Programm zum Auswerten und Rendern von Druck-Bohrdaten in einem proprietärem _(?)_ Format.

Das Programm liest Druck-Daten als Excel-Dateien ein und generiert hübsche Diagramme daraus.
Außerdem wird eine statistische Analyse durchgeführt.

## Benutzung

1. Lege deine Excel-Dateien in `1_Rohdaten_Excel/` ab
   * Unterstützt: `.xls` und `.xlsx`
2. Passe die Werte für Wichte und Cu-Faktor in `Werte.json` an
3. Starte DruckPlots.exe
    * Geduld: Der erste Programmstart dauert bis zu einige Minuten, bevor etwas angezeigt wird
    * Bilder werden unter `3_Plots/` abgelegt
    * Statistiken werden unter `4_Statistik/` abgelegt
4. Setze die Statistik-Bereiche für jede Sondierung unter `Grenzen.csv`
   * Ändere z.B. `B 19/19,,` zu `B 19/19,6,35` um für Sondierung B 19/19 einen Statistik-Bereich von [6,35] auszuwählen
   * auf -1,-1 setzen, um keinen blauen Hintergrund anzuzeigen 
   * Die Analyse erfolgt nur im blauen Bereich
6. Starte DruckPlots.exe erneut, um Bilder und Statistiken anhand der neuen Grenzen zu aktualisieren

## Konfiguration

Ändere die Werte in `Werte.json`

STATS kann dabei `qc_kN` oder `C_u` sein

## Installation

1. Lade `DruckPlots.exe` herunter
2. Führe DruckPlots.exe einmal aus, um alle Verzeichnisse und Dateien zu erzeugen

## Kompilierung von DruckPlots.exe

1. `conda env create -n druckplots -f requirements.txt`
2. `conda activate druckplots`
3. `pyinstaller.exe --exclude-module PyQt5 -F DruckPlots.py`
4. `DruckPlots.exe` zum Testen einmal starten
