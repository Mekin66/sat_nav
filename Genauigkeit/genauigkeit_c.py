import folium

from Positionsbestimmung.convert_ecef import ecef_to_wgs84


def vergleiche_dynamisch(pos_block4, pos_block5, dateiname="vergleich_dynamische_trajektorie.html"):
    """
    Aufgabe c): Stellt die dynamischen Trajektorien aus Abschnitt 4 (nur
    GPS, C1C) und Abschnitt 5 (GPS + Galileo, Mehrsystem-Loesung) gemeinsam
    auf einer Karte dar, um sie optisch zu vergleichen.

    :param pos_block4: Nx3 ECEF-Positionen der dynamischen Messung, Abschnitt 4
    :param pos_block5: Mx3 ECEF-Positionen der dynamischen Messung, Abschnitt 5
    :param dateiname: Zieldatei der HTML-Karte
    :return: None
    """
    wgs84_4 = [ecef_to_wgs84(*p)[:2] for p in pos_block4]
    wgs84_5 = [ecef_to_wgs84(*p)[:2] for p in pos_block5]

    if not wgs84_4 and not wgs84_5:
        print("Keine Daten zum Vergleich der dynamischen Trajektorien vorhanden.")
        return

    zentrum = wgs84_4[0] if wgs84_4 else wgs84_5[0]
    m = folium.Map(location=zentrum, zoom_start=17)

    if wgs84_4:
        folium.PolyLine(wgs84_4, color="blue", weight=3, opacity=0.8,
                         tooltip="Abschnitt 4 (nur GPS)").add_to(m)
    if wgs84_5:
        folium.PolyLine(wgs84_5, color="red", weight=3, opacity=0.8,
                         tooltip="Abschnitt 5 (GPS + Galileo + BEIdou)").add_to(m)

    m.save(dateiname)
    print(f"Aufgabe c) Vergleichskarte gespeichert als '{dateiname}'.")
