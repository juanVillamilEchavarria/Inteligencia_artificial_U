
--- Página 1 ---
1 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Clase 12: Scikit-Learn – Entrenar, Evaluar y Guardar Modelos 
Inteligencia Artificial · Ingeniería de Sistemas · Período 2026-02 · Docente: Jhon James Cano Sánchez · 
Lunes 9 de noviembre de 2026 · 90 minutos 
¿De qué trata esta clase? En la clase del perceptrón se programó un modelo a 
mano, línea por línea, para entender cómo aprende una IA. Hoy se usa Scikit-Learn, 
una librería que hace ese mismo trabajo en pocas líneas. 
Al terminar, cada estudiante sabrá entrenar un modelo, probarlo con datos que no 
conoce, compararlo con otros y guardarlo en un archivo. Eso es exactamente lo que 
necesita el proyecto final. 
1. Lo que ya sabemos (5 min) 
• 
Clase del perceptrón: se programó una neurona con NumPy: suma ponderada 
X @ w + b, sigmoide, pérdida, descenso del gradiente y escalado de los datos. 
• 
Segundo parcial: se limpiaron datos con Pandas, se hicieron gráficos con 
Seaborn y se entrenó un perceptrón con datos de Cartago. 
• 
Avance 2: cada grupo aplicó el perceptrón a los datos de su proyecto. 
Quedaron dos preguntas pendientes que hoy se responden: 
1. La exactitud del perceptrón se midió con los mismos datos con los que 
aprendió. ¿Es confiable ese resultado? → Hoy se aprende a separar datos de 
entrenamiento y de prueba. 
2. En la clase «¿Cómo aprende una IA?» se vio que una sola neurona no puede 
aprender la compuerta XOR. ¿Hay alguna forma? → Hoy se resuelve con una red 
neuronal. 
2. ¿Qué se aprenderá hoy? 
• 
Usar Scikit-Learn con tres pasos: crear el modelo, entrenarlo (fit) y predecir 
(predict). 
• 
Separar los datos en entrenamiento y prueba. 
• 
Comparar tres modelos y elegir el mejor con las métricas adecuadas. 
• 
Predecir un número (regresión), además de una clase 0/1. 
• 
Reconocer cuando un modelo memoriza en lugar de aprender (sobreajuste). 
• 
Guardar un modelo en un archivo y usarlo después sin volver a entrenarlo. 

--- Página 2 ---
2 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
3. Agenda de la Clase 
Momento 
Actividad 
Tiempo 
1 
Lo que ya sabemos 
5 min 
2 
Conceptos clave 
25 min 
3 
Preparar el entorno (carpeta clase12) 
10 min 
4 
Actividad práctica: 5 pasos 
45 min 
5 
Cierre y trabajo para el proyecto final 
5 min 
 
Total 
90 min 
 
4. Conceptos Clave (25 min) 
4.1. ¿Qué es Scikit-Learn? 
Es la librería de Python más usada para Machine Learning. Ya viene instalada en el 
contenedor del curso (aparece como scikit-learn en requirements.txt). Todos 
sus modelos se usan igual, en tres pasos: 
modelo = NombreDelModelo()        # 1. crear el modelo 
modelo.fit(X_train, y_train)      # 2. entrenar: el modelo aprende los pesos 
predicciones = modelo.predict(X)  # 3. predecir con datos nuevos 
 
Lo que antes se programó a mano ahora es una sola instrucción: 
En la clase del perceptrón (a mano) 
Con Scikit-Learn 
Ciclo de 500 épocas con descenso del gradiente 
modelo.fit(X, y) 
sigmoide(X @ w + b) >= 0.5 
modelo.predict(X) 
sigmoide(X @ w + b) (probabilidad) 
modelo.predict_proba(X) 
(X - media) / desviación 
StandardScaler() 
Pesos w y sesgo b 
modelo.coef_ y modelo.intercept_ 
 
Importante: Se usa la librería después de haber construido el modelo a mano. Así, 
cuando se escribe fit(), ya se sabe qué ocurre por dentro. 
4.2. Datos de entrenamiento y datos de prueba 
Si un profesor evalúa con las mismas preguntas del taller, el estudiante puede sacar 
5.0 solo porque las memorizó. Con los modelos pasa lo mismo. Por eso los datos se 
dividen en dos partes: 
• 
Entrenamiento (80 %): el modelo aprende con estos datos. 
• 
Prueba (20 %): se guardan aparte y solo se usan al final para medir qué tan bien 
funciona el modelo con datos que nunca vio. 

--- Página 3 ---
3 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
from sklearn.model_selection import train_test_split 
 
X_train, X_test, y_train, y_test = train_test_split( 
    X, y, test_size=0.2, random_state=42, stratify=y 
) 
 
• 
test_size=0.2: el 20 % de los datos va para prueba. 
• 
random_state=42: la división siempre sale igual, así todos obtienen los 
mismos resultados. 
• 
stratify=y: las dos partes quedan con la misma proporción de 0 y 1. 
4.3. Pipeline: escalar sin equivocarse 
En la clase del perceptrón se aprendió una regla: los datos nuevos se escalan con la 
media y la desviación de los datos de entrenamiento. Un Pipeline une el escalado y 
el modelo en un solo objeto, y aplica esa regla automáticamente: 
modelo = Pipeline([ 
    ("escalado", StandardScaler()),     # paso 1: escalar 
    ("modelo", LogisticRegression()),   # paso 2: el modelo 
]) 
 
Cuando se guarda el Pipeline en un archivo, el escalado se guarda junto con el 
modelo. Así nunca se olvida escalar los datos nuevos. 
4.4. Tres modelos para clasificar (0 o 1) 
Modelo 
¿Cómo decide? 
Para recordar 
Regresión logística 
Suma ponderada + sigmoide. Separa las 
clases con una línea recta. 
Es el perceptrón de la clase 
anterior, hecho por la librería. 
KNN (vecinos más 
cercanos) 
Busca los 5 registros más parecidos y 
decide por mayoría. 
Necesita datos escalados 
porque mide distancias. 
Árbol de decisión 
Hace preguntas de sí o no («¿llovió más 
de 140 mm?») hasta decidir. 
Es fácil de leer, pero si crece 
mucho, memoriza. 
 
4.5. ¿Cómo saber si el modelo es bueno? 
La matriz de confusión cuenta los aciertos y los errores del modelo: 
 
El modelo dijo 0 
El modelo dijo 1 
Era 0 
Acierto (verdadero negativo) 
Error: falsa alarma (falso positivo) 
Era 1 
Error: caso que se escapó (falso 
negativo) 
Acierto (verdadero positivo) 
 

--- Página 4 ---
4 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Con esos conteos se calculan las métricas: 
Métrica 
Pregunta que responde 
¿Cuándo importa más? 
Exactitud 
¿Qué porcentaje acertó en total? 
Cuando hay más o menos la misma 
cantidad de 0 y de 1. 
Precisión 
De los que el modelo dijo «1», ¿cuántos 
eran 1 de verdad? 
Cuando una falsa alarma cuesta caro 
(por ejemplo, enviar un técnico sin 
necesidad). 
Recall 
De todos los 1 reales, ¿cuántos 
encontró? 
Cuando dejar escapar un caso es grave 
(por ejemplo, una alerta de incendio). 
F1 
Un equilibrio entre precisión y recall. 
Buena métrica general para elegir el 
mejor modelo. 
 
Todas van de 0 a 1: 0.958 significa 95.8 %. 
4.6. Predecir un número (regresión) 
Si lo que se quiere predecir es un número (kilos de café, consumo de agua, ventas), se 
usa LinearRegression. Es la misma suma ponderada, pero sin sigmoide. Para medir 
el error se usan: 
Métrica 
¿Qué significa? 
MAE 
En promedio, cuánto se equivoca el modelo (en las mismas unidades: kg/ha, 
m³…). 
RMSE 
Parecido al MAE, pero castiga más los errores grandes. 
R² 
Qué tan bien explica el modelo los datos: 1 es perfecto; 0 es igual que adivinar 
siempre el promedio. 
 
4.7. Validación cruzada y sobreajuste 
• 
Validación cruzada: en lugar de probar una sola vez, divide los datos en 5 
partes y prueba 5 veces, cada vez con una parte distinta. Luego promedia los 
resultados. Es una medida más confiable. 
• 
Sobreajuste: el modelo memoriza el entrenamiento (casi 100 %) pero falla con 
datos nuevos. Se nota cuando la exactitud de entrenamiento es mucho mayor 
que la de prueba. 
• 
Subajuste: el modelo es tan simple que falla en los dos. 
4.8. ¿Y las redes neuronales? 
Una red neuronal es un grupo de perceptrones organizados en capas. Las capas del 
medio (capas ocultas) permiten fronteras curvas, por eso pueden resolver XOR. Scikit-
Learn trae MLPClassifier para crear redes pequeñas. Los asistentes de chat y otras 
IA modernas usan las mismas piezas del curso (pesos, activación, pérdida y descenso 
del gradiente), pero con millones de neuronas. 

--- Página 5 ---
5 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
4.9. Guardar y cargar un modelo 
import joblib 
 
joblib.dump(modelo, "modelo_cultivos.joblib")   # guardar, después de entrenar 
modelo = joblib.load("modelo_cultivos.joblib")  # cargar en otro script, sin entrenar de 
nuevo 
 
Así funcionará la demostración del proyecto final: un script entrena y guarda; otro 
script carga y predice en segundos. 
5. Preparar el Entorno (10 min) 
Antes de empezar: Todos los comandos se escriben en la terminal de Ubuntu 
(WSL), desde la carpeta del curso ~/IA. Docker Desktop debe estar abierto. 
5.1. Ir a la carpeta del curso 
cd ~/IA 
ls 
 
Deben aparecer las carpetas de las clases anteriores (por ejemplo, clase7, clase8, 
clase10). 
5.2. Apagar el contenedor de la clase anterior 
Todas las clases usan un contenedor con el mismo nombre, ia_python. Si el de la 
clase anterior sigue encendido, hay que apagarlo y borrarlo (los archivos no se pierden, 
porque están en la carpeta de cada clase): 
docker ps 
 
Si en la lista aparece ia_python: 
docker stop ia_python 
docker rm ia_python 
 
5.3. Crear la carpeta clase12 y copiar lo necesario 
Se copian los archivos del entorno (Docker) y los datos de cultivos desde la carpeta de 
la clase anterior, clase10: 
mkdir -p clase12/src clase12/data clase12/notebooks 
cp clase10/Dockerfile clase10/docker-compose.yml clase10/requirements.txt clase12/ 
cp clase10/data/cultivos_cartago.csv clase12/data/ 
ls clase12 clase12/data 
 

--- Página 6 ---
6 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Salida esperada: 
clase12: 
data  docker-compose.yml  Dockerfile  notebooks  requirements.txt  src 
 
clase12/data: 
cultivos_cartago.csv 
 
¿No encuentra cultivos_cartago.csv? Es el archivo de lotes de cultivo que se usó 
para entrenar el perceptrón. Búsquelo con ls */data y cópielo desde la carpeta 
donde aparezca, cambiando clase10 por el nombre de esa carpeta. 
Verificar que requirements.txt incluya Scikit-Learn: 
cat clase12/requirements.txt 
 
numpy 
pandas 
matplotlib 
scikit-learn 
jupyter 
seaborn 
 
Si 
falta 
scikit-learn, 
agregarlo 
con 
echo 
"scikit-learn" 
>> 
clase12/requirements.txt. 
5.4. Encender el contenedor y abrir VS Code 
cd clase12 
docker-compose up -d --build 
code . 
 
La primera vez tarda unos minutos mientras se instalan las librerías. Luego se entra al 
contenedor: 
docker exec -it ia_python bash 
 
Ya dentro del contenedor (el indicador cambia a algo como root@…:/app#), ir a src 
y comprobar que todo esté listo: 
cd src 
python -c "import sklearn, seaborn, joblib; print('Entorno listo', sklearn.__version__)" 
 
Salida esperada (el número de versión puede variar): 
Entorno listo 1.9.1 
 

--- Página 7 ---
7 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
6. Actividad Práctica Paso a Paso (45 min) 
Se trabaja con el archivo cultivos_cartago.csv: 120 lotes de cultivo con la lluvia 
(precipitacion_mm), la temperatura (temperatura_c) y si la cosecha fue exitosa 
(cosecha_exitosa: 1 = sí, 0 = no). 
Cómo crear cada archivo: En VS Code, clic derecho sobre la carpeta src → New 
File → escribir el nombre → pegar el código → Ctrl + S. Después se ejecuta en la 
terminal del contenedor, que debe estar en /app/src. 
Paso 1: Comparar tres modelos (clasificar_cultivos.py) 
Este script divide los datos, entrena los tres modelos, los compara con los datos de 
prueba y guarda el mejor en un archivo. 
src/clasificar_cultivos.py 
""" 
Paso 1: comparar tres modelos de clasificación con Scikit-Learn. 
Datos: cultivos_cartago.csv (los mismos de la clase del perceptrón). 
Genera: matriz_confusion.png y modelo_cultivos.joblib 
""" 
import joblib 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, 
                             precision_score, recall_score) 
from sklearn.model_selection import cross_val_score, train_test_split 
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import StandardScaler 
from sklearn.tree import DecisionTreeClassifier 
 
# 1. Cargar los datos 
df = pd.read_csv("../data/cultivos_cartago.csv") 
X = df[["precipitacion_mm", "temperatura_c"]]   # entradas 
y = df["cosecha_exitosa"]                        # lo que se quiere predecir (0 o 1) 
 
# 2. Separar los datos: 80 % para entrenar y 20 % para probar 
X_train, X_test, y_train, y_test = train_test_split( 
    X, y, test_size=0.2, random_state=42, stratify=y 
) 
print(f"Lotes para entrenar: {len(X_train)} | Lotes para probar: {len(X_test)}") 
 
# 3. Los tres modelos (cada uno escala los datos antes de aprender) 
modelos = { 
    "Regresión logística": Pipeline([ 
        ("escalado", StandardScaler()), 
        ("modelo", LogisticRegression()), 
    ]), 
    "KNN (5 vecinos)": Pipeline([ 
        ("escalado", StandardScaler()), 
        ("modelo", KNeighborsClassifier(n_neighbors=5)), 
    ]), 

--- Página 8 ---
8 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
    "Árbol de decisión": Pipeline([ 
        ("escalado", StandardScaler()), 
        ("modelo", DecisionTreeClassifier(max_depth=3, random_state=42)), 
    ]), 
} 
 
# 4. Entrenar cada modelo y medirlo con los datos de prueba 
resultados = [] 
for nombre, modelo in modelos.items(): 
    modelo.fit(X_train, y_train)          # aprende solo con los datos de entrenamiento 
    y_pred = modelo.predict(X_test)       # predice datos que nunca vio 
    resultados.append({ 
        "Modelo": nombre, 
        "Exactitud": accuracy_score(y_test, y_pred), 
        "Precisión": precision_score(y_test, y_pred), 
        "Recall": recall_score(y_test, y_pred), 
        "F1": f1_score(y_test, y_pred), 
        "Val. cruzada": cross_val_score(modelo, X, y, cv=5).mean(), 
    }) 
 
tabla = pd.DataFrame(resultados) 
print("\nComparación de modelos (datos de prueba):") 
print(tabla.round(3).to_string(index=False)) 
 
# 5. Elegir el modelo con el F1 más alto 
nombre_mejor = tabla.loc[tabla["F1"].idxmax(), "Modelo"] 
mejor_modelo = modelos[nombre_mejor] 
print(f"\nMejor modelo según F1: {nombre_mejor}") 
 
if nombre_mejor == "Regresión logística": 
    regresion = mejor_modelo.named_steps["modelo"] 
    w1, w2 = regresion.coef_[0] 
    b = regresion.intercept_[0] 
    print(f"Pesos aprendidos: w1 = {w1:.2f}, w2 = {w2:.2f}, b = {b:.2f}") 
 
# 6. Matriz de confusión del mejor modelo 
matriz = confusion_matrix(y_test, mejor_modelo.predict(X_test)) 
print("\nMatriz de confusión (filas = valor real, columnas = predicción):") 
print(matriz) 
 
plt.figure(figsize=(6, 5)) 
sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues", cbar=False, 
            xticklabels=["Predijo 0", "Predijo 1"], yticklabels=["Real 0", "Real 1"]) 
plt.title(f"Matriz de confusión – {nombre_mejor}") 
plt.tight_layout() 
plt.savefig("matriz_confusion.png", dpi=150) 
plt.close() 
print("Gráfico guardado: matriz_confusion.png") 
 
# 7. Guardar el mejor modelo en un archivo 
joblib.dump(mejor_modelo, "modelo_cultivos.joblib") 
print("Modelo guardado: modelo_cultivos.joblib") 
 
 

--- Página 9 ---
9 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Qué hace cada parte: 
• 
Parte 2: separa 96 lotes para entrenar y 24 para probar. 
• 
Parte 3: crea los tres modelos; cada uno va dentro de un Pipeline con su 
escalado. 
• 
Parte 4: entrena cada modelo solo con los datos de entrenamiento y lo mide 
con los de prueba. También calcula la validación cruzada. 
• 
Parte 5: elige el modelo con el F1 más alto (idxmax busca la fila del valor 
máximo). 
• 
Partes 6 y 7: dibuja la matriz de confusión y guarda el mejor modelo con 
joblib. 
Ejecutar: 
python clasificar_cultivos.py 
 
Salida esperada: 
Lotes para entrenar: 96 | Lotes para probar: 24 
 
Comparación de modelos (datos de prueba): 
             Modelo  Exactitud  Precisión  Recall    F1  Val. cruzada 
Regresión logística      0.958      1.000   0.923 0.960         0.883 
    KNN (5 vecinos)      0.875      0.857   0.923 0.889         0.883 
  Árbol de decisión      0.750      0.889   0.615 0.727         0.842 
 
Mejor modelo según F1: Regresión logística 
Pesos aprendidos: w1 = 2.27, w2 = -2.03, b = 0.31 
 
Matriz de confusión (filas = valor real, columnas = predicción): 
[[11  0] 
 [ 1 12]] 
Gráfico guardado: matriz_confusion.png 
Modelo guardado: modelo_cultivos.joblib 

--- Página 10 ---
10 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
 
 
Figura 1. Matriz de confusión del mejor modelo con los 24 lotes de prueba: solo se equivocó en 1. 
¿Qué significan estos resultados? 
• 
Ganó la regresión logística: acertó 23 de 24 lotes de prueba (95.8 %). 
• 
Sus pesos (w1 = 2.27, w2 = −2.03) tienen los mismos signos que los del 
perceptrón hecho a mano (w1 ≈ 2.62, w2 ≈ −2.37): más lluvia ayuda a la cosecha 
y más temperatura la perjudica. Es el mismo modelo. 
• 
Precisión 1.000: todos los lotes que el modelo llamó «exitosos» lo eran. Recall 
0.923: de los 13 exitosos reales, encontró 12. 
• 
La validación cruzada (0.883) es más baja que la exactitud de prueba (0.958), 
pero es más confiable: con solo 24 lotes de prueba, un acierto más o menos 
cambia mucho el porcentaje. 
• 
El árbol fue el peor: estos datos se separan bien con una línea recta, que es lo 
que mejor hace la regresión logística. 
 

--- Página 11 ---
11 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Paso 2: Usar el modelo guardado (usar_modelo.py) 
Este script no entrena nada: carga el archivo del Paso 1 y predice lotes nuevos. Es la 
base de la demostración del proyecto final. 
src/usar_modelo.py 
""" 
Paso 2: usar el modelo guardado para predecir lotes nuevos. 
No se entrena nada: solo se carga el archivo y se predice. 
""" 
import joblib 
import pandas as pd 
 
# 1. Cargar el modelo guardado en el Paso 1 (ya incluye el escalado) 
modelo = joblib.load("modelo_cultivos.joblib") 
 
# 2. Lotes nuevos (mismos nombres de columna que en el entrenamiento) 
lotes_nuevos = pd.DataFrame({ 
    "precipitacion_mm": [220.0, 60.0, 150.0], 
    "temperatura_c": [23.5, 30.0, 26.0], 
}) 
 
# 3. Predecir la probabilidad de éxito y la clase (0 o 1) 
probabilidad = modelo.predict_proba(lotes_nuevos)[:, 1] 
prediccion = modelo.predict(lotes_nuevos) 
 
lotes_nuevos["probabilidad_exito_%"] = (probabilidad * 100).round(1) 
lotes_nuevos["resultado"] = ["Exitosa" if p == 1 else "No exitosa" for p in prediccion] 
 
print("Predicciones con el modelo guardado:") 
print(lotes_nuevos.to_string(index=False)) 
 
• 
Los datos nuevos deben tener los mismos nombres de columna que se usaron 
para entrenar. 
• 
predict_proba(...)[:, 1] devuelve la probabilidad de que la cosecha sea 
exitosa (clase 1). 
python usar_modelo.py 
 
Salida esperada: 
Predicciones con el modelo guardado: 
 precipitacion_mm  temperatura_c  probabilidad_exito_%  resultado 
            220.0           23.5                  99.0    Exitosa 
             60.0           30.0                   0.2 No exitosa 
            150.0           26.0                  52.7    Exitosa 
 
Mucha lluvia y temperatura baja → 99 % de probabilidad de éxito. Poca lluvia y calor → 
0.2 %. El tercer lote está en la frontera (52.7 %): el modelo lo clasifica como exitoso, 
pero con poca seguridad. 

--- Página 12 ---
12 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Para 
el 
proyecto 
final: 
Este 
es 
el 
esquema 
de 
la 
sustentación: 
modelo_proyecto.py entrena y guarda el modelo; usar_modelo.py lo carga y 
predice los casos que se pidan. 
Paso 3: Predecir un número (regresion_rendimiento.py) 
Sirve para los proyectos que predicen una cantidad (producción, consumo, ventas, 
tiempos). El script crea sus propios datos simulados de rendimiento de cultivos y los 
guarda en data/rendimiento_cartago.csv. 
src/regresion_rendimiento.py 
""" 
Paso 3: regresión lineal, es decir, predecir un NÚMERO (rendimiento en kg/ha) 
en lugar de una clase 0/1. 
Los datos son simulados (con rangos realistas para Cartago) y se generan aquí mismo. 
Genera: ../data/rendimiento_cartago.csv y real_vs_predicho.png 
""" 
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score 
from sklearn.model_selection import train_test_split 
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import StandardScaler 
 
# 1. Crear los datos (la semilla hace que siempre salgan iguales) 
generador = np.random.default_rng(seed=7) 
n = 150 
df = pd.DataFrame({ 
    "precipitacion_mm": generador.uniform(40, 260, n).round(1), 
    "temperatura_c": generador.uniform(21, 31, n).round(1), 
    "fertilizante_kg_ha": generador.uniform(50, 300, n).round(0), 
}) 
df["rendimiento_kg_ha"] = ( 
    2000 
    + 6.0 * df["precipitacion_mm"] 
    - 90.0 * (df["temperatura_c"] - 26) 
    + 3.0 * df["fertilizante_kg_ha"] 
    + generador.normal(0, 180, n) 
).round(0) 
df.to_csv("../data/rendimiento_cartago.csv", index=False) 
 
print("Primeros datos:") 
print(df.head()) 
print(f"\nRendimiento promedio: {df['rendimiento_kg_ha'].mean():.0f} kg/ha") 
 
# 2. Entradas, salida y separación entrenamiento/prueba 
entradas = ["precipitacion_mm", "temperatura_c", "fertilizante_kg_ha"] 
X = df[entradas] 
y = df["rendimiento_kg_ha"] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
 
# 3. Entrenar la regresión lineal 
modelo = Pipeline([ 
    ("escalado", StandardScaler()), 

--- Página 13 ---
13 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
    ("modelo", LinearRegression()), 
]) 
modelo.fit(X_train, y_train) 
y_pred = modelo.predict(X_test) 
 
# 4. Medir el error con los datos de prueba 
mae = mean_absolute_error(y_test, y_pred) 
rmse = np.sqrt(mean_squared_error(y_test, y_pred)) 
r2 = r2_score(y_test, y_pred) 
print("\nMétricas con los datos de prueba:") 
print(f"MAE  = {mae:.1f} kg/ha") 
print(f"RMSE = {rmse:.1f} kg/ha") 
print(f"R²   = {r2:.3f}") 
 
# 5. ¿Cuánto pesa cada variable? 
regresion = modelo.named_steps["modelo"] 
print("\nEfecto de cada variable (al subir una desviación estándar):") 
for nombre, coef in zip(entradas, regresion.coef_): 
    print(f"  {nombre}: {coef:+.1f} kg/ha") 
 
# 6. Gráfico: valor real contra valor predicho 
plt.figure(figsize=(7, 6)) 
plt.scatter(y_test, y_pred, color="teal", edgecolors="black") 
minimo, maximo = y.min(), y.max() 
plt.plot([minimo, maximo], [minimo, maximo], color="red", linestyle="--", 
         label="Predicción perfecta") 
plt.title(f"Regresión lineal: real vs. predicho (R² = {r2:.2f})") 
plt.xlabel("Rendimiento real (kg/ha)") 
plt.ylabel("Rendimiento predicho (kg/ha)") 
plt.legend() 
plt.grid(True, alpha=0.3) 
plt.tight_layout() 
plt.savefig("real_vs_predicho.png", dpi=150) 
plt.close() 
print("\nGráfico guardado: real_vs_predicho.png") 
 
python regresion_rendimiento.py 
 
Salida esperada: 
Primeros datos: 
   precipitacion_mm  temperatura_c  fertilizante_kg_ha  rendimiento_kg_ha 
0             177.5           23.5               210.0             3827.0 
1             237.4           29.1                96.0             3703.0 
2             210.7           27.8               240.0             3682.0 
3              89.5           28.2               239.0             3126.0 
4             106.0           27.3               230.0             3168.0 
 
Rendimiento promedio: 3405 kg/ha 
 
Métricas con los datos de prueba: 
MAE  = 122.3 kg/ha 
RMSE = 157.2 kg/ha 
R²   = 0.901 
 
Efecto de cada variable (al subir una desviación estándar): 

--- Página 14 ---
14 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
  precipitacion_mm: +389.2 kg/ha 
  temperatura_c: -250.0 kg/ha 
  fertilizante_kg_ha: +200.5 kg/ha 
 
Gráfico guardado: real_vs_predicho.png 
 
 
Figura 2. Cada punto es un lote de prueba. Entre más cerca esté de la línea roja, mejor fue la predicción. 
• 
MAE = 122.3 kg/ha: en promedio el modelo se equivoca en unos 122 kg/ha, 
frente a un rendimiento promedio de 3405 kg/ha (cerca del 3.6 %). 
• 
R² = 0.901: el modelo explica el 90 % de lo que cambia el rendimiento. 
• 
Efecto de cada variable: la lluvia es la que más suma; la temperatura resta. 
Como en el perceptrón, el signo indica si la variable sube o baja el resultado. 
 

--- Página 15 ---
15 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Paso 4: Resolver la compuerta XOR (red_xor.py) 
XOR da 1 solo cuando las dos entradas son distintas. No hay una línea recta que separe 
esos casos, por eso una sola neurona no puede aprenderlo. 
src/red_xor.py 
""" 
Paso 4: la compuerta XOR. 
Una sola neurona no puede aprender XOR; una red con una capa oculta sí. 
""" 
import numpy as np 
import pandas as pd 
from sklearn.linear_model import LogisticRegression 
from sklearn.neural_network import MLPClassifier 
 
# 1. Datos de la compuerta XOR 
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) 
y = np.array([0, 1, 1, 0]) 
 
# 2. Una sola neurona (regresión logística) 
neurona = LogisticRegression() 
neurona.fit(X, y) 
 
# 3. Una red neuronal con una capa oculta de 4 neuronas 
red = MLPClassifier(hidden_layer_sizes=(4,), activation="tanh", 
                    solver="lbfgs", max_iter=1000, random_state=1) 
red.fit(X, y) 
 
# 4. Comparar las respuestas 
tabla = pd.DataFrame({ 
    "x1": X[:, 0], 
    "x2": X[:, 1], 
    "Esperado": y, 
    "Una neurona": neurona.predict(X), 
    "Red neuronal": red.predict(X), 
}) 
print(tabla.to_string(index=False)) 
print(f"\nExactitud de una neurona:   {neurona.score(X, y):.0%}") 
print(f"Exactitud de la red neuronal: {red.score(X, y):.0%}") 
 
python red_xor.py 
 
Salida esperada: 
 x1  x2  Esperado  Una neurona  Red neuronal 
  0   0         0            0             0 
  0   1         1            0             1 
  1   0         1            0             1 
  1   1         0            0             0 
 
Exactitud de una neurona:   50% 
Exactitud de la red neuronal: 100% 
 

--- Página 16 ---
16 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Una sola neurona se queda en 50 % (es como adivinar). La red con una capa oculta de 
4 neuronas acierta el 100 %. Esta es la respuesta a la pregunta que quedó abierta en la 
clase «¿Cómo aprende una IA?». 
Paso 5 (si hay tiempo): Ver el sobreajuste (profundidad_arbol.py) 
Se entrenan árboles de decisión cada vez más profundos (con más preguntas) y se 
compara su exactitud en entrenamiento y en prueba. 
src/profundidad_arbol.py 
""" 
Paso 5: ver el sobreajuste. 
Un árbol de decisión muy profundo memoriza los datos de entrenamiento, 
pero no mejora con los datos de prueba. 
Genera: sobreajuste_arbol.png 
""" 
import matplotlib.pyplot as plt 
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier 
 
df = pd.read_csv("../data/cultivos_cartago.csv") 
X = df[["precipitacion_mm", "temperatura_c"]] 
y = df["cosecha_exitosa"] 
X_train, X_test, y_train, y_test = train_test_split( 
    X, y, test_size=0.2, random_state=42, stratify=y 
) 
 
# Entrenar árboles cada vez más profundos y medir en entrenamiento y en prueba 
filas = [] 
for profundidad in range(1, 13): 
    arbol = DecisionTreeClassifier(max_depth=profundidad, random_state=42) 
    arbol.fit(X_train, y_train) 
    filas.append({ 
        "Profundidad": profundidad, 
        "Entrenamiento": arbol.score(X_train, y_train), 
        "Prueba": arbol.score(X_test, y_test), 
    }) 
 
tabla = pd.DataFrame(filas) 
print(tabla.round(3).to_string(index=False)) 
 
plt.figure(figsize=(8, 5)) 
plt.plot(tabla["Profundidad"], tabla["Entrenamiento"], marker="o", label="Entrenamiento") 
plt.plot(tabla["Profundidad"], tabla["Prueba"], marker="s", label="Prueba") 
plt.title("Sobreajuste: exactitud según la profundidad del árbol") 
plt.xlabel("Profundidad del árbol (max_depth)") 
plt.ylabel("Exactitud") 
plt.legend() 
plt.grid(True, alpha=0.3) 
plt.tight_layout() 
plt.savefig("sobreajuste_arbol.png", dpi=150) 
plt.close() 
print("\nGráfico guardado: sobreajuste_arbol.png") 
 

--- Página 17 ---
17 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
python profundidad_arbol.py 
 
Salida esperada: 
 Profundidad  Entrenamiento  Prueba 
           1          0.760   0.667 
           2          0.885   0.750 
           3          0.927   0.750 
           4          0.938   0.708 
           5          0.979   0.708 
           6          0.990   0.750 
           7          1.000   0.708 
           8          1.000   0.708 
           9          1.000   0.708 
          10          1.000   0.708 
          11          1.000   0.708 
          12          1.000   0.708 
 
Gráfico guardado: sobreajuste_arbol.png 
 
Figura 3. Desde la profundidad 7 el árbol acierta el 100 % en entrenamiento, pero no mejora en prueba: está 
memorizando. 
La distancia entre la línea azul (entrenamiento) y la naranja (prueba) es el sobreajuste. 
Por eso en el Paso 1 el árbol se limitó a max_depth=3. 
Preguntas de reflexión 
1. ¿Por qué la validación cruzada (0.883) es más confiable que la exactitud con 
solo 24 lotes de prueba (0.958)? 
2. En su proyecto, ¿qué error es más grave: una falsa alarma (falso positivo) o un 
caso que se escapa (falso negativo)? ¿Qué métrica conviene usar? 
3. ¿Qué pasaría si los datos de prueba se escalaran con su propia media? ¿Cómo 
lo evita el Pipeline? 

--- Página 18 ---
18 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
4. ¿Por qué el árbol de profundidad 12 acierta el 100 % en entrenamiento y menos 
en prueba? 
5. ¿Qué tienen en común el perceptrón hecho a mano, LogisticRegression y 
cada neurona de MLPClassifier? 
Guardar el trabajo en GitHub 
Salir del contenedor y subir los cambios desde la carpeta del curso: 
exit 
cd ~/IA 
git add clase12 
git commit -m "Clase 12: Scikit-Learn, métricas y modelo guardado" 
git push 
 
El archivo modelo_cultivos.joblib es pequeño y se puede subir. En el proyecto 
final, si el modelo pesa más de 50 MB, no se sube: se explica en el README cómo volver 
a generarlo. 
Problemas frecuentes 
Mensaje o síntoma 
Causa 
Solución 
Conflict. The container name 
"/ia_python" is already in 
use 
Sigue existiendo el contenedor 
de otra clase. 
docker stop ia_python, docker 
rm ia_python y volver a ejecutar 
docker-compose up -d --build. 
ModuleNotFoundError: No 
module named 'sklearn' 
Falta scikit-learn en 
requirements.txt o se 
ejecutó fuera del contenedor. 
Agregarlo a requirements.txt y 
ejecutar docker-compose up -d 
--build. 
FileNotFoundError: 
../data/cultivos_cartago.csv 
No se copió el archivo o no se 
está en /app/src. 
Revisar el punto 5.3 y ejecutar cd 
/app/src. 
FileNotFoundError: 
modelo_cultivos.joblib 
Se ejecutó el Paso 2 antes del 
Paso 1. 
Ejecutar primero python 
clasificar_cultivos.py. 
ValueError: The feature 
names should match… 
Los datos nuevos tienen 
columnas con otro nombre. 
Usar exactamente los mismos 
nombres de columna del 
entrenamiento. 
ValueError: could not 
convert string to float 
Hay columnas de texto en X. 
Convertirlas con pd.get_dummies, 
como en la clase de preparación de 
datos con Pandas. 
 
 

--- Página 19 ---
19 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
7. Trabajo Independiente: el Modelo del Proyecto Final 
Con lo aprendido hoy se construye el modelo final del proyecto. No se entrega por 
separado: es la parte técnica del proyecto final. 
1. En el repositorio del proyecto, crear src/modelo_proyecto.py a partir de 
clasificar_cultivos.py 
(si 
se 
predice 
una 
clase) 
o 
de 
regresion_rendimiento.py (si se predice un número). 
2. Usar los datos limpios del Avance 2 y aplicar las correcciones de la 
retroalimentación. 
3. Si hay columnas de texto útiles, convertirlas en números con pd.get_dummies. 
4. Separar entrenamiento y prueba (test_size=0.2, random_state=42 y, si es 
clasificación, stratify=y). 
5. Entrenar y comparar al menos dos modelos dentro de un Pipeline, con 
validación cruzada. 
6. Presentar una tabla con las métricas de prueba. Clasificación: exactitud, 
precisión, recall, F1 y matriz de confusión. Regresión: MAE, RMSE y R². 
7. Elegir el mejor modelo, explicar por qué se escogió esa métrica y guardarlo con 
joblib. 
8. Crear src/usar_modelo.py que cargue el modelo y prediga al menos 3 casos 
nuevos realistas: será la demostración de la sustentación. 
9. Comparar el resultado con el perceptrón hecho a mano en el Avance 2. 
10. Explicar todo en el README y hacer commit. 
Si el proyecto trabaja con texto o recomendaciones: Texto (chatbot, tutor, PQRS): 
convertir el texto en números sencillos (cantidad de palabras, palabras clave) o usar 
TfidfVectorizer de Scikit-Learn dentro del Pipeline. 
Recomendaciones: definir algo que se pueda clasificar y medir (por ejemplo, 
«compra / no compra») y dejar la recomendación como una función adicional. 
Recomendación: Tener el modelo listo una semana antes de la sustentación, para 
dedicar el tiempo restante al informe en normas APA y a la presentación. 
 

--- Página 20 ---
20 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
8. Cierre (5 min) 
Resumen de la clase: 
• 
Con fit y predict, Scikit-Learn hace lo que en la clase del perceptrón se 
programó a mano. 
• 
Un modelo siempre se evalúa con datos de prueba que no vio; la validación 
cruzada da una medida más estable. 
• 
El Pipeline escala los datos correctamente y se guarda junto con el modelo. 
• 
La métrica se elige según qué error es más grave: precisión, recall o F1. 
• 
Las redes neuronales unen perceptrones en capas y resuelven problemas como 
XOR. 
• 
Con joblib el modelo se guarda y se usa en la demostración sin volver a 
entrenar. 
Próximas fechas: 
Fecha 
Actividad 
Lunes 16 de noviembre 
Festivo: no hay clase. 
Lunes 23 o 30 de noviembre (por 
confirmar) 
Sustentación presencial del proyecto final y entrega del 
informe en normas APA. 
 
Importante: Esta es la última clase de contenido del semestre. Las dudas se 
resuelven por los canales del curso en AVACO. 

--- Página 21 ---
21 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Anexo A: Resumen de Scikit-Learn 
Tarea 
Código 
Dividir los datos 
train_test_split(X, y, test_size=0.2, random_state=42, 
stratify=y) 
Escalar + modelo 
Pipeline([("escalado", StandardScaler()), ("modelo", 
LogisticRegression())]) 
Entrenar / predecir 
modelo.fit(X_train, y_train) / modelo.predict(X_test) 
Probabilidad 
modelo.predict_proba(X)[:, 1] 
Métricas de clasificación 
accuracy_score, precision_score, recall_score, f1_score, 
confusion_matrix 
Métricas de regresión 
mean_absolute_error, np.sqrt(mean_squared_error(...)), r2_score 
Validación cruzada 
cross_val_score(modelo, X, y, cv=5).mean() 
Guardar / cargar 
joblib.dump(modelo, "archivo.joblib") / 
joblib.load("archivo.joblib") 
Columnas de texto 
pd.get_dummies(df, columns=["columna"]) 
 
Anexo B: Así debe quedar la carpeta clase12 
clase12/ 
├── Dockerfile 
├── docker-compose.yml 
├── requirements.txt 
├── data/ 
│   ├── cultivos_cartago.csv 
│   └── rendimiento_cartago.csv    ← lo crea el Paso 3 
├── notebooks/ 
└── src/ 
    ├── clasificar_cultivos.py 
    ├── usar_modelo.py 
    ├── regresion_rendimiento.py 
    ├── red_xor.py 
    ├── profundidad_arbol.py 
    ├── modelo_cultivos.joblib      ← lo crea el Paso 1 
    ├── matriz_confusion.png 
    ├── real_vs_predicho.png 
    └── sobreajuste_arbol.png 
 
Bibliografía 
Géron, A. (2022). Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow 
(3.ª ed.). O'Reilly. 
Müller, A. C. y Guido, S. (2016). Introduction to Machine Learning with Python. O'Reilly. 
Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine 
Learning Research, 12, 2825–2830. 
