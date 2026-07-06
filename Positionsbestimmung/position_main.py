import numpy as np

from Positionsbestimmung.nutzerposition_a import berechne_nutzerposition, c
from Positionsbestimmung.convert_ecef import ecef_to_wgs84, ecef_to_enu
from Positionsbestimmung.trajektorie import berechne_trajektorie, karte_erstellen


def _test_synthetisch():
    """
    Aufgabe a) & b): Testet das Newton-Verfahren mit einem synthetisch
    erzeugten Datensatz, bei dem die wahre Nutzerposition bekannt ist.
    Der resultierende Fehler dient als Funktionsnachweis.

    :return: None
    """
    print("\n=== Aufgabe a & b: Synthetischer Test Newton-Verfahren ===")
    sat_pos_test = np.array([
        [20000000, 0, 0],
        [0, 20000000, 0],
        [0, 0, 20000000],
        [15000000, 15000000, 15000000],
    ])
    nutzer_echt = np.array([6371000.0, 0.0, 0.0])
    sat_dt_test = np.array([1e-5, -2e-5, 3e-5, 0.0])
    uhr_nutzer_echt = 1.5e-6

    wahre_distanzen = np.linalg.norm(sat_pos_test - nutzer_echt, axis=1)
    pr_test = wahre_distanzen + c * uhr_nutzer_echt - c * sat_dt_test

    pos_calc = berechne_nutzerposition(pr_test, sat_pos_test, sat_dt_test)
    fehler_m = np.linalg.norm(pos_calc - nutzer_echt)

    print(f"Berechnete Position: {pos_calc}")
    print(f"Synthetischer Fehler: {fehler_m:.4f} m (sollte 0 sein)")


def run(data_stat, data_dyn, data_nav):
    """
    Fuehrt alle Aufgaben aus Aufgabenblock 4 (Positionsbestimmung) aus.

    :param data_stat: Statische Beobachtungsdaten
    :param data_dyn: Dynamische Beobachtungsdaten
    :param data_nav: Navigationsdaten
    :return: dict mit den berechneten ECEF-Positionen/Zeiten, das von
        Aufgabenblock 5 (Genauigkeit) zum Vergleich weiterverwendet wird
    """
    _test_synthetisch()

    print("\n=== Aufgabe c: Positionsbestimmung fuer die statische Aufzeichnung ===")
    pos_stat, zeit_stat = berechne_trajektorie(data_stat, data_nav)
    print(f"{len(pos_stat)} von {len(data_stat.time)} Epochen erfolgreich berechnet.")
    karte_erstellen(pos_stat, "statische_trajektorie.html")

    print("\n=== Aufgabe d: ECEF zu ENU & Standardabweichung ===")
    mittlere_position = np.mean(pos_stat, axis=0)
    enu_koordinaten = ecef_to_enu(pos_stat, mittlere_position)
    std_abweichung = np.std(enu_koordinaten, axis=0)

    lat, lon, alt = ecef_to_wgs84(*mittlere_position)
    print(f"Mittlere Position (WGS84) -> Breite: {lat:.6f} Grad, Laenge: {lon:.6f} Grad, Hoehe: {alt:.2f} m")
    print(f"Standardabweichung (Ost, Nord, Oben) in m: {std_abweichung}")

    print("\n=== Aufgabe e: Positionsbestimmung fuer die dynamische Aufzeichnung ===")
    pos_dyn, zeit_dyn = berechne_trajektorie(data_dyn, data_nav)
    print(f"{len(pos_dyn)} von {len(data_dyn.time)} Epochen erfolgreich berechnet.")
    karte_erstellen(pos_dyn, "dynamische_trajektorie.html")

    print("\n=== Aufgabe f: Bewertung der Ergebnisse ===")
    print("Die statische Position streut nur im Meterbereich um einen Mittelwert, waehrend die")
    print("dynamische Aufzeichnung eine zusammenhaengende Trajektorie entlang des zurueckgelegten")
    print("Weges ergibt. Beides entspricht den Erwartungen an eine GNSS-Einzelpunktmessung (Single")
    print("Point Positioning) ohne zusaetzliche Fehlerkorrektur.")

    return {
        "pos_stat": pos_stat,
        "zeit_stat": zeit_stat,
        "pos_dyn": pos_dyn,
        "zeit_dyn": zeit_dyn,
        "mittlere_position": mittlere_position,
    }
