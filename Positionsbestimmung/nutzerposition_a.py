import numpy as np

c = 299792458.0  # Lichtgeschwindigkeit in m/s

def berechne_nutzerposition(pr, sat_pos, sat_dt):
    """
    Aufgabe a): Loest das nichtlineare Multilaterationsproblem (Abschnitt 4,
    Gl. 6/7) iterativ mit dem Newton-Verfahren und schaetzt so die
    ECEF-Nutzerposition sowie den Nutzeruhrenfehler aus einer Menge von
    Pseudorangemessungen.

    Abbruchkriterium: Die Iteration stoppt, sobald die Positionskorrektur
    |dx| < 1e-4 m betraegt (Konvergenz), spaetestens jedoch nach 15
    Iterationsschritten (Sicherheitsgrenze gegen Divergenz).

    :param pr: Array der gemessenen Pseudoranges (m), N Satelliten
    :param sat_pos: Nx3-Array der Satellitenpositionen im ECEF (m)
    :param sat_dt: Array der Satellitenuhrenkorrekturen (s), N Werte
    :return: Geschaetzte Nutzerposition im ECEF (3,) in Metern
    """
    x = np.array([0.0, 0.0, 0.0, 0.0])

    for _ in range(15):
        dist = np.linalg.norm(sat_pos - x[:3], axis=1)

        pr_modell = dist + x[3] - c * sat_dt

        dp = pr - pr_modell

        H = np.zeros((len(pr), 4))
        for i in range(len(pr)):
            H[i, :3] = -(sat_pos[i] - x[:3]) / dist[i]
            H[i, 3] = 1.0

        dx = np.linalg.lstsq(H, dp, rcond=None)[0]

        x += dx

        if np.linalg.norm(dx[:3]) < 1e-4:
            break

    return x[:3]
