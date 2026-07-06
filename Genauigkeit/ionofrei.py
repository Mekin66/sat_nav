import numpy as np

# GPS-Traegerfrequenzen (Hz)
F_L1 = 1575.42e6
F_L5 = 1176.45e6


def korrigiere_pseudorange_ionosphaerenfrei(pr_l1, pr_l5):
    """
    Bildet die ionosphaerenfreie Linearkombination zweier Pseudorange-
    Messungen auf unterschiedlichen Frequenzen (Abschnitt 5, Gl. 6).

    Da die ionosphaerische Laufzeitverzoegerung frequenzabhaengig ist
    (Delta I ~= 40.3 * TEC / f^2), lassen sich Pseudorangemessungen auf zwei
    Frequenzen so gewichtet kombinieren, dass sich der ionosphaerische Anteil
    naeherungsweise aufhebt:

        pr_if = (f1^2 * pr_l1 - f2^2 * pr_l5) / (f1^2 - f2^2)

    Ist fuer einen Satelliten keine L5-Messung vorhanden (NaN), wird auf die
    unkorrigierte L1-Pseudorange zurueckgefallen, damit der Satellit nicht
    vollstaendig aus der Positionsbestimmung herausfaellt.

    :param pr_l1: Pseudorange auf L1 (z.B. C1C), array-like
    :param pr_l5: Pseudorange auf L5 (z.B. C5Q), array-like (kann NaN enthalten)
    :return: Ionosphaerenfrei korrigierte (bzw. bei fehlender L5-Messung
        unkorrigierte) Pseudorange, gleiche Form wie die Eingaben
    """
    pr_l1 = np.asarray(pr_l1, dtype=float)
    pr_l5 = np.asarray(pr_l5, dtype=float)

    f1_sq = F_L1 ** 2
    f5_sq = F_L5 ** 2
    pr_ionosphaerenfrei = (f1_sq * pr_l1 - f5_sq * pr_l5) / (f1_sq - f5_sq)

    return np.where(np.isnan(pr_l5), pr_l1, pr_ionosphaerenfrei)


def pseudorange_ionosphaerenfrei(epoche):
    """
    Extrahiert C1C (L1) und C5Q (L5) einer Beobachtungsepoche und kombiniert
    sie ionosphaerenfrei. Zur Verwendung als `pseudorange_fn` in
    `Positionsbestimmung.trajektorie.berechne_trajektorie`.

    :param epoche: Beobachtungsdaten einer einzelnen Epoche (georinex Dataset,
        bereits auf die gewuenschten Satelliten eingeschraenkt)
    :return: Array der ionosphaerenfrei korrigierten Pseudoranges
    """
    return korrigiere_pseudorange_ionosphaerenfrei(epoche['C1C'].values, epoche['C5Q'].values)
