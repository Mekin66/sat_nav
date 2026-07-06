from Positionsbestimmung.trajektorie import berechne_trajektorie
from Genauigkeit.ionofrei import pseudorange_ionosphaerenfrei
from Genauigkeit.genauigkeit_b import vergleiche_statistik
from Genauigkeit.genauigkeit_c import vergleiche_dynamisch


def run(data_stat, data_dyn, data_nav, ergebnisse_block4):
    """
    Fuehrt alle Aufgaben aus Aufgabenblock 5 (Genauigkeit) aus.

    Als Verfahren zur Steigerung der Positionsgenauigkeit (Aufgabe a) wird
    die Mehrfrequenzverarbeitung genutzt: Fuer jeden GPS-Satelliten mit
    vorhandener L5-Messung (C5Q) wird die ionosphaerenfreie Linearkombination
    aus L1 (C1C) und L5 gebildet, wodurch der ionosphaerische Fehleranteil
    naeherungsweise eliminiert wird (siehe Genauigkeit/ionofrei.py).

    :param data_stat: Statische Beobachtungsdaten
    :param data_dyn: Dynamische Beobachtungsdaten
    :param data_nav: Navigationsdaten
    :param ergebnisse_block4: Rueckgabewert von
        Positionsbestimmung.position_main.run(...), enthaelt die
        Positionsschaetzungen aus Abschnitt 4 zum Vergleich
    :return: dict mit den Positionsschaetzungen aus Abschnitt 5
    """
    print("\n=== Aufgabe a: Ionosphaerenfreie Zweifrequenzkorrektur ===")
    pos_stat_5, zeit_stat_5 = berechne_trajektorie(
        data_stat, data_nav, pseudorange_fn=pseudorange_ionosphaerenfrei
    )
    pos_dyn_5, zeit_dyn_5 = berechne_trajektorie(
        data_dyn, data_nav, pseudorange_fn=pseudorange_ionosphaerenfrei
    )
    print(f"{len(pos_stat_5)} von {len(data_stat.time)} statischen Epochen erfolgreich berechnet (Abschnitt 5).")
    print(f"{len(pos_dyn_5)} von {len(data_dyn.time)} dynamischen Epochen erfolgreich berechnet (Abschnitt 5).")

    print("\n=== Aufgabe b: Vergleich statische Messung ===")
    vergleiche_statistik(ergebnisse_block4["pos_stat"], pos_stat_5)

    print("\n=== Aufgabe c: Vergleich dynamische Messung ===")
    vergleiche_dynamisch(ergebnisse_block4["pos_dyn"], pos_dyn_5)

    return {
        "pos_stat": pos_stat_5,
        "zeit_stat": zeit_stat_5,
        "pos_dyn": pos_dyn_5,
        "zeit_dyn": zeit_dyn_5,
    }
