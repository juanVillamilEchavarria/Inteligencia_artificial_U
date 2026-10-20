"""
perceptron_reto.py  –  Actividad grupal Clase 9
Construcción completa del perceptrón con descenso del gradiente.

¿CÓMO FUNCIONA ESTE ARCHIVO?
  - El código tiene 7 RETOS marcados con  >>> RETO X <<<.
  - Cada reto tiene un PUNTO DE CONTROL que verifica si quedó bien resuelto.
  - Al ejecutar el script, se detiene en el primer reto pendiente y muestra una pista.
  - Resuelva el reto, guarde (Ctrl + S) y vuelva a ejecutar:  python perceptron_reto.py
  - Cuando todos los retos estén superados, el script genera los gráficos finales.

Genera: curva_aprendizaje.png, frontera_decision.png
"""

import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def punto_de_control(superado, reto, pista):
    """Verifica un reto. Si no está superado, muestra la pista y detiene el programa."""
    if superado:
        print(f"[OK] {reto} superado")
    else:
        print(f"\n[PENDIENTE] {reto}")
        print(f"   Pista: {pista}")
        print("   Complete el reto, guarde con Ctrl + S y vuelva a ejecutar el script.")
        sys.exit()


# ============================================================
# 1. Cargar los datos
# ============================================================
df = pd.read_csv("data/cultivos_cartago.csv")
X = df[["precipitacion_mm", "temperatura_c"]].to_numpy()
y = df["cosecha_exitosa"].to_numpy()
print(f"Datos: X tiene forma {X.shape} | y tiene forma {y.shape}\n")


# ============================================================
# >>> RETO 1 <<<  Vectorización: todas las sumas ponderadas a la vez
# ============================================================
def suma_ponderada(X, w, b):
    """Debe devolver z = w1*x1 + w2*x2 + b para TODAS las filas de X, sin usar ciclos."""
    # ESCRIBA AQUÍ SU SOLUCIÓN (reemplace la línea de abajo)
    return np.dot(X, w) + b


X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
z_and = suma_ponderada(X_and, np.array([0.5, 0.5]), -0.7)
punto_de_control(
    z_and is not None and np.allclose(z_and, [-0.7, -0.2, -0.2, 0.3]),
    "RETO 1 (vectorización)",
    "Con la neurona AND de la Clase 8 (w=[0.5, 0.5], b=-0.7) se esperaba [-0.7 -0.2 -0.2 0.3]. "
    "¿Qué operador de NumPy multiplica una matriz por un vector? (Clase 4)",
)


# ============================================================
# >>> RETO 2 <<<  Una activación que entregue probabilidades
# ============================================================
def sigmoide(z):
    """Debe convertir cualquier número z en un valor entre 0 y 1 (0.5 cuando z = 0)."""
    # ESCRIBA AQUÍ SU SOLUCIÓN (reemplace la línea de abajo)
    return 1 / (1 + np.exp(-z))


prueba = sigmoide(np.array([-6.0, 0.0, 6.0]))
punto_de_control(
    prueba is not None and np.allclose(prueba, [0.0025, 0.5, 0.9975], atol=1e-3),
    "RETO 2 (función sigmoide)",
    "Para z = -6, 0 y 6 se esperaba aproximadamente 0.0025, 0.5 y 0.9975. "
    "Busque la fórmula de la función sigmoide; en NumPy, e elevado a la x es np.exp(x).",
)


def predecir_probabilidad(X, w, b):
    return sigmoide(suma_ponderada(X, w, b))


# ============================================================
# >>> RETO 3 <<<  Medir qué tan mal predice el modelo
# ============================================================
def calcular_perdida(y_real, y_prob):
    """Pérdida logarítmica (entropía cruzada binaria). Debe devolver UN solo número."""
    epsilon = 1e-9
    y_prob = np.clip(y_prob, epsilon, 1 - epsilon)   # evita log(0)
    # ESCRIBA AQUÍ SU SOLUCIÓN (reemplace la línea de abajo)
    return  - np.mean(y_real * np.log(y_prob) + (1 - y_real) * np.log(1 - y_prob))

perdida_inicial = calcular_perdida(np.array([1, 0, 1, 0]), np.array([0.5, 0.5, 0.5, 0.5]))
perdida_segura = calcular_perdida(np.array([1]), np.array([0.9]))
punto_de_control(
    perdida_inicial is not None and np.isclose(perdida_inicial, 0.6931, atol=1e-3)
    and np.isclose(perdida_segura, 0.1054, atol=1e-3),
    "RETO 3 (función de pérdida)",
    "Si el modelo dice 0.5 para todo, la pérdida debe ser 0.6931; si acierta con 0.9, debe ser 0.1054. "
    "Busque 'binary cross entropy'. Use np.log y np.mean.",
)


def calcular_exactitud(y_real, y_prob):
    return np.mean((y_prob >= 0.5).astype(int) == y_real)


# ============================================================
# >>> RETO 4 (parte A) <<<  ¿Hacia dónde mover los pesos?
# ============================================================
def calcular_gradientes(X, y_real, y_prob):
    """Debe devolver (gradiente_w, gradiente_b) promediando sobre todos los ejemplos."""
    # ESCRIBA AQUÍ SU SOLUCIÓN (reemplace las dos líneas de abajo)
    gradiente_w =  np.dot(X.T, (y_prob - y_real)) / len(y_real)  
    gradiente_b = np.mean(y_prob - y_real)
    return gradiente_w, gradiente_b


gw, gb = calcular_gradientes(np.array([[1.0, 0.0], [0.0, 1.0]]), np.array([1, 0]), np.array([0.5, 0.5]))
punto_de_control(
    gw is not None and np.allclose(gw, [-0.25, 0.25]) and np.isclose(gb, 0.0),
    "RETO 4A (gradientes)",
    "Con X=[[1,0],[0,1]], y=[1,0] y y_prob=[0.5,0.5] se esperaba gradiente_w=[-0.25 0.25] y gradiente_b=0. "
    "El error es (y_prob - y_real); el gradiente de w usa la transpuesta de X y se divide por n.",
)


# ============================================================
# >>> RETO 5 <<<  Preparar las entradas (resuélvalo cuando el punto de control lo pida)
# ============================================================
# Por ahora las entradas se usan tal como vienen del archivo.
media =  X.mean(axis=0)       # (se necesitará en los retos 6 y 7)
desviacion = X.std( axis=0)    # (se necesitará en los retos 6 y 7)
X_esc = (X - media) / desviacion


# ============================================================
# 2. Entrenamiento con descenso del gradiente
# ============================================================
w = np.zeros(2)
b = 0.0
tasa_aprendizaje = 0.1
epocas = 500
historial_perdida = []
historial_exactitud = []

for epoca in range(1, epocas + 1):
    y_prob = predecir_probabilidad(X_esc, w, b)
    gradiente_w, gradiente_b = calcular_gradientes(X_esc, y, y_prob)

    # >>> RETO 4 (parte B) <<<  Dar el paso de aprendizaje
    # ESCRIBA AQUÍ SU SOLUCIÓN (complete las dos líneas de abajo)
    w = w - tasa_aprendizaje * gradiente_w
    b = b - tasa_aprendizaje * gradiente_b

    if epoca == 1:
        punto_de_control(
            np.allclose(w, -tasa_aprendizaje * gradiente_w) and np.isclose(b, -tasa_aprendizaje * gradiente_b),
            "RETO 4B (actualización de pesos)",
            "Los pesos no cambiaron o se movieron en la dirección equivocada. Recuerde la Clase 8: el nuevo peso "
            "depende del peso anterior, de la tasa de aprendizaje y del gradiente. ¿Se suma o se resta para ir 'cuesta abajo'?",
        )

    historial_perdida.append(calcular_perdida(y, y_prob))
    historial_exactitud.append(calcular_exactitud(y, y_prob))
    if epoca == 1 or epoca % 100 == 0:
        print(f"Época {epoca:>3} | Pérdida: {historial_perdida[-1]:.4f} | "
              f"Exactitud: {historial_exactitud[-1]:.2%} | w=[{w[0]:.3f}, {w[1]:.3f}] b={b:.3f}")


y_prob_final = predecir_probabilidad(X_esc, w, b)
exactitud_final = calcular_exactitud(y, y_prob_final)
print(f"\nRESULTADO: pérdida final {calcular_perdida(y, y_prob_final):.4f} | exactitud {exactitud_final:.2%}")
print(f"Pesos finales: w1={w[0]:.4f}, w2={w[1]:.4f}, b={b:.4f}\n")

punto_de_control(
    media is not None and desviacion is not None
    and np.allclose(X_esc.mean(axis=0), 0, atol=1e-6) and np.allclose(X_esc.std(axis=0), 1, atol=1e-6),
    "RETO 5 (preparación de las entradas)",
    "El modelo entrena, pero ¿los resultados son buenos? ¿Apareció alguna advertencia (RuntimeWarning)? "
    "Compare los valores de la lluvia (40 a 260) con los de la temperatura (21 a 31). "
    "Recuerde lo que se hizo en la Clase 7 antes de entregar datos a un modelo. "
    "Guarde también en 'media' y 'desviacion' los valores usados: se necesitan en los retos 6 y 7.",
)

# ============================================================
# 3. Curva de aprendizaje
# ============================================================
fig, (eje1, eje2) = plt.subplots(1, 2, figsize=(12, 4.5))
eje1.plot(historial_perdida, color="red")
eje1.set_title("Pérdida por época")
eje1.set_xlabel("Época")
eje1.grid(True, alpha=0.3)
eje2.plot(historial_exactitud, color="green")
eje2.set_title("Exactitud por época")
eje2.set_xlabel("Época")
eje2.set_ylim(0, 1.05)
eje2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("curva_aprendizaje.png", dpi=150)
plt.close()
print("Gráfico guardado: curva_aprendizaje.png")

# ============================================================
# >>> RETO 6 <<<  La frontera de decisión
# ============================================================
x1_original = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
x1_esc = (x1_original - media[0]) / desviacion[0]
# La frontera es la línea donde la neurona duda totalmente (probabilidad 0.5).
x2_esc =-(w[0] * x1_esc + b) / w[1]

punto_de_control(
    x2_esc is not None and np.allclose(w[0] * x1_esc + w[1] * x2_esc + b, 0, atol=1e-6),
    "RETO 6 (frontera de decisión)",
    "¿Para qué valor de z la sigmoide da exactamente 0.5? Escriba esa igualdad con w1, x1, w2, x2 y b, "
    "y despeje x2.",
)
x2_original = x2_esc * desviacion[1] + media[1]

plt.figure(figsize=(9, 6))
plt.scatter(X[y == 1, 0], X[y == 1, 1], color="green", edgecolors="black", label="Exitosa (1)")
plt.scatter(X[y == 0, 0], X[y == 0, 1], color="orange", marker="s", edgecolors="black", label="No exitosa (0)")
plt.plot(x1_original, x2_original, color="blue", linewidth=2.5, label="Frontera de decisión")
plt.ylim(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5)
plt.title("Frontera de decisión – Cultivos de Cartago")
plt.xlabel("Precipitación mensual (mm)")
plt.ylabel("Temperatura promedio (°C)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("frontera_decision.png", dpi=150)
plt.close()
print("Gráfico guardado: frontera_decision.png")

# ============================================================
# >>> RETO 7 <<<  Usar el modelo con lotes nuevos
# ============================================================
lotes_nuevos = np.array([
    [220.0, 23.5],
    [60.0, 30.0],
    [150.0, 26.0],
])
lotes_nuevos_esc = (lotes_nuevos - media) / desviacion

punto_de_control(
    lotes_nuevos_esc is not None and np.allclose(lotes_nuevos_esc, (lotes_nuevos - media) / desviacion),
    "RETO 7 (predicción de lotes nuevos)",
    "Los lotes nuevos deben pasar por la MISMA preparación que los datos de entrenamiento. "
    "¿Con qué media y qué desviación? ¿Las de los 3 lotes nuevos o las de los 120 lotes?",
)

for (lluvia, temperatura), probabilidad in zip(lotes_nuevos, predecir_probabilidad(lotes_nuevos_esc, w, b)):
    decision = "EXITOSA" if probabilidad >= 0.5 else "NO EXITOSA"
    print(f"Lluvia {lluvia:>5.1f} mm | Temp {temperatura:>4.1f} °C -> {probabilidad:.2%} -> {decision}")

print("\n*** ¡Todos los retos superados! Perceptrón completo construido desde cero. ***")
