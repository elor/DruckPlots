# DruckPlots

## Beschreibung

Programm zum Auswerten und Rendern von Druck-Bohrdaten in proprietärem _(?)_ Format.

Das Programm liest Druck-Daten als Excel-Dateien einPlots ab

## Benutzung

1. Lege Excel-Dateien in 1_Rohdaten_Excel ab
   * Unterstützt: `.xls` und `.xlsx`
2. Schreibe Wert für die Wichte in Wichte.txt
3. Starte DruckPlots.exe
    * Geduld: Programmstart dauert bis zu einigen Minuten, bevor etwas angezeigt wird
4. Ändere die Grenzwerte unter `5_Grenzen/limits.csv`
   * Legt den Bereich für den blauen Hintergrund in den Plots fest
   * auf -1,-1 setzen, um keinen blauen Hintergrund anzuzeigen 
5. Starte WichtePlotx.exe erneut, um blaue Hintergründe zu erzeugen

## Installation / Kompilierung

1. `conda env create -n druckplots -f requirements.txt`
2. `conda activate druckplots`
3. `pyinstaller.exe -F DruckPlots.py`
4. `DruckPlot.exe` zum Testen einmal starten
