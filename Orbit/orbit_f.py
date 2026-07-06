import numpy as np
import matplotlib.pyplot as plt
from Orbit.orbit_d import berechne_ecef_und_uhr


def plot_24h_uhr(eph, start_zeit):
    """
    Berechnet den Verlauf der Satellitenuhrkorrektur im 5-Minuten-Takt
    ueber 24 Stunden und stellt diesen grafisch in einem 2D-Plot dar.

    :param eph: Ephemeridendaten des zu berechnenden Satelliten
    :param start_zeit: Beginn des zu plottenden Zeitraums 
    :return: None
    """
    zeit_list = []
    uhr_list = []

    i = 0
    while i < 288:
        dt_sekunden = i * 300
        t_eval = start_zeit + np.timedelta64(dt_sekunden, 's')
        x, y, z, dt_sat = berechne_ecef_und_uhr(eph, t_eval)
        zeit_list.append(dt_sekunden / 3600.0)
        uhr_list.append(dt_sat)
        i = i + 1

    plt.figure(figsize=(10, 6))
    plt.plot(zeit_list, uhr_list, label="Uhrenkorrektur")
    plt.xlabel("Zeit in Stunden")
    plt.ylabel("Korrektur in Sekunden")
    plt.title("Satellitenuhr-Verlauf ueber 24h")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()