import warnings as w
from pathlib import Path

import georinex as gr

from Orbit.orbit_basis import load_data as load_nav_data
from Observation import observation_main
from Orbit import orbit_main
from Positionsbestimmung import position_main
from Genauigkeit import genauigkeit_main

# Unterdruecke Warnungen beim Einlesen der Rohdaten in der Kommandozeile
w.filterwarnings("ignore", category=FutureWarning)

ROHDATEN_PFAD = Path("Rohdateien")
DATEI_STATISCH = ROHDATEN_PFAD / "gnss_log_2026_04_21_15_34_15.26o"
DATEI_DYNAMISCH = ROHDATEN_PFAD / "gnss_log_2026_04_21_16_03_28.26o"
DATEI_NAV = ROHDATEN_PFAD / "TIT200DEU_R_20261110000_01D_MN.rnx.gz"


def main():
    """
    Laedt die statische, die dynamische Beobachtungsaufzeichnung sowie die
    Navigationsdaten und fuehrt anschliessend nacheinander die vier
    Aufgabenbloecke des Institutsprojekts aus:

        2 - Observablen
        3 - Satellitenorbits
        4 - Positionsbestimmung
        5 - Genauigkeit

    Die Ergebnisse aus Aufgabenblock 4 werden an Aufgabenblock 5
    weitergereicht, da dort ein direkter Vergleich gefordert ist.

    :return: None
    """
    #Nur notwendige Sateliten laden
    sets = {'G', 'E'}
    data_stat = gr.load(DATEI_STATISCH, use=sets)
    data_dyn = gr.load(DATEI_DYNAMISCH, use=sets)
    data_nav = load_nav_data(DATEI_NAV, sets)

    print("\n########## Aufgabenblock 2: Observablen ##########")
    #observation_main.run(data_stat, data_dyn)

    print("\n########## Aufgabenblock 3: Satellitenorbits ##########")
    #orbit_main.run(data_nav)

    print("\n########## Aufgabenblock 4: Positionsbestimmung ##########")
    ergebnisse_block4 = position_main.run(data_stat, data_dyn, data_nav)

    print("\n########## Aufgabenblock 5: Genauigkeit ##########")
    genauigkeit_main.run(data_stat, data_dyn, data_nav, ergebnisse_block4)


if __name__ == "__main__":
    main()
