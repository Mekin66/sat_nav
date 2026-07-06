import matplotlib.pyplot as plt
import numpy as np

def vergleiche_galileo_e1_e5(data):
    """
    Aufgabe e): Waehlt einen Galileo-Satelliten aus und plottet die
    Differenz der Pseudorange zwischen dem E1-Band (C1C) und dem E5-Band
    (C5Q), um den Effekt der Frequenzabhaengigkeit (u.a. Ionosphaere) zu
    veranschaulichen.

    :param data: Beobachtungsdaten (georinex Dataset einer Obs-Datei)
    :return: None
    """
    # Einen Galileo-Satelliten finden (z.B. den ersten)
    satellites = data.sv.to_numpy().astype(str)
    galileo_sats = [sat for sat in satellites if sat.startswith('E')]

    if not galileo_sats:
        print("Kein Galileo Satellit gefunden!")
        return

    ziel_sat = galileo_sats[0]
    print(f"Verwende Galileo-Satellit: {ziel_sat}")

    sat_data = data.sel(sv=ziel_sat)
    times = data.time.to_numpy()

    plt.figure(figsize=(10, 5))
    plt.title(f"Aufgabe e) {ziel_sat}: Pseudorange E1 vs E5")

    # E1 (meist C1C) und E5 (meist C5Q) plotten
    #plt.plot(times, sat_data['C1C'], label='E1 Band (C1C)')
    #plt.plot(times, sat_data['C5Q'], label='E5 Band (C5Q)')

    # Plotte Differenz
    plt.plot(times, (sat_data['C1C']-sat_data['C5Q']), label='Differenz')

    plt.ylabel("Pseudorange (m)")
    plt.xlabel("Zeit")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
