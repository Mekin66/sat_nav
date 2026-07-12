import numpy as np
import folium

from Orbit.orbit_d import berechne_ecef_und_uhr
from Positionsbestimmung.nutzerposition_a import berechne_nutzerposition, c
from Positionsbestimmung.convert_ecef import ecef_to_wgs84


def _gueltige_nav_daten(data_nav, gps_svs):
    """
    Baut fuer jeden GPS-Satelliten einen auf gueltige (nicht-NaN) Toe-Eintraege
    reduzierten Navigationsdatensatz auf. Dies ist noetig, da der Zeit-Index
    der Navigationsdatei ein gemeinsamer Raster ueber alle Satelliten ist -
    nicht jeder Satellit hat an jedem Zeitpunkt dieses Rasters eine gueltige
    Ephemeride uebertragen.

    :param data_nav: Navigationsdaten (georinex Dataset einer Nav-Datei)
    :param gps_svs: Liste/Array der zu beruecksichtigenden GPS-SV-Kennungen
    :return: dict {sv_name: Dataset mit nur gueltigen Zeitpunkten}
    """
    nav_je_sv = {}
    for sv in gps_svs:
        sv_name = str(sv)
        sat_nav = data_nav.sel(sv=sv_name)
        gueltig = ~np.isnan(sat_nav['Toe'].values)
        if gueltig.any():
            nav_je_sv[sv_name] = sat_nav.isel(time=gueltig)
    return nav_je_sv


def berechne_trajektorie(data_obs, data_nav, pseudorange_fn=None, min_satelliten=4):
    """
    Berechnet fuer jede Epoche der Beobachtungsdaten die Nutzerposition im
    ECEF-Koordinatensystem per Multilateration (Newton-Verfahren).

    Es werden ausschliesslich GPS-Satelliten (SV-Kennung 'G') beruecksichtigt:
    Abschnitt 4 der Aufgabenstellung schreibt dies explizit vor, und nur fuer
    GPS liefert Aufgabenblock 3 die passenden Kepler-Bahnelemente - andere
    Systeme wie GLONASS uebertragen ihre Ephemeriden in einem anderen
    (kartesischen) Format.

    :param data_obs: Beobachtungsdaten (georinex Dataset einer Obs-Datei)
    :param data_nav: Navigationsdaten (georinex Dataset einer Nav-Datei)
    :param pseudorange_fn: Optionale Funktion(epoche) -> Pseudorange-Array
        fuer alle GPS-Satelliten einer Epoche. Wird genutzt, um z.B. die
        ionosphaerenfreie Korrektur aus Aufgabenblock 5 einzubringen.
        Standardmaessig wird die rohe C1C-Pseudorange verwendet.
    :param min_satelliten: Mindestanzahl gueltiger Pseudoranges pro Epoche
        (4 Unbekannte: x, y, z, Uhrenfehler)
    :return: (positionen, zeiten) - Nx3-Array der ECEF-Positionen und die
        zugehoerigen Zeitstempel; Epochen ohne ausreichend Satelliten werden
        uebersprungen.
    """
    gps_maske = np.array([str(sv).startswith('G') for sv in data_obs.sv.values])
    gps_svs = data_obs.sv.values[gps_maske]
    nav_je_sv = _gueltige_nav_daten(data_nav, gps_svs)

    positionen = []
    zeiten = []

    for t in data_obs.time.values:
        epoche = data_obs.sel(sv=gps_svs, time=t)

        if pseudorange_fn is not None:
            pr_epoche = pseudorange_fn(epoche)
        else:
            pr_epoche = epoche['C1C'].values

        # Nur Satelliten beruecksichtigen, die sowohl eine gueltige
        # Pseudorange als auch Navigationsdaten besitzen.
        sichtbare_svs = [
            sv for sv, pr in zip(gps_svs, pr_epoche)
            if not np.isnan(pr) and str(sv) in nav_je_sv
        ]
        pr_gueltig = np.array([
            pr for sv, pr in zip(gps_svs, pr_epoche)
            if not np.isnan(pr) and str(sv) in nav_je_sv
        ])

        if len(sichtbare_svs) < min_satelliten:
            continue

        sat_pos = np.zeros((len(sichtbare_svs), 3))
        sat_dt = np.zeros(len(sichtbare_svs))
        for i, sv in enumerate(sichtbare_svs):
            eph = nav_je_sv[str(sv)].sel(time=t, method='nearest')
            laufzeit_s = pr_gueltig[i] / c
            laufzeit_td = (laufzeit_s * 1e9).astype('timedelta64[ns]')
            x, y, z, dt_sat = berechne_ecef_und_uhr(eph, t-laufzeit_td)
            sat_pos[i] = (x, y, z)
            sat_dt[i] = dt_sat

        pos_ecef = berechne_nutzerposition(pr_gueltig, sat_pos, sat_dt)

        positionen.append(pos_ecef)
        zeiten.append(t)

    return np.array(positionen), np.array(zeiten)


def karte_erstellen(positionen_ecef, dateiname):
    """
    Wandelt ECEF-Positionen nach WGS84 um und stellt sie als Linienzug auf
    einer interaktiven Karte (Leaflet/folium) dar, um sie visuell zu
    verifizieren.

    :param positionen_ecef: Nx3-Array der ECEF-Positionen
    :param dateiname: Zieldatei der HTML-Karte
    :return: None
    """
    if len(positionen_ecef) == 0:
        print("Keine Daten zur Visualisierung vorhanden.")
        return

    wgs84_koordinaten = [ecef_to_wgs84(*p)[:2] for p in positionen_ecef]

    m = folium.Map(location=wgs84_koordinaten[0], zoom_start=17)
    folium.PolyLine(wgs84_koordinaten, color="blue", weight=3, opacity=0.8).add_to(m)
    m.save(dateiname)
    print(f"Karte erfolgreich als '{dateiname}' gespeichert.")
