import numpy as np

def analyse_satellites(data):
    """
    This function is used to analyse the satellite data.
    It printes the  number of Satelites in each GNSS-System
    
    :param data: This is the Rinex-Data given. It contains the Infromation about our Satellites.
    :return: 
    """

    # 1. Satelliten-Namen modern abrufen und als Text sicherstellen
    satellites = data.sv.to_numpy().astype(str)

    # 2. Den ersten Buchstaben jedes Satelliten extrahieren
    system_letters = [sat[0] for sat in satellites]

    # 3. Die einzigartigen Systeme und ihre Häufigkeit zählen
    unique_systems, counts = np.unique(system_letters, return_counts=True)

    # 4. Ein kleines Lexikon (Dictionary) zur Übersetzung der Buchstaben
    system_names = {
        'G': 'GPS',
        'E': 'Galileo',
        'R': 'GLONASS',
        'C': 'BeiDou',
        'S': 'SBAS',
        'J': 'QZSS',
        'I': 'IRNSS'
    }

    # 5. Das Ergebnis übersichtlich ausgeben
    print("Aufgabe c) Anzahl der Satelliten pro System:")
    print("-" * 45)
    for sys_letter, count in zip(unique_systems, counts):
        name = system_names.get(sys_letter, f"Unbekanntes System ({sys_letter})")
        print(f"{name:<15} : {count} Satellit(en)")