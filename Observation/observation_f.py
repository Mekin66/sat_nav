import matplotlib.pyplot as plt

def vergleiche_traegerphase(data):
    """
    Aufgabe f): Stellt fuer einen GPS-Satelliten die Pseudorange (C1C) und
    die Traegerphase (L1C) gemeinsam in einem Diagramm mit zwei Y-Achsen
    dar, um beide Beobachtungsgroessen visuell zu vergleichen.

    :param data: Beobachtungsdaten (georinex Dataset einer Obs-Datei)
    :return: None
    """
    # Wir nehmen den ersten GPS Satelliten
    satellites = data.sv.to_numpy().astype(str)
    ziel_sat = [sat for sat in satellites if sat.startswith('G')][0]

    sat_data = data.sel(sv=ziel_sat)
    times = data.time.to_numpy()

    fig, ax1 = plt.subplots(figsize=(10, 5))
    fig.suptitle(f"Aufgabe f) {ziel_sat}: Pseudorange vs Trägerphase", fontweight='bold')

    # Achse 1: Pseudorange (in Metern)
    color1 = 'tab:blue'
    ax1.set_xlabel('Zeit')
    ax1.set_ylabel('Pseudorange C1C (m)', color=color1)
    ax1.plot(times, sat_data['C1C'], color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    # Achse 2: Trägerphase (in Zyklen)
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Trägerphase L1C (Zyklen)', color=color2)
    ax2.plot(times, sat_data['L1C'], color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    #fig.tight_layout()
    plt.show()
