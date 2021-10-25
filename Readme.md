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
    * Geduld: Programmstart dauert bis zu einigen Minuten, bevor etwas angezeigt wird
    * Bilder werden unter `4_Plots/` abgelegt
    * Statistiken werden unter `5_Statistik/` abgelegt
4. Ändere die Grenzwerte unter `2_Grenzen/limits.csv`
   * Legt den Bereich für den blauen Hintergrund in den Plots fest
   * auf -1,-1 setzen, um keinen blauen Hintergrund anzuzeigen 
5. Starte DruckPlots.exe erneut, um blaue Hintergründe zu erzeugen

## Installation

1. Lade `DruckPlots.exe` und `Werte.json` herunter
2. Führe DruckPlots.exe aus, um die Verzeichnisse und Dateien zu erzeugen

## Kompilierung von DruckPlots.exe

1. `conda env create -n druckplots -f requirements.txt`
2. `conda activate druckplots`
3. `pyinstaller.exe --exclude-module PyQt5 --distpath . -F DruckPlots.py`
4. `DruckPlots.exe` zum Testen einmal starten
