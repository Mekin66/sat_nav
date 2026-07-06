from Orbit.orbit_c import filtere_nav_satellit
from Orbit.orbit_d import berechne_ecef_und_uhr
from Orbit.orbit_e import plot_24h_ecef
from Orbit.orbit_f import plot_24h_uhr
from Orbit.orbit_g import plot_24h_eci


def run(data_nav):
    """
    Fuehrt alle Aufgaben aus Aufgabenblock 3 (Satellitenorbits) fuer einen
    exemplarisch ausgewaehlten GPS-Satelliten aus.

    :param data_nav: Navigationsdaten
    :return: None
    """
    print("\n=== Aufgabe c: Auswahl eines Navigationssatelliten ===")
    eph, sat_name = filtere_nav_satellit(data_nav)
    start_zeit = eph.time.values
    print("Startzeitpunkt fuer Berechnungen: " + str(start_zeit))

    print("\n=== Aufgabe d: ECEF-Position & Uhrenkorrektur ===")
    x, y, z, dt_sat = berechne_ecef_und_uhr(eph, start_zeit)
    print("Position ECEF X (m): " + str(float(x)))
    print("Position ECEF Y (m): " + str(float(y)))
    print("Position ECEF Z (m): " + str(float(z)))
    print("Uhrenkorrektur (s):  " + str(float(dt_sat)))

    print("\n=== Aufgabe e: ECEF-Orbit ueber 24h ===")
    print("Erstelle ECEF-Plot...")
    plot_24h_ecef(eph, start_zeit)

    print("\n=== Aufgabe f: Uhrenkorrektur ueber 24h ===")
    print("Erstelle Plot der Uhrenkorrektur...")
    plot_24h_uhr(eph, start_zeit)

    print("\n=== Aufgabe g: ECI-Orbit ueber 24h ===")
    print("Erstelle ECI-Plot...")
    plot_24h_eci(eph, start_zeit)
