from Genauigkeit.mehrsysteme import berechne_trajektorie_mehrsysteme, SYSTEME, glaette_trajektorie
from Genauigkeit.genauigkeit_b import vergleiche_statistik
from Genauigkeit.genauigkeit_c import vergleiche_dynamisch
from Positionsbestimmung.trajektorie import karte_erstellen


def run(data_stat, data_dyn, data_nav, ergebnisse_block4):
    """
    Fuehrt alle Aufgaben aus Aufgabenblock 5 (Genauigkeit) aus.

    Als Verfahren zur Steigerung der Positionsgenauigkeit (Aufgabe a) wird
    die Nutzung zusaetzlicher Satellitensysteme genutzt: Neben GPS werden
    zusaetzlich Galileo-Satelliten in die Multilateration einbezogen, mit
    einem zusaetzlich geschaetzten Inter-System-Bias (ISB) zwischen GPS- und
    Galileo-Systemzeit (siehe Genauigkeit/mehrsysteme.py). Durch die groessere
    Anzahl gleichzeitig sichtbarer Satelliten verbessert sich die Geometrie
    der Messung und damit die Cramer-Rao-Lower-Bound der Positionsschaetzung.

    :param data_stat: Statische Beobachtungsdaten
    :param data_dyn: Dynamische Beobachtungsdaten
    :param data_nav: Navigationsdaten
    :param ergebnisse_block4: Rueckgabewert von
        Positionsbestimmung.position_main.run(...), enthaelt die
        Positionsschaetzungen aus Abschnitt 4 zum Vergleich
    :return: dict mit den Positionsschaetzungen aus Abschnitt 5
    """
    print(f"\n=== Aufgabe a: Nutzung zusaetzlicher Satellitensysteme ({'+'.join(SYSTEME)}) ===")
    pos_stat_5, zeit_stat_5 = berechne_trajektorie_mehrsysteme(data_stat, data_nav)
    pos_dyn_5, zeit_dyn_5 = berechne_trajektorie_mehrsysteme(data_dyn, data_nav)
    print(f"{len(pos_stat_5)} von {len(data_stat.time)} statischen Epochen erfolgreich berechnet (Abschnitt 5).")
    print(f"{len(pos_dyn_5)} von {len(data_dyn.time)} dynamischen Epochen erfolgreich berechnet (Abschnitt 5).")

    print("\n=== Aufgabe b: Vergleich statische Messung ===")
    vergleiche_statistik(ergebnisse_block4["pos_stat"], pos_stat_5)

    print("\n=== Aufgabe c: Vergleich dynamische Messung ===")
    vergleiche_dynamisch(ergebnisse_block4["pos_dyn"], pos_dyn_5)

    print("\n=== Zusatz: Geglaettete Mehrsystem-Trajektorie (dynamisch) ===")
    pos_dyn_5_geglaettet = glaette_trajektorie(pos_dyn_5)
    karte_erstellen(pos_dyn_5_geglaettet, "dynamische_trajektorie_mehrsysteme_geglaettet.html")

    print("\n=== Zusatz: Geglaettete Mehrsystem-Trajektorie (statisch) ===")
    pos_dyn_5_geglaettet = glaette_trajektorie(pos_stat_5)
    karte_erstellen(pos_dyn_5_geglaettet, "statische_trajektorie_mehrsysteme_geglaettet.html")

    return {
        "pos_stat": pos_stat_5,
        "zeit_stat": zeit_stat_5,
        "pos_dyn": pos_dyn_5,
        "zeit_dyn": zeit_dyn_5,
    }
