"""
generar_datos.py
Genera el dataset cultivos_cartago.csv para la Clase 9.

Cada fila representa un lote de cultivo de la zona rural de Cartago, Valle,
con dos variables climáticas medidas durante el ciclo del cultivo y una
etiqueta que indica si la cosecha fue exitosa (1) o no (0).

IMPORTANTE: los datos son SIMULADOS con rangos realistas para la región.
Se usan con fines pedagógicos para entrenar el perceptrón.
"""

import numpy as np
import pandas as pd

# ============================================================
# 1. Semilla para que todos obtengan exactamente los mismos datos
# ============================================================
generador = np.random.default_rng(seed=42)

cantidad_lotes = 120

# ============================================================
# 2. Generar las variables de entrada (features)
# ============================================================
# Precipitación promedio mensual en milímetros (entre 40 y 260 mm)
precipitacion_mm = generador.uniform(40, 260, cantidad_lotes).round(1)

# Temperatura promedio en grados Celsius (entre 21 y 31 °C)
temperatura_c = generador.uniform(21, 31, cantidad_lotes).round(1)

# ============================================================
# 3. Generar la etiqueta (variable objetivo)
# ============================================================
# Regla oculta: más lluvia ayuda y más calor perjudica.
# Se agrega "ruido" para que los datos no sean perfectos (como en la vida real).
ruido = generador.normal(0, 0.8, cantidad_lotes)
puntaje = 0.03 * (precipitacion_mm - 150) - 0.6 * (temperatura_c - 26) + ruido
cosecha_exitosa = (puntaje > 0).astype(int)

# ============================================================
# 4. Construir el DataFrame y guardarlo en la carpeta data
# ============================================================
df = pd.DataFrame({
    "lote": [f"L{numero:03d}" for numero in range(1, cantidad_lotes + 1)],
    "precipitacion_mm": precipitacion_mm,
    "temperatura_c": temperatura_c,
    "cosecha_exitosa": cosecha_exitosa,
})

ruta_salida = "data/cultivos_cartago.csv"
df.to_csv(ruta_salida, index=False)

print("=" * 60)
print("DATASET GENERADO")
print("=" * 60)
print(f"Archivo: {ruta_salida}")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
print("\nPrimeras 5 filas:")
print(df.head())
print("\nCantidad de lotes por clase:")
print(df["cosecha_exitosa"].value_counts())
