import numpy as np
from pathlib import Path
import georinex as gr
import pandas as pd

# Naturkonstanten
MU = 3.986005e14
OMEGA_E_DOT = 7.2921151467e-5
F = -4.442807633e-10
SEC_PER_WEEK = 604800


def load_data(pfad, sets):
    """
    Laedt die Navigationsdatei aus dem angegebenen Pfad ein.

    :param pfad: String oder Pfad-Objekt zur Navigationsdatei
    :return: Dataset mit den Navigationsdaten
    """
    print("lese_satelliten_aus")
    kompletter_pfad = Path(pfad)
    data = gr.load(kompletter_pfad, use=sets)
    return data


def korrigiere_zeit(t_eval, t_ref):
    """
    Berechnet die Zeitdifferenz in Sekunden und korrigiert den
    Wochenuebergang.

    :param t_eval: Auswertungszeitpunkt (als np.datetime64 oder Sekunden)
    :param t_ref: Referenzzeitpunkt der Ephemeride
    :return: Korrigierte Zeitdifferenz in Sekunden (Float)
    """
    t_eval_np = pd.to_datetime(t_eval).to_numpy()
    t_ref_np = pd.to_datetime(t_ref).to_numpy()

    # Differenz direkt in Sekunden berechnen
    dt = (t_eval_np - t_ref_np) / np.timedelta64(1, 's')

    # Vektorisierte Korrektur für den GNSS-Wochenwechsel
    dt = np.where(dt > 302400, dt - 604800, dt)
    dt = np.where(dt < -302400, dt + 604800, dt)

    return dt


def berechne_orbit_ebene(eph, tk):
    """
    Loest die Kepler-Gleichung und berechnet die 2D-Koordinaten in der
    Orbitalebene

    :param eph: Ephemeridendaten des jeweiligen Satelliten
    :param tk: Korrigierte Zeit seit der Referenzepoche (Toe) in Sekunden
    :return: xk_prime (X-Koordinate in der Bahnebene),
             yk_prime (Y-Koordinate in der Bahnebene),
             ik (Inklination),
             Ek (Exzentrische Anomalie)
    """
    sqrt_a = eph['sqrtA'].values
    A = sqrt_a * sqrt_a

    delta_n = eph['DeltaN'].values
    n0 = np.sqrt(MU / (A * A * A))
    n = n0 + delta_n

    m0 = eph['M0'].values
    Mk = m0 + n * tk

    e = eph['Eccentricity'].values

    # Kepler-Gleichung iterativ loesen. np.all(...) statt einem Skalarvergleich,
    # da eph auch mehrere Satelliten gleichzeitig enthalten kann (Aufgabenblock 4/5).
    Ek = Mk
    i = 0
    while i < 10:
        Ek_next = Mk + e * np.sin(Ek)
        diff = np.abs(Ek_next - Ek)
        Ek = Ek_next
        if np.all(diff < 1e-12):
            break
        i = i + 1

    nu_k = np.arctan2(np.sqrt(1 - (e * e)) * np.sin(Ek), np.cos(Ek) - e)
    omega = eph['omega'].values
    Phi_k = nu_k + omega

    cuc = eph['Cuc'].values
    cus = eph['Cus'].values
    crc = eph['Crc'].values
    crs = eph['Crs'].values
    cic = eph['Cic'].values
    cis = eph['Cis'].values

    # Gleichung (8)
    du_k = cus * np.sin(2 * Phi_k) + cuc * np.cos(2 * Phi_k)
    dr_k = crs * np.sin(2 * Phi_k) + crc * np.cos(2 * Phi_k)
    di_k = cis * np.sin(2 * Phi_k) + cic * np.cos(2 * Phi_k)

    # Gleichung (9), (10), (11)
    uk = Phi_k + du_k
    rk = A * (1 - e * np.cos(Ek)) + dr_k

    io_val = eph['Io'].values
    idot_val = eph['IDOT'].values
    ik = io_val + di_k + idot_val * tk

    # Gleichung (14)
    xk_prime = rk * np.cos(uk)
    yk_prime = rk * np.sin(uk)

    return xk_prime, yk_prime, ik, Ek