import numpy as np


def vergleiche_statistik(pos_block4, pos_block5):
    """
    Aufgabe b): Vergleicht fuer die statische Messung Mittelwert und Varianz
    der Positionsschaetzungen aus Abschnitt 4 (nur C1C) und Abschnitt 5
    (ionosphaerenfrei korrigiert).

    :param pos_block4: Nx3 ECEF-Positionen der statischen Messung, Abschnitt 4
    :param pos_block5: Mx3 ECEF-Positionen der statischen Messung, Abschnitt 5
    :return: None (Ausgabe erfolgt auf der Konsole)
    """
    mittel_4 = np.mean(pos_block4, axis=0)
    mittel_5 = np.mean(pos_block5, axis=0)
    varianz_4 = np.var(pos_block4, axis=0)
    varianz_5 = np.var(pos_block5, axis=0)

    print("Aufgabe b) Vergleich statische Messung: Abschnitt 4 vs. Abschnitt 5")
    print("-" * 60)
    print(f"Mittelwert ECEF Abschnitt 4 (m):   {mittel_4}")
    print(f"Mittelwert ECEF Abschnitt 5 (m):   {mittel_5}")
    print(f"Varianz    ECEF Abschnitt 4 (m^2): {varianz_4}")
    print(f"Varianz    ECEF Abschnitt 5 (m^2): {varianz_5}")

    gesamtvarianz_4 = np.sum(varianz_4)
    gesamtvarianz_5 = np.sum(varianz_5)
    print(f"Summierte Varianz Abschnitt 4: {gesamtvarianz_4:.4f} m^2")
    print(f"Summierte Varianz Abschnitt 5: {gesamtvarianz_5:.4f} m^2")

    if gesamtvarianz_5 < gesamtvarianz_4:
        print("-> Die ionosphaerenfreie Korrektur verringert die Streuung der Positionsschaetzung.")
    else:
        print("-> Die ionosphaerenfreie Korrektur verringert die Streuung in diesem Datensatz nicht merklich.")
