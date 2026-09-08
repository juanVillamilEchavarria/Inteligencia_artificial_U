import csv
with open("cultivos.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
           print(fila)