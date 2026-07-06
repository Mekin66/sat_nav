import numpy as np
import Orbit.orbit_basis as hf

def berechne_ecef_und_uhr(eph, t_eval):
    """
    Berechnet die Position des Satelliten im ECEF-Koordinatensystem sowie
    die Uhrenkorrektur zu einem bestimmten Auswertungszeitpunkt.
    Verwendet streng die Formeln aus dem Skript.

    :param eph: Ephemeridendaten des zu berechnenden Satelliten
    :param t_eval: Auswertungszeitpunkt (als np.datetime64)
    :return: x, y, z (ECEF-Koordinaten in m),
             dt_sat (Uhrenkorrektur in s)
    """
    epoche_zeit = eph.time.values
    tk = hf.korrigiere_zeit(t_eval, epoche_zeit)

    xk_prime, yk_prime, ik, Ek = hf.berechne_orbit_ebene(eph, tk)

    omega0 = float(eph['Omega0'].values)
    omega_dot = float(eph['OmegaDot'].values)

    toe_sekunden = float(eph['Toe'].values)

    omega_k = omega0 + (omega_dot - hf.OMEGA_E_DOT) * tk - hf.OMEGA_E_DOT * toe_sekunden

    x = xk_prime * np.cos(omega_k) - yk_prime * np.cos(ik) * np.sin(omega_k)
    y = xk_prime * np.sin(omega_k) + yk_prime * np.cos(ik) * np.cos(omega_k)
    z = yk_prime * np.sin(ik)

    dt_clock = hf.korrigiere_zeit(t_eval, epoche_zeit)

    af0 = float(eph['SVclockBias'].values)
    af1 = float(eph['SVclockDrift'].values)
    af2 = float(eph['SVclockDriftRate'].values)

    sqrt_a = float(eph['sqrtA'].values)
    e = float(eph['Eccentricity'].values)

    rel_korrektur = hf.F * e * sqrt_a * np.sin(Ek)

    dt_sat = af0 + af1 * dt_clock + af2 * dt_clock * dt_clock + rel_korrektur

    return x, y, z, dt_sat