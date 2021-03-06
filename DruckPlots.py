#!/usr/bin/env python3

print('Lade Bibliotheken, Geduld bitte')

print('  1/3 Lade Systembibliotheken')
import math
import os
import glob
import json
from time import sleep
print('  2/3 Lade Pandas')
import pandas as pd
import pandas.plotting._matplotlib
print('  3/3 Lade Matplotlib')
import matplotlib.pyplot as plt


def wait_and_exit(code=0, secs=600):
    print('Beende Programm mit Ctrl+C')
    sleep(secs)
    exit(code)


def read_werte(wertefile='Werte.json'):
    try:
        werte = json.load(open(wertefile))
    except:
        werte = {}

    must_update = False
    if not 'WICHTE' in werte:
        werte['WICHTE'] = 15.0
        print(f'Bitte ändere "WICHTE" in {wertefile}')
        must_update = True
    if not 'CU_FAKTOR' in werte:
        werte['CU_FAKTOR'] = 20.0
        print(f'Bitte ändere "CU_FAKTOR" in {wertefile}')
        must_update = True
    if not 'MAXTIEFE' in werte:
        werte['MAXTIEFE'] = 40.0
        print(f'Bitte ändere "MAXTIEFE" in {wertefile}')
        must_update = True
    if not 'STATS' in werte:
        werte['STATS'] = 'C_u'
        print(f'Bitte ändere "STATS" in {wertefile}')
        must_update = True

    if must_update:
        json.dump(werte, open(wertefile, 'w'), indent=2)

    return werte['WICHTE'], werte['CU_FAKTOR'], werte['MAXTIEFE'], werte['STATS']


WICHTE, CU_FAKTOR, MAXTIEFE, STATSNAME = read_werte()

print(f'WICHTE: {WICHTE}')
print(f'CU_FAKTOR: {CU_FAKTOR}')
print(f'MAXTIEFE: {MAXTIEFE}')

LIMITSFILE = 'Grenzen.csv'

BASEDIR = '1_Rohdaten_EXCEL'
CU_OUTPUT_DIR = '2_Cu_CSV'
PLOTDIR = '3_Plots'
ANALYSISDIR = '4_Statistik'

def makedir(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


makedir(BASEDIR)
makedir(CU_OUTPUT_DIR)
makedir(PLOTDIR)
makedir(ANALYSISDIR)


def pathsafe(_sondierungsnummer):
    return "".join([c for c in _sondierungsnummer.replace('/', '_').replace('\\', '_') if c.isalpha() or c.isdigit() or c in ['_']]).strip()


if __name__ == "__main__":
    xlsfiles = glob.glob(os.path.join(BASEDIR, '*.xlsx')) + \
        glob.glob(os.path.join(BASEDIR, '*.xls'))

    all_analyses = {}

    try:
        limits_df = pd.read_csv(LIMITSFILE)
    except:
        limits_df = pd.DataFrame(
            columns=['sondierungsnummer', 'depth_min', 'depth_max'])
        limits_df.to_csv(LIMITSFILE, index=False)
    limits_df = limits_df[['sondierungsnummer', 'depth_min', 'depth_max']]
    print(f'Limits: ({LIMITSFILE})')
    print(limits_df)

    for excel_filename in xlsfiles:
        print(f'reading {excel_filename}')

        xl = pd.ExcelFile(excel_filename)

        if not 'Kopfdaten' in xl.sheet_names or not 'Data' in xl.sheet_names:
            print('  FEHLER: Tabellenblätter "Kopfdaten" und "Data" nicht enthalten')
            print(f'  Enthaltene Tabellenblätter: {xl.sheet_names}')
            continue

        info_df = pd.read_excel(xl, sheet_name='Kopfdaten', header=None)
        data_df = pd.read_excel(xl, sheet_name='Data')

        sondierungsnummer_df = info_df[info_df[0] == 'Sondierungs-Nummer']
        assert(len(sondierungsnummer_df) == 1)
        sondierungsnummer = sondierungsnummer_df[1].values[0]

        print(
            f'  Sondierungsnummer: {sondierungsnummer} ({pathsafe(sondierungsnummer)})')

        subdata_df = data_df[['Depth [m]', 'Cone resistance (qc) in MPa']]
        subdata_df.columns = ['depth_m', 'qc_MPa']
        subdata_df = subdata_df[subdata_df.qc_MPa > 0]

        assert(len(subdata_df) > 1)

        subdata_df['qc_kN'] = subdata_df.qc_MPa * 1000
        subdata_df['Ueberlagerungsdruck_kN'] = subdata_df.depth_m * WICHTE
        subdata_df['C_u'] = (subdata_df.qc_kN -
                             subdata_df.Ueberlagerungsdruck_kN) / CU_FAKTOR

        subdata_df.to_csv(
            f'{CU_OUTPUT_DIR}/{pathsafe(sondierungsnummer)}.csv', index=False)

        minmax_df = limits_df[limits_df.sondierungsnummer == sondierungsnummer]

        depth_min = None
        depth_max = None
        if len(minmax_df) == 1:
            depth_min = minmax_df.depth_min.values[0]
            depth_max = minmax_df.depth_max.values[0]
        elif len(minmax_df) == 0:
            print(f'  adding {sondierungsnummer} to {LIMITSFILE}')
            limits_df = limits_df.append(
                {'sondierungsnummer': sondierungsnummer}, ignore_index=True)
            limits_df.to_csv(LIMITSFILE, index=False)
        else:
            print(f'  FEHLER: {sondierungsnummer} doppelt in {LIMITSFILE}')
            continue

        total_depth_min = subdata_df.depth_m.min()
        total_depth_max = subdata_df.depth_m.max()
        if depth_min == None or math.isnan(depth_min):
            depth_min = total_depth_min
        if depth_max == None or math.isnan(depth_max):
            depth_max = total_depth_max

        print(f'  depth min/max: {depth_min} - {depth_max}')

        if depth_min == depth_max:
            print(
                f'  WARNUNG: {sondierungsnummer} wird ignoriert. Werte wurden manuell auf {depth_min} == {depth_max} gesetzt')
            analysis = None
        else:
            analysis_df = subdata_df[subdata_df.depth_m.between(depth_min, depth_max, inclusive='both')]
            stats_values = analysis_df[STATSNAME]
            # analysis_df = subdata_df[]
            analysis = {
                'min': stats_values.min(),
                'max': stats_values.max(),
                'mean': stats_values.mean(),
                'median': stats_values.median(),
                'stddev': stats_values.std(),
            }
            all_analyses[sondierungsnummer] = analysis
            # TODO: analyse hier
            pass

        ax = subdata_df.plot('depth_m', STATSNAME)
        figure = ax.get_figure()

        ax.set_xlim([0, max(MAXTIEFE, total_depth_max)])
        for n in range(0, int(math.ceil(total_depth_max))):
            ax.axvline(n, color='grey', linewidth=0.2 if n % 5 else 0.5)

        if analysis:
            ax.text(0.4, 0.95, '\n'.join([f'{k}: {round(v, 1)}' for k, v in analysis.items()]),
                    verticalalignment='top', transform=ax.transAxes, bbox={'facecolor': 'white', 'alpha': 0.5})

        ax.set_xlabel('Tiefe [$m$]')
        if STATSNAME == 'C_u':
            ax.set_ylabel('$C_u$ [$kN/m^2$]')
            ax.set_title(f'{sondierungsnummer}: Undränierte Scherfestigkeit $C_u$')
        elif STATSNAME == 'qc_kN':
            ax.set_ylabel('$q_c$ [$kN$]')
            ax.set_title(f'{sondierungsnummer}: Spitzendruck $q_c$')
        else:
            ax.set_ylabel(f'${STATSNAME}$')
            ax.set_title(f'{sondierungsnummer}: ${STATSNAME}$')
        ax.legend([sondierungsnummer])

        ax.axvspan(depth_min, depth_max, alpha=0.2)

        plot_filename = f'{PLOTDIR}/{pathsafe(sondierungsnummer)}.png'
        print(f'  saving {plot_filename}')
        figure.savefig(plot_filename)
        print('')

        plt.close(figure)

    with open(f'{ANALYSISDIR}/all.txt', 'w') as all_analysis_file:
        for sondierungsnummer, analysis in all_analyses.items():
            analysis_filename = f''
            with open(f'{ANALYSISDIR}/{pathsafe(sondierungsnummer)}.txt', 'w') as analysis_file:
                for outfile in [analysis_file, all_analysis_file]:
                    outfile.write(f'sondierungsnummer: {sondierungsnummer}\n')
                    outfile.write(
                        '\n'.join([f'{k}: {round(v, 1)}' for k, v in analysis.items()]))
                    outfile.write('\n\n')

