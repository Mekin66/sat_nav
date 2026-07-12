import numpy as np
import pandas as pd

from Orbit.orbit_basis import OMEGA_E_DOT

c = 299792458.0  # Lichtgeschwindigkeit in m/s

# Zu nutzende Systeme neben GPS ('G'): Galileo ('E') sendet wie GPS
# Kepler-Bahnelemente im Navigationsdatensatz, sodass Orbit.orbit_d ohne
# Anpassung auch fuer Galileo-Satelliten die ECEF-Position liefert. BeiDou
# ('C') nutzt dieselben Kepler-Bahnelemente (die hier beruecksichtigten
# MEO/IGSO-Satelliten, keine GEO-Sonderfaelle), sendet seine Ephemeriden
# aber in BeiDou-Zeit (BDT). GPST ist BDT konstant um 14s voraus, deshalb
# wird dieser Offset unten vor der Bahnberechnung fuer 'C'-Satelliten
# herausgerechnet. GLONASS ('R') wird weiterhin nicht beruecksichtigt, da
# es seine Ephemeriden in einem anderen (kartesischen) Format ueberraegt.
SYSTEME = ('G', 'E')
mapping = {'G':'C1C','E':'C1C','C':'C1P'}

# GPST liegt konstant 14s vor BDT (BeiDou Time) - siehe ICD-BDS.
BDT_GPST_OFFSET = np.timedelta64(14, 's')


def _gueltige_nav_daten(data_nav, svs):
    """
    Baut fuer jeden Satelliten einen auf gueltige (nicht-NaN) Toe-Eintraege
    reduzierten Navigationsdatensatz auf (siehe
    Positionsbestimmung.trajektorie._gueltige_nav_daten).

    :param data_nav: Navigationsdaten (georinex Dataset einer Nav-Datei)
    :param svs: Liste/Array der zu beruecksichtigenden SV-Kennungen
    :return: dict {sv_name: Dataset mit nur gueltigen Zeitpunkten}
    """
    nav_je_sv = {}
    for sv in svs:
        sv_name = str(sv)
        sat_nav = data_nav.sel(sv=sv_name)
        gueltig = ~np.isnan(sat_nav['Toe'].values)
        if gueltig.any():
            nav_je_sv[sv_name] = sat_nav.isel(time=gueltig)
    return nav_je_sv


def berechne_nutzerposition_mehrsysteme(pr, sat_pos, sat_dt, system_ids):
    """
    Multilateration mit zusaetzlicher Inter-System-Bias-Schaetzung (Abschnitt
    5, Aufgabe a: Nutzung zusaetzlicher Satellitensysteme).

    GPS und Galileo fuehren ihre eigene Systemzeit, die nicht exakt
    synchronisiert ist; zudem verarbeitet der Empfaenger beide Signale ueber
    leicht unterschiedliche Hardware-Pfade. Neben Position (x, y, z) und dem
    GPS-bezogenen Empfaengeruhrenfehler wird deshalb je zusaetzlichem System
    ein Inter-System-Bias (ISB) als weitere Unbekannte mitgeschaetzt, anstatt
    wie in Abschnitt 4 nur GPS-Satelliten zu verwenden.

    :param pr: Array der gemessenen Pseudoranges (m), N Satelliten
    :param sat_pos: Nx3-Array der Satellitenpositionen im ECEF (m)
    :param sat_dt: Array der Satellitenuhrenkorrekturen (s), N Werte
    :param system_ids: Array der Systemkennung je Satellit (0 = GPS als
        Referenzsystem, 1..k = zusaetzliche Systeme mit eigenem ISB)
    :return: Geschaetzte Nutzerposition im ECEF (3,) in Metern
    """
    system_ids = np.asarray(system_ids)
    anzahl_zusatzsysteme = int(system_ids.max()) if len(system_ids) else 0
    n_unbekannte = 4 + anzahl_zusatzsysteme

    x = np.zeros(n_unbekannte)

    for _ in range(15):
        dist = np.linalg.norm(sat_pos - x[:3], axis=1)
        isb = np.zeros(len(pr))
        for s in range(1, anzahl_zusatzsysteme + 1):
            isb[system_ids == s] = x[3 + s]

        pr_modell = dist + x[3] - c * sat_dt + isb

        dp = pr - pr_modell

        H = np.zeros((len(pr), n_unbekannte))
        for i in range(len(pr)):
            H[i, :3] = -(sat_pos[i] - x[:3]) / dist[i]
            H[i, 3] = 1.0
            if system_ids[i] > 0:
                H[i, 3 + system_ids[i]] = 1.0

        dx = np.linalg.lstsq(H, dp, rcond=None)[0]

        x += dx

        if np.linalg.norm(dx[:3]) < 1e-4:
            break

    return x[:3]


def berechne_trajektorie_mehrsysteme(data_obs, data_nav, systeme=SYSTEME, min_satelliten = 4 + (len(SYSTEME) - 1)):
    """
    Berechnet fuer jede Epoche der Beobachtungsdaten die Nutzerposition im
    ECEF-Koordinatensystem per Multilateration, wobei zusaetzlich zu GPS
    weitere Satellitensysteme (Abschnitt 5, Aufgabe a) genutzt werden.

    Durch die zusaetzlichen Satelliten steigt die Anzahl gleichzeitig
    sichtbarer Satelliten und verbessert typischerweise die raeumliche
    Verteilung (Geometrie) der Messung, wodurch die Cramer-Rao-Lower-Bound
    fuer die Varianz der Positionsschaetzung sinkt.

    :param data_obs: Beobachtungsdaten (georinex Dataset einer Obs-Datei)
    :param data_nav: Navigationsdaten (georinex Dataset einer Nav-Datei)
    :param systeme: Tupel der zu nutzenden SV-Systembuchstaben, das erste
        Element ist das Referenzsystem (GPS) ohne eigenen ISB
    :param min_satelliten: Mindestanzahl gueltiger Pseudoranges pro Epoche
        (4 + ein ISB pro zusaetzlichem System)
    :return: (positionen, zeiten) - Nx3-Array der ECEF-Positionen und die
        zugehoerigen Zeitstempel; Epochen ohne ausreichend Satelliten aus
        allen Systemen werden uebersprungen.
    """
    from Orbit.orbit_d import berechne_ecef_und_uhr

    system_index = {sys_letter: i for i, sys_letter in enumerate(systeme)}
    maske = np.array([str(sv)[0] in system_index for sv in data_obs.sv.values])
    svs = data_obs.sv.values[maske]
    nav_je_sv = _gueltige_nav_daten(data_nav, svs)

    positionen = []
    zeiten = []

    for t in data_obs.time.values:
        epoche = data_obs.sel(sv=svs, time=t)
        sichtbare_svs = []
        pr_gueltig = []

        for sv in svs:
            sv_str = str(sv)
            if sv_str not in nav_je_sv:
                continue

            # Signaltyp (z.B. 'C1C' oder 'C1P') anhand des Systembuchstabens ermitteln
            obs_typ = mapping.get(sv_str[0])

            # Prüfen, ob der Typ im Mapping existiert und in der Epoche gemessen wurde
            if not obs_typ or obs_typ not in epoche.data_vars:
                continue

            # Pseudorange für genau diesen Satelliten und Signaltyp auslesen
            pr = float(epoche[obs_typ].sel(sv=sv).values)

            if not np.isnan(pr):
                sichtbare_svs.append(sv)
                pr_gueltig.append(pr)

        pr_gueltig = np.array(pr_gueltig)

        # Ohne mindestens einen GPS-Satelliten als Referenzsystem ist der
        # Inter-System-Bias der zusaetzlichen Systeme nicht vom
        # Empfaengeruhrenfehler zu trennen.
        hat_referenzsystem = any(str(sv).startswith(systeme[0]) for sv in sichtbare_svs)

        if len(sichtbare_svs) < min_satelliten or not hat_referenzsystem:
            continue

        sat_pos = np.zeros((len(sichtbare_svs), 3))
        sat_dt = np.zeros(len(sichtbare_svs))
        system_ids = np.zeros(len(sichtbare_svs), dtype=int)
        for i, sv in enumerate(sichtbare_svs):
            eph = nav_je_sv[str(sv)].sel(time=t, method='nearest')
            laufzeit_s = pr_gueltig[i] / c
            laufzeit_td = (laufzeit_s * 1e9).astype('timedelta64[ns]')
            t_sende = t - laufzeit_td
            if str(sv).startswith('C'):
                # BeiDou-Ephemeriden liegen in BDT vor, t_sende hier noch in
                # GPST - Offset herausrechnen (siehe BDT_GPST_OFFSET oben).
                t_sende = t_sende - BDT_GPST_OFFSET

            x, y, z, dt_sat = berechne_ecef_und_uhr(eph, t_sende)

            # Erdrotation waehrend der individuellen Signallaufzeit
            # (Sagnac-Korrektur), analog zu Positionsbestimmung.trajektorie.
            theta = OMEGA_E_DOT * laufzeit_s
            x_korr = x * np.cos(theta) + y * np.sin(theta)
            y_korr = -x * np.sin(theta) + y * np.cos(theta)

            sat_pos[i] = (x_korr, y_korr, z)
            sat_dt[i] = dt_sat
            system_ids[i] = system_index[str(sv)[0]]

        pos_ecef = berechne_nutzerposition_mehrsysteme(pr_gueltig, sat_pos, sat_dt, system_ids)
        positionen.append(pos_ecef)
        zeiten.append(t)

    return np.array(positionen), np.array(zeiten)

def glaette_trajektorie(positionen, fenstergroesse=5):
    """
    Glaettet eine ECEF-Trajektorie epochenweise mit einem zentrierten
    gleitenden Mittelwert, um einzelne Epochen mit Ausreissern (z.B. durch
    ungueustige Satellitengeometrie oder Mehrwegeffekte) zu daempfen, sodass
    sich die Position von einem Zeitschritt zum naechsten weniger stark
    aendert.

    Am Rand der Trajektorie (erste/letzte fenstergroesse//2 Epochen) wird
    ueber die jeweils verfuegbaren Nachbarepochen gemittelt, statt die
    Randwerte durch fehlende Nachbarn kuenstlich zu daempfen.

    :param positionen: Nx3-Array der ECEF-Positionen (chronologisch sortiert)
    :param fenstergroesse: Anzahl der Epochen im gleitenden Fenster
    :return: Nx3-Array der geglaetteten ECEF-Positionen (gleiche Laenge)
    """
    if len(positionen) == 0:
        return positionen

    df = pd.DataFrame(positionen, columns=["x", "y", "z"])
    geglaettet = df.rolling(window=fenstergroesse, center=True, min_periods=1).mean()
    return geglaettet.to_numpy()