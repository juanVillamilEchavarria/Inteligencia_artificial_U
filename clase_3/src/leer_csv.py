import csv
with open("cultivos.csv", "r") as archivo:
    lector = csv.reader(archivo)
    for fila in lector:
        print(fila)