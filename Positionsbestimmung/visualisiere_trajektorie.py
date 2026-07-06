import folium
import numpy as np
from Positionsbestimmung.nutzerposition_a import berechne_nutzerposition
from Positionsbestimmung.convert_ecef import ecef_to_wgs84
from Orbit.orbit_d import berechne_ecef_und_uhr  # Wichtig: Import hinzufügen


def visualisiere_trajektorie(data_obs, data_nav):
    wgs84_koordinaten = []

    # Beobachtungsdaten extrahieren
    pr_all = data_obs['C1C'].values
    zeiten = data_obs['time'].values

    for i in range(len(zeiten)):
        aktuelle_zeit = zeiten[i]
        pr_epoche = pr_all[i]

        # Ungültige Messungen (NaN) der aktuellen Epoche herausfiltern
        gueltige_idx = ~np.isnan(pr_epoche)
        pr_gueltig = pr_epoche[gueltige_idx]

        # Mindestens 4 Beobachtungen für 4 Unbekannte (X, Y, Z, dt) notwendig
        if len(pr_gueltig) < 4:
            continue

        # Fehlende Satellitenpositionen und -uhren für diese Epoche berechnen
        # (Hinweis: Passen Sie die Parameter von berechne_ecef_und_uhr an Ihre Implementierung an,
        # idealerweise so, dass nur die Positionen der 'gueltige_idx' berechnet werden)
        sichtbare_svs = data_obs['sv'].values[gueltige_idx]

        # 2. Ephemeriden für exakt diese Satelliten und die nächstgelegene Zeit extrahieren
        aktuelle_eph = data_nav.sel(sv=sichtbare_svs, time=aktuelle_zeit, method='nearest')

        # 3. Den reduzierten, sauberen Datensatz übergeben
        sat_pos, sat_dt = berechne_ecef_und_uhr(aktuelle_eph, aktuelle_zeit)


        # Nutzerposition ausgleichen
        pos_ecef = berechne_nutzerposition(pr_gueltig, sat_pos, sat_dt)

        # In WGS84 transformieren und speichern
        lat, lon, alt = ecef_to_wgs84(*pos_ecef)
        wgs84_koordinaten.append((lat, lon))

    if not wgs84_koordinaten:
        print("Keine Daten zur Visualisierung vorhanden.")
        return

    # Karte generieren
    m = folium.Map(location=wgs84_koordinaten[0], zoom_start=17)
    folium.PolyLine(wgs84_koordinaten, color="blue", weight=3, opacity=0.8).add_to(m)
    m.save("dynamische_trajektorie.html")
    print("Karte erfolgreich als 'dynamische_trajektorie.html' gespeichert.")