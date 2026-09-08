import csv

def leer_cultivos(archivo_csv):
    cultivos = []
    with open(archivo_csv, "r") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            cultivo = {
                "nombre": fila["nombre"],
                "hectareas": float(fila["hectareas"]),
                "produccion_toneladas": float(fila["produccion_toneladas"])
            }
            cultivos.append(cultivo)
    return cultivos


def calcular_estadisticas(cultivos):
    total_hectareas = sum(c["hectareas"] for c in cultivos)
    total_produccion = sum(c["produccion_toneladas"] for c in cultivos)
    promedio = total_produccion / total_hectareas if total_hectareas > 0 else 0

    mayor = max(cultivos, key=lambda c: c["produccion_toneladas"])
    menor = min(cultivos, key=lambda c: c["produccion_toneladas"])

    return {
        "total_hectareas": total_hectareas,
        "total_produccion": total_produccion,
        "promedio_rendimiento": promedio,
        "cultivo_mayor_produccion": mayor["nombre"],
        "cultivo_menor_produccion": menor["nombre"]
    }


def generar_informe(estadisticas, archivo_salida):
    """Genera un informe en Markdown con las estadísticas."""
    with open(archivo_salida, "w") as archivo:
        archivo.write("# Informe de Cultivos\n\n")
        archivo.write(f"**Total de hectáreas:** {estadisticas['total_hectareas']:.2f}\n")
        archivo.write(f"**Total de producción (toneladas):** {estadisticas['total_produccion']:.2f}\n")
        archivo.write(f"**Promedio de rendimiento (ton/ha):** {estadisticas['promedio_rendimiento']:.2f}\n")
        archivo.write(f"**Cultivo con mayor producción:** {estadisticas['cultivo_mayor_produccion']}\n")
        archivo.write(f"**Cultivo con menor producción:** {estadisticas['cultivo_menor_produccion']}\n")


# Programa principal
if __name__ == "__main__":
    cultivos = leer_cultivos("cultivos.csv")
    estadisticas = calcular_estadisticas(cultivos)
    generar_informe(estadisticas, "informe_cultivos.md")
    print("Informe generado correctamente: informe_cultivos.md")