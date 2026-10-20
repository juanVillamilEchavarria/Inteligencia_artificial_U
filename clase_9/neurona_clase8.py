"""
neurona_clase8.py  –  MISIÓN 0 (diagnóstico)
Se toma la neurona de la Clase 8 (la de la compuerta AND), SIN CAMBIAR SU LÓGICA,
y se pone a trabajar con datos reales: 120 lotes de cultivo de Cartago.

Pregunta de la misión: ¿esta neurona sirve para un problema real?
Ejecute el script, observe con atención y responda las preguntas de la guía.

Genera: diagnostico_clase8.png
"""

import csv
import matplotlib.pyplot as plt

# ============================================================
# 1. Función de activación y neurona (idénticas a la Clase 8)
# ============================================================
def escalon(z):
    return 1 if z >= 0 else 0


def neurona(x1, x2, w1, w2, b):
    z = w1 * x1 + w2 * x2 + b
    return escalon(z)


# ============================================================
# 2. Cargar los datos reales (sin ninguna preparación)
# ============================================================
datos = []
with open("data/cultivos_cartago.csv", encoding="utf-8") as archivo:
    for fila in csv.DictReader(archivo):
        datos.append((float(fila["precipitacion_mm"]),
                      float(fila["temperatura_c"]),
                      int(fila["cosecha_exitosa"])))
print(f"Lotes cargados: {len(datos)}")

# ============================================================
# 3. Entrenamiento con la regla de la Clase 8
# ============================================================
w1, w2, b = 0.1, 0.1, 0.0
tasa_aprendizaje = 0.1
errores_por_epoca = []

for epoca in range(30):
    error_total = 0
    for x1, x2, y_real in datos:
        y_pred = neurona(x1, x2, w1, w2, b)
        error = y_real - y_pred
        error_total += abs(error)
        w1 += tasa_aprendizaje * error * x1
        w2 += tasa_aprendizaje * error * x2
        b += tasa_aprendizaje * error
    errores_por_epoca.append(error_total)
    print(f"Época {epoca + 1:>2} | Errores: {error_total:>3} de {len(datos)} | "
          f"w1={w1:>8.2f} w2={w2:>8.2f} b={b:>6.2f}")

# ============================================================
# 4. Resultado final
# ============================================================
aciertos = sum(1 for x1, x2, y in datos if neurona(x1, x2, w1, w2, b) == y)
print(f"\nExactitud final: {aciertos / len(datos):.2%}")
print(f"Ejemplo: la neurona dice {neurona(150, 26, w1, w2, b)} para un lote de 150 mm y 26 °C "
      "(¿qué tan segura está? No lo sabemos...)")

plt.figure(figsize=(8, 5))
plt.plot(range(1, len(errores_por_epoca) + 1), errores_por_epoca, marker="o", color="red")
plt.title("Diagnóstico: neurona de la Clase 8 con datos reales")
plt.xlabel("Época")
plt.ylabel("Número de errores")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("diagnostico_clase8.png", dpi=150)
plt.close()
print("Gráfico guardado: diagnostico_clase8.png")
