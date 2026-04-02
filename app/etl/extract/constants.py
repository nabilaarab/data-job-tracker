from typing import Dict

# Mapping ville/canton → regionId (commun aux deux plateformes)
JOBCLOUD__REGION_IDS: Dict[str, int] = {
    # Genève (6)
    "genève": 6, "geneve": 6, "geneva": 6, "ge": 6,
    # Vaud / Valais (10)
    "lausanne": 10, "vaud": 10, "vd": 10, "valais": 10,
    "vs": 10, "sion": 10, "montreux": 10,
    # Neuchâtel / Jura (8)
    "neuchâtel": 8, "neuchatel": 8, "ne": 8,
    "jura": 8, "ju": 8, "delémont": 8,
    # Fribourg (9)
    "fribourg": 9, "freiburg": 9, "fr": 9,
    # Berne (13)
    "bern": 13, "berne": 13, "be": 13,
    "biel": 13, "bienne": 13, "thun": 13,
    # Mittelland AG/SO (12)
    "aargau": 12, "argovie": 12, "ag": 12,
    "solothurn": 12, "soleure": 12, "so": 12, "aarau": 12,
    # Bâle (14)
    "basel": 14, "bâle": 14, "bs": 14, "bl": 14, "liestal": 14,
    # Suisse centrale (15)
    "luzern": 15, "lucerne": 15, "lu": 15,
    "zug": 15, "zoug": 15, "zg": 15,
    "schwyz": 15, "sz": 15, "uri": 15, "ur": 15,
    "obwalden": 15, "ow": 15, "nidwalden": 15, "nw": 15,
    # Zurich ville / Lac (19)
    "zürich": 19, "zurich": 19, "zh": 19,
    # Zurich Unterland / Limmattal (22)
    "dietikon": 22, "limmattal": 22,
    # Zurich Oberland (20)
    "uster": 20,
    # Winterthur / Schaffhausen (25)
    "winterthur": 25, "schaffhausen": 25, "schaffhouse": 25, "sh": 25,
    # St-Gall / Appenzell (21)
    "st. gallen": 21, "st gallen": 21, "saint-gall": 21,
    "sg": 21, "appenzell": 21, "ar": 21, "ai": 21,
    # Wil / Toggenburg (17)
    "wil": 17, "toggenburg": 17,
    # Thurgau / Lac de Constance (18)
    "thurgau": 18, "thurgovie": 18, "tg": 18,
    # Rheintal / FL / Sargans / Linth (23)
    "rheintal": 23, "liechtenstein": 23, "fl": 23, "sargans": 23,
    # Graubünden (24)
    "graubünden": 24, "grisons": 24, "gr": 24, "chur": 24, "coire": 24,
    # Oberwallis (16)
    "oberwallis": 16, "visp": 16, "brig": 16,
    # Tessin (4)
    "ticino": 4, "tessin": 4, "ti": 4,
    "lugano": 4, "locarno": 4, "bellinzona": 4,
    # Remote → Suisse romande par défaut
    "remote": 3,
}