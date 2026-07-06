import georinex as gr
from pathlib import Path
import warnings as w
import numpy as np


#Observablen
from Observation.observation_c import analyse_satellites
from Observation.observation_d import plot_gps_l1
from Observation.observation_e import vergleiche_galileo_e1_e5
from Observation.observation_f import vergleiche_traegerphase
from Observation.observation_g import vergleiche_doppler

#Satellitenorbits
from Orbit.orbit_basis import load_data as load_nav_data
from Orbit.orbit_c import filtere_nav_satellit
from Orbit.orbit_d import berechne_ecef_und_uhr
from Orbit.orbit_e import plot_24h_ecef
from Orbit.orbit_f import plot_24h_uhr
from Orbit.orbit_g import plot_24h_eci
from Positionsbestimmung.convert_ecef import ecef_to_enu, ecef_to_wgs84

#Postiotonsbestimmung
from Positionsbestimmung.nutzerposition_a import berechne_nutzerposition
from Positionsbestimmung.nutzerposition_a import c
from Positionsbestimmung.visualisiere_trajektorie import visualisiere_trajektorie

# 0. Dateipfad modern und betriebssystemunabhängig zusammensetzen
dateipfad = Path("Rohdateien")
dateiname_1 = "gnss_log_2026_04_21_15_34_15.26o"
dateiname_2 = "gnss_log_2026_04_21_16_03_28.26o"
kompletter_pfad_1 = dateipfad / dateiname_1
kompletter_pfad_2 = dateipfad / dateiname_2

dateiname_nav = "TIT200DEU_R_20261110000_01D_MN.rnx.gz"
kompletter_pfad_nav = dateipfad / dateiname_nav

# Unterdrücke Warnings beim aufruf von data in der Commandozeile
w.filterwarnings("ignore", category=FutureWarning)

# Datei einlesen
data = gr.load(kompletter_pfad_1)
data_nav = load_nav_data(kompletter_pfad_nav)

###
# Observation
###
print("\n=== Alter Versuch: Aufgabe c ===")
# analyse_satellites(data)

print("\n=== Alter Versuch: Aufgabe d ===")
# plot_gps_l1(data)

print("\n=== Alter Versuch: Aufgabe e ===")
# vergleiche_galileo_e1_e5(data)

print("\n=== Alter Versuch: Aufgabe f ===")
# vergleiche_traegerphase(data)

print("\n=== Alter Versuch: Aufgabe g ===")
# data_2 = gr.load(kompletter_pfad_2)
# vergleiche_doppler(data, data_2)


###
# Satellitenorbits
###
"""
print("\n=== Aufgabe c ===")
eph, sat_name = filtere_nav_satellit(data_nav)

start_zeit = eph.time.values
print("Startzeitpunkt fuer Berechnungen: " + str(start_zeit))

print("\n=== Aufgabe d ===")
x, y, z, dt_sat = berechne_ecef_und_uhr(eph, start_zeit)
print("Position ECEF X (m): " + str(float(x)))
print("Position ECEF Y (m): " + str(float(y)))
print("Position ECEF Z (m): " + str(float(z)))
print("Uhrenkorrektur (s):  " + str(float(dt_sat)))

print("\n=== Aufgabe e ===")
print("Erstelle ECEF-Plot...")
plot_24h_ecef(eph, start_zeit)

print("\n=== Aufgabe f ===")
print("Erstelle Plot der Uhrenkorrektur...")
plot_24h_uhr(eph, start_zeit)

print("\n=== Aufgabe g ===")
print("Erstelle ECI-Plot...")
plot_24h_eci(eph, start_zeit)
"""
###
# Positionsbestimmung
###
print("\n=== Aufgabe a & b: Synthetischer Test Newton-Verfahren ===")
sat_pos_test = np.array([[20000000, 0, 0], [0, 20000000, 0], [0, 0, 20000000], [15000000, 15000000, 15000000]])
nutzer_echt = np.array([6371000.0, 0.0, 0.0])
sat_dt_test = np.array([1e-5, -2e-5, 3e-5, 0.0])
uhr_nutzer_echt = 1.5e-6

wahre_distanzen = np.linalg.norm(sat_pos_test - nutzer_echt, axis=1)
pr_test = wahre_distanzen + c * uhr_nutzer_echt - c * sat_dt_test

# Funktion testen
pos_calc = berechne_nutzerposition(pr_test, sat_pos_test, sat_dt_test)
fehler_m = np.linalg.norm(pos_calc - nutzer_echt)
print(f"Berechnete Position: {pos_calc}")
print(f"Synthetischer Fehler: {fehler_m:.4f} m (sollte 0 sein)")

print("\n=== Aufgabe c: ECEF zu WGS84 ===")
lat, lon, alt = ecef_to_wgs84(pos_calc[0], pos_calc[1], pos_calc[2])
print(f"WGS84 Koordinaten -> Breite: {lat:.4f}°, Laenge: {lon:.4f}°, Hoehe: {alt:.2f}m")

print("\n=== Aufgabe d: ECEF zu ENU & Standardabweichung ===")
# Wir erzeugen ein Array aus der errechneten Position und einem leicht abweichenden Punkt
pos_wolke = np.array([pos_calc, pos_calc + [10, -5, 2]])

enu_coords = ecef_to_enu(pos_wolke, pos_calc)
std_dev = np.std(enu_coords, axis=0)

print(f"ENU Koordinaten des abweichenden Punktes (East, North, Up):\n{enu_coords[1]}")
print(f"Standardabweichung (E, N, U): {std_dev}")

print("\n=== Aufgabe e: Berechne Position fuer dynamische Aufzeichnung ===")
visualisiere_trajektorie(data, data_nav)