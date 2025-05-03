import json
from datetime import date, timedelta

# pprint et OrderedDict permettent un affichage ordonné du fichier json
from pprint import pprint
from collections import OrderedDict

## emplacement du fichier
fichierJson = "/Users/philippepeter/Desktop/Python/etna_data.json"

## lecture du fichier json pour en récupérer le dictionnaire et l'afficher
with open(fichierJson, "r", encoding="utf-8") as fichier:
    etna = json.load(fichier, object_pairs_hook=OrderedDict)
    pprint(etna)

## ajout des couples clés/valeurs pour les coordonnées
print("Ajout des coordonnées... ", end="")
etna["Latitude"] = "37.748 N"
etna["Longitude"] = "14.999 E"

## écriture des coordonnées dans le fichier json
with open(fichierJson, "w", encoding="utf-8") as fichier:
    json.dump(etna, fichier, ensure_ascii=False, indent=4)
print("OK")

## Seconde modification pour une date
print("Modification de la date de la dernière éruption... ", end="")
with open(fichierJson, "r", encoding="utf-8") as fichier:
    etna = json.load(fichier)

## modification de la date (+2 jours)
dateEruption = date.fromisoformat(etna["Dernière éruption"])
nouvelleDateEruption = dateEruption + timedelta(days=2)
etna["Dernière éruption"] = nouvelleDateEruption.isoformat()

## écriture de le nouvelle date dans le fichier json
with open(fichierJson, "w", encoding="utf-8") as fichier:
    json.dump(etna, fichier, ensure_ascii=False, indent=4)
print("OK")

## Affichage du fichier json
with open(fichierJson, "r", encoding="utf-8") as fichier:
    etna = json.load(fichier, object_pairs_hook=OrderedDict)
    pprint(etna)
