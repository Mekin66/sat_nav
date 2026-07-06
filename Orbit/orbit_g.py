import numpy as np
import matplotlib.pyplot as plt
import Orbit.orbit_basis as hf


def berechne_eci(eph, t_eval):
    """
    Berechnet die Position des Satelliten im ECI (Erdzentriertes inertiales
    Koordinatensystem) zu einem bestimmten Auswertungszeitpunkt.
    Verwendet hierbei explizit die Gleichung (23) aus dem Skript.

    :param eph: Ephemeridendaten des zu berechnenden Satelliten
    :param t_eval: Auswertungszeitpunkt (als np.datetime64)
    :return: x, y, z (ECI-Koordinaten in Metern)
    """
    # KORREKTUR: tk wird ueber die datetime64-Werte berechnet
    epoche_zeit = eph.time.values
    tk = hf.korrigiere_zeit(t_eval, epoche_zeit)

    xk_prime, yk_prime, ik, Ek = hf.berechne_orbit_ebene(eph, tk)

    omega0 = float(eph['Omega0'].values)
    omega_dot = float(eph['OmegaDot'].values)

    # Gleichung (23) exakt aus dem Skript (physikalischer Fehler im Skript uebernommen)
    omega_k = omega0 + omega_dot * tk

    # Gleichungen (19), (20), (21)
    x = xk_prime * np.cos(omega_k) - yk_prime * np.cos(ik) * np.sin(omega_k)
    y = xk_prime * np.sin(omega_k) + yk_prime * np.cos(ik) * np.cos(omega_k)
    z = yk_prime * np.sin(ik)

    return x, y, z


def plot_24h_eci(eph, start_zeit):
    """
    Berechnet die Position des Satelliten im ECI im 5-Minuten-Takt
    ueber 24 Stunden, plottet die 3D-Trajektorie und gibt die
    theoretische Antwort ueber den Unterschied zu ECEF auf der Konsole aus.

    :param eph: Ephemeridendaten des zu berechnenden Satelliten
    :param start_zeit: Beginn des zu plottenden Zeitraums (np.datetime64)
    :return: None
    """
    x_list = []
    y_list = []
    z_list = []

    i = 0
    while i < 288:
        t_eval = start_zeit + np.timedelta64(i * 300, 's')
        x, y, z = berechne_eci(eph, t_eval)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        i = i + 1

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_list, y_list, z_list, color='r', label="ECI Orbit")
    ax.set_xlabel("X in m")
    ax.set_ylabel("Y in m")
    ax.set_zlabel("Z in m")
    ax.set_title("Satellitenorbit im ECI ueber 24h")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("--- Antwort zur Theorie ---")
    print("Wie unterscheiden sich die Satellitenbahnen?")
    print(
        "ECEF: Rotiert mit der Erde. Hierdurch ist die relative Bewegung des Satelliten zur sich drehenden Erde sichtbar.")
    print("ECI: Inertialsystem, rotiert nicht mit der Erde. Die Bahn stellt sich als feststehende Ellipse im Raum dar.")