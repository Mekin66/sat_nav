import numpy as np
import matplotlib.pyplot as plt
from Orbit.orbit_d import berechne_ecef_und_uhr


def plot_24h_ecef(eph, start_zeit):
    """
    Berechnet die Position des Satelliten im ECEF im 5-Minuten-Takt
    ueber einen Zeitraum von 24 Stunden und plottet diese.

    :param eph: Ephemeridendaten des zu berechnenden Satelliten
    :param start_zeit: Beginn des zu plottenden Zeitraums
    :return: None
    """
    x_list = []
    y_list = []
    z_list = []

    i = 0
    while i < 288:
        t_eval = start_zeit + np.timedelta64(i * 300, 's')
        x, y, z, dt_sat = berechne_ecef_und_uhr(eph, t_eval)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        i = i + 1

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_list, y_list, z_list, label="ECEF Orbit")
    ax.set_xlabel("X in m")
    ax.set_ylabel("Y in m")
    ax.set_zlabel("Z in m")
    ax.set_title("Satellitenorbit im ECEF ueber 24h")
    plt.legend()
    plt.tight_layout()
    plt.show()