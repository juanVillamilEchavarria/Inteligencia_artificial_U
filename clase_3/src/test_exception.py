import csv
try:
    with open("cultivos.csv", "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            print(fila)
except FileNotFoundError:
    print("El archivo no existe. Por favor, verifique la ruta.")