import numpy as np
import matplotlib.pyplot as plt


def vergleiche_doppler(data_stat, data_dyn):
    """
    Findet Satelliten, die in Beiden Messungen vorkommen und Plottet sie ins selbe koordinatensystem
    Die Plotzeit wird auf die der Kürzeren statischen messung begrent

    :param data_stat:
    :param data_dyn:
    :return:
    """
    def get_valid_sats(ds):
        counts = ds['D1C'].count(dim='time')
        valid_svs = counts.where(counts > 0, drop=True).sv.values
        return set(valid_svs.astype(str))

    sats_stat = get_valid_sats(data_stat)
    sats_dyn = get_valid_sats(data_dyn)
    gemeinsame = sorted(list(sats_stat.intersection(sats_dyn)))

    if not gemeinsame:
        print("Abbruch: Keine gemeinsamen Satelliten gefunden.")
        return

    ziel_sat = gemeinsame[0]
    print(f"Erzwinge Plot für Satellit: {ziel_sat}")

    # 2. Daten extrahieren und NaN entfernen
    s_stat = data_stat.sel(sv=ziel_sat).dropna(dim='time', subset=['D1C'])
    s_dyn = data_dyn.sel(sv=ziel_sat).dropna(dim='time', subset=['D1C'])

    # 3. Rohe Arrays ziehen (löst alle xarray-Datumsprobleme auf einen Schlag)
    t_stat_raw = s_stat.time.values
    t_dyn_raw = s_dyn.time.values
    val_stat = s_stat['D1C'].values
    val_dyn = s_dyn['D1C'].values

    # 4. In Sekunden ab Messbeginn umwandeln
    t_stat_sec = (t_stat_raw - t_stat_raw[0]) / np.timedelta64(1, 's')
    t_dyn_sec = (t_dyn_raw - t_dyn_raw[0]) / np.timedelta64(1, 's')

    # 5. Dynamische Daten hart abschneiden (auf Dauer der statischen)
    dauer_statisch = t_stat_sec[-1]  # Die Gesamtdauer in Sekunden

    # Maske: Behalte nur dynamische Punkte, deren Zeit <= dauer_statisch ist
    mask_dyn = t_dyn_sec <= dauer_statisch

    t_dyn_plot = t_dyn_sec[mask_dyn]
    val_dyn_plot = val_dyn[mask_dyn]

    # 6. Plotten!
    plt.figure(figsize=(12, 6))

    plt.plot(t_stat_sec, val_stat,
             label=f'Statisch (Dauer: {dauer_statisch:.1f} s)',
             color='blue')

    plt.plot(t_dyn_plot, val_dyn_plot,
             label='Dynamisch (relativ & auf statische Dauer gekappt)',
             color='orange')

    plt.title(f"Dopplerfrequenz relativ zum Messbeginn (Satellit {ziel_sat})", fontweight='bold')
    plt.xlabel("Vergangene Zeit seit Messbeginn [s]")
    plt.ylabel("Dopplerfrequenz [Hz]")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()