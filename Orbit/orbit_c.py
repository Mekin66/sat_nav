import numpy as np


def filtere_nav_satellit(data_nav):
    """
    Filtert einen Satelliten heraus, der ueber gueltige Daten verfuegt,
    und berechnet die Zeitabstaende der aufeinanderfolgenden
    Navigationsnachrichten.

    :param data_nav: Navigationsdatei
    :return: eph (erste gueltige Ephemeride des Satelliten),
             first_sat (String mit dem Namen des Satelliten)
    """
    gueltige_eintraege = data_nav['Toe'].count(dim='time')
    sats_mit_daten = gueltige_eintraege.where(gueltige_eintraege > 0, drop=True).sv.values
    first_sat = str(sats_mit_daten[0])

    nav_sat_data = data_nav.sel(sv=first_sat)
    print("Gewaehlte Navigationsnachrichten: " + first_sat)

    toe_values = nav_sat_data['Toe'].values
    valid_toe_values = toe_values[~np.isnan(toe_values)]

    abstaende_sekunden = []
    i = 0
    n = len(valid_toe_values) - 1

    while i < n:
        diff = valid_toe_values[i + 1] - valid_toe_values[i]
        abstaende_sekunden.append(diff)
        i = i + 1

    print("Die Navigationsnachrichten fuer " + first_sat + " liegen in folgenden Abstaenden vor:")
    print(str(abstaende_sekunden) + " Sekunden")

    valid_indices = np.where(~np.isnan(toe_values))[0]
    first_valid_idx = valid_indices[0]

    eph = nav_sat_data.isel(time=first_valid_idx)

    return eph, first_sat