import json
nuevos_datos = [
    {"nombre": "Cacao", "hectareas": 8, "produccion_toneladas": 3.5},
    {"nombre": "Palma", "hectareas": 12, "produccion_toneladas": 7.2}
]
with open("nuevos_cultivos.json", "w") as archivo:
    json.dump(nuevos_datos, archivo, indent=4)