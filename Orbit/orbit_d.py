import numpy as np
import Orbit.orbit_basis as hf

def berechne_ecef_und_uhr(eph, t_eval):
    """
    Berechnet die Position des Satelliten im ECEF-Koordinatensystem sowie
    die Uhrenkorrektur zu einem bestimmten Auswertungszeitpunkt.
    Verwendet streng die Formeln aus dem Skript.

    :param eph: Ephemeridendaten eines einzelnen Satelliten ODER mehrerer
        Satelliten gleichzeitig (mit Dimension 'sv'). Im zweiten Fall werden
        alle Rueckgabewerte als Arrays (einer je Satellit) geliefert.
    :param t_eval: Auswertungszeitpunkt (als np.datetime64)
    :return: x, y, z (ECEF-Koordinaten in m),
             dt_sat (Uhrenkorrektur in s)
    """
    epoche_zeit = eph.time.values
    tk = hf.korrigiere_zeit(t_eval, epoche_zeit)

    xk_prime, yk_prime, ik, Ek = hf.berechne_orbit_ebene(eph, tk)

    # Hinweis: bewusst kein float(...), damit die Funktion sowohl fuer einen
    # einzelnen Satelliten (Aufgabenblock 3) als auch vektorisiert fuer
    # mehrere gleichzeitig sichtbare Satelliten (Aufgabenblock 4/5) nutzbar ist.
    omega0 = eph['Omega0'].values
    omega_dot = eph['OmegaDot'].values
    toe_sekunden = eph['Toe'].values

    omega_k = omega0 + (omega_dot - hf.OMEGA_E_DOT) * tk - hf.OMEGA_E_DOT * toe_sekunden

    x = xk_prime * np.cos(omega_k) - yk_prime * np.cos(ik) * np.sin(omega_k)
    y = xk_prime * np.sin(omega_k) + yk_prime * np.cos(ik) * np.cos(omega_k)
    z = yk_prime * np.sin(ik)

    # dt_clock entspricht tk (identische Zeitdifferenz zur Referenzepoche)
    dt_clock = tk

    af0 = eph['SVclockBias'].values
    af1 = eph['SVclockDrift'].values
    af2 = eph['SVclockDriftRate'].values

    sqrt_a = eph['sqrtA'].values
    e = eph['Eccentricity'].values

    rel_korrektur = hf.F * e * sqrt_a * np.sin(Ek)

    dt_sat = af0 + af1 * dt_clock + af2 * dt_clock * dt_clock + rel_korrektur

    return x, y, z, dt_sat