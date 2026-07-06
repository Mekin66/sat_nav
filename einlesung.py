import georinex as gr
import numpy as np
import warnings as w
from pathlib import Path
import matplotlib.pyplot as plt

w.filterwarnings("ignore", category=FutureWarning)

def lese_satelliten_aus():
    """
    Liest die Navigationsdatei aus
    :return: Daten der NAvigationsdatei
    """
    print("lese_satelliten_aus")
    dateipfad = Path("Rohdateien")
    kompletter_pfad = dateipfad / "TIT200DEU_R_20261110000_01D_MN.rnx.gz"
    data = gr.load(kompletter_pfad)
    return data

def filter_satelliete(data):
    """
    Filtert den ersten Satelliten raus und gibt diesen zurück
    :param data:
    :return:
    """
    all_sats = data.sv.values
    first_sat = all_sats[0]
    sv_data = data.sel(sv=first_sat)
    print(f"Dynamisch gewählter Satellit: {first_sat}")

    # Zeitabstände der Navigationsnachrichten berechnen
    time_diffs = np.diff(sv_data['time'].values)
    time_diffs_hours = time_diffs.astype('timedelta64[s]').astype(float) / 3600

    print(f"Zeitabstände in Stunden: {time_diffs_hours}")


data = lese_satelliten_aus()
filter_satelliete(data)