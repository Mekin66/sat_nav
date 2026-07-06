import matplotlib.pyplot as plt

def plot_gps_l1(data):
    """
    This function is plotting the Pseudorange,  Dopplerfrequenz and the development of the Signalquality

    :param data:
    :return:
    """
    # Alle GPS-Satelliten herausfiltern
    satellites = data.sv.to_numpy().astype(str)
    gps_sats = [sat for sat in satellites if sat.startswith('G')]

    # 3 Sub-Plots untereinander erstellen
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("Aufgabe d) GPS L1 C/A-Signal", fontsize=14, fontweight='bold')

    times = data.time.to_numpy()

    for sat in gps_sats:
        sat_data = data.sel(sv=sat)
        # Plot 1: Pseudorange (C1C)
        axes[0].plot(times, sat_data['C1C'])
        # Plot 2: Doppler (D1C)
        axes[1].plot(times, sat_data['D1C'])
        # Plot 3: SNR / Signalstärke (S1C)
        axes[2].plot(times, sat_data['S1C'])

    # Achsenbeschriftung
    axes[0].set_ylabel("Pseudorange (m)")
    axes[1].set_ylabel("Dopplerfrequenz (Hz)")
    axes[2].set_ylabel("Signalstärke SNR (dBHz)")
    axes[2].set_xlabel("Zeit (UTC)")

    for ax in axes:
        ax.grid(True)

    plt.show()