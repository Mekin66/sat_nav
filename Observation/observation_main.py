from Observation.observation_c import analyse_satellites
from Observation.observation_d import plot_gps_l1
from Observation.observation_e import vergleiche_galileo_e1_e5
from Observation.observation_f import vergleiche_traegerphase
from Observation.observation_g import vergleiche_doppler


def run(data_stat, data_dyn):
    """
    Fuehrt alle Aufgaben aus Aufgabenblock 2 (Observablen) aus. Die
    Aufgaben c-f arbeiten auf der statischen Aufzeichnung, fuer Aufgabe g)
    wird zusaetzlich die dynamische Aufzeichnung zum Dopplervergleich
    herangezogen.

    :param data_stat: Statische Beobachtungsdaten
    :param data_dyn: Dynamische Beobachtungsdaten
    :return: None
    """
    print("\n=== Aufgabe c: Satelliten pro System ===")
    analyse_satellites(data_stat)

    print("\n=== Aufgabe d: GPS L1 C/A-Signal ===")
    plot_gps_l1(data_stat)

    print("\n=== Aufgabe e: Galileo E1 vs. E5 ===")
    vergleiche_galileo_e1_e5(data_stat)

    print("\n=== Aufgabe f: Pseudorange vs. Traegerphase ===")
    vergleiche_traegerphase(data_stat)

    print("\n=== Aufgabe g: Dopplervergleich statisch/dynamisch ===")
    vergleiche_doppler(data_stat, data_dyn)
