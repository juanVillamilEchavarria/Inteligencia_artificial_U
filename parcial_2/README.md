# Parcial 2 - Inteligencia Artificial - Grupo 07

**Integrantes:**
- Juan Esteban Villamil Echavarría
- Santiago Hidalgo López


**Tema:** Residuos - rutas de recolección. Predicción de `ruta_retrasada` a partir de `toneladas_recogidas` y `distancia_km`.

---

## 1. Descripción del problema

Una entidad local de Cartago necesita anticipar si una ruta de recolección de residuos terminará con retraso (`1`) o a tiempo (`0`) usando dos variables numéricas:

- `toneladas_recogidas`: toneladas recogidas en la ruta.
- `distancia_km`: distancia recorrida por la ruta.

El archivo original es `src/data/grupo_07.csv`, exportado sin depurar. El objetivo del parcial es revisar su calidad, limpiarlo, visualizar las relaciones entre variables y entrenar un perceptrón desde cero con NumPy.

---

## 2. Arquitectura del proyecto


```
parcial_2/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── data/
│   └── grupo_07_limpio.csv
└── src/
    ├── data/grupo_07.csv
    ├── parcial2.py                         # Entry point
    ├── api/
    │   └── RecorridosGateWay.py            # Acceso al CSV
    ├── app_collections/
    │   └── RecorridosCollection.py         # Colección de dominio
    ├── entities/
    │   └── Recorrido.py                    # Entidad de dominio
    ├── enums/
    │   └── RecorridoFilteringKeys.py       # Claves de filtrado
    ├── dto/
    │   ├── RecorridoNumPyDTO.py
    │   └── PerceptronTrainingDTO.py
    ├── services/
    │   ├── RecorridoStatisticsService.py   # Estadísticas en Python puro
    │   ├── NumpyStatisticsService.py       # Estadísticas con NumPy
    │   └── PerceptronService.py            # Sigmoide, pérdida, gradientes y train
    ├── pipelines/
    │   ├── transform/                      # Pipeline de preparación
    │   │   ├── DataPreparationContext.py   # Estado inmutable
    │   │   ├── DataPreparationPipeline.py  # Orquestador
    │   │   ├── DataPreparationRunner.py    # Composition root
    │   │   ├── dtos/
    │   │   │   ├── CleaningReport.py
    │   │   │   └── EdaReport.py
    │   │   └── steps/
    │   │       ├── DataPreparationStep.py
    │   │       ├── LoadDataStep.py
    │   │       ├── EdaStep.py
    │   │       ├── CleanDataStep.py
    │   │       ├── FeatureEngineeringStep.py
    │   │       └── PersistStep.py
    │   └── train/                          # Pipeline del perceptrón
    │       ├── PerceptronTrainingContext.py
    │       ├── PerceptronTrainingPipeline.py
    │       ├── PerceptronTrainingRunner.py
    │       ├── dtos/
    │       │   ├── PerceptronReport.py
    │       │   └── PredictionResult.py
    │       └── steps/
    │           ├── TrainingStep.py
    │           ├── LoadPreparedDataStep.py
    │           ├── SelectFeaturesStep.py
    │           ├── StandardizeStep.py
    │           ├── TrainPerceptronStep.py
    │           └── EvaluateStep.py
    ├── controllers/
    │   ├── RecorridoController.py
    │   ├── RecorridoGraphicsController.py
    │   └── PerceptronController.py
    ├── outputs/
    │   ├── reporting/
    │   │   └── DataQualityReportGenerator.py
    │   └── visualization/
    │       ├── SeabornChartRenderer.py
    │       └── PerceptronChartRenderer.py
    ├── helpers/
    │   ├── output_helpers.py
    │   └── project_paths.py
    ├── charts_seaborn/
    │   ├── seaborn_scatter_features_target.png
    │   └── seaborn_boxplot_distancia_objetivo.png
    └── charts_perceptron/
        ├── curva_aprendizaje.png
        └── frontera_decision.png
```

Principios aplicados:

- **SRP:** cada step, servicio y renderer tiene una única responsabilidad.
- **Estado inmutable:** contextos `@dataclass(frozen=True)` y `dataclasses.replace`.
- **DTOs tipados:** reportes y predicciones no se pasan como diccionarios sueltos.
- **Separación de capas:** servicios sin prints ni gráficos; outputs solo generan artefactos.
- **Dependency injection:** runners y controllers reciben sus dependencias.
- **Sin Scikit-Learn:** el perceptrón está implementado únicamente con NumPy.

---

## 3. Reproducción del entorno

### Con Docker

Desde `parcial_2/`:

```bash
docker compose up -d --build
docker exec -it parcial2_ia bash
cd src
python parcial2.py
exit
```

El contenedor se llama `parcial2_ia` para no chocar con `python_ia` de las clases.

Si `python_ia` está encendido:

```bash
docker stop python_ia
```

### Sin Docker

```bash
cd parcial_2/src
pip install -r ../requirements.txt
python parcial2.py
```

Dependencias declaradas en `requirements.txt`: `numpy`, `pandas`, `matplotlib` y `seaborn`.

---

## 4. Tarea 2 - Carga e inspección

Salidas obtenidas al ejecutar `python parcial2.py`:

- **Primeras 5 filas:** R001 a R005.
- **Shape:** `(84, 5)`.
- **Tipos:** `recorrido_id` y `ruta` como texto; `toneladas_recogidas` y `distancia_km` como `float64`; `ruta_retrasada` como `int64`.
- **Nulos por columna:** `distancia_km = 3`; el resto en 0. Total: 3 nulos.
- **Filas duplicadas exactas:** 4.
- **IDs duplicados:** 4 (`R019`, `R010`, `R008`, `R067`).
- **Rutas únicas:** 5.
- **Distribución por ruta:** Ruta 2 = 20, Ruta 1 = 19, Ruta 3 = 16, Ruta 5 = 15, Ruta 4 = 14.
- **Distribución del objetivo:** clase 0 = 47, clase 1 = 37.

### Pregunta clave: ¿alguna columna numérica tiene un tipo que no debería?

No. Las columnas numéricas se cargan correctamente:

- `toneladas_recogidas` y `distancia_km` son `float64` porque tienen decimales. `distancia_km` además contiene nulos, lo que obliga a Pandas a representarla como flotante.
- `ruta_retrasada` es `int64` porque solo contiene `0` y `1`.

El valor `3700.0` de `R031` no es un problema de tipo de dato: es un problema de **escala/unidades**.

---

## 5. Tarea 3 - Calidad y limpieza de datos

Se detectaron y corrigieron **4 problemas de calidad** (más los IDs duplicados asociados).

| # | Problema | ¿Cómo se detectó? | Decisión | ¿Por qué? |
|---|---|---|---|---|
| 1 | 4 filas duplicadas exactas | `df.duplicated().sum() = 4` y `df['recorrido_id'].duplicated().sum() = 4`; IDs `R008`, `R010`, `R019`, `R067` | Eliminar con `drop_duplicates(keep='first')` | Son registros idénticos; contarlos dos veces sesga promedios, clases y entrenamiento |
| 2 | 3 nulos en `distancia_km` | `df.isnull().sum()`: `distancia_km = 3`; filas `R027`, `R037`, `R071` | Imputar con la mediana: **23.9 km** | La mediana es robusta ante valores extremos y permite conservar las 3 filas |
| 3 | Distancia negativa imposible | `df[df['distancia_km'] < 0]`: `R035 = -24.4 km` | Corregir el signo a **24.4 km** | Una distancia no puede ser negativa; la magnitud es coherente con el resto de rutas |
| 4 | Tonelaje con unidades equivocadas | `df.describe()`: máximo `3700.0 t` frente al rango normal `2.3 - 15.0 t`; fila `R031` | Convertir a **3.7 t** dividiendo entre 1000 | Probablemente el sistema exportó kilogramos como toneladas. `3700 kg = 3.7 t` |

También se normalizaron espacios en las columnas de texto `recorrido_id` y `ruta`.

### Filas antes y después

| Momento | Filas | Columnas | Nulos | Clase 0 | Clase 1 |
|---|---:|---:|---:|---:|---:|
| Dataset original | 84 | 5 | 3 | 47 | 37 |
| Después de limpieza | 80 | 5 | 0 | 46 | 34 |

El dataset limpio se guarda en `data/grupo_07_limpio.csv`.

### Pregunta clave: ¿cuál fue el valor más sospechoso?

El valor más sospechoso fue **`toneladas_recogidas = 3700.0` en `R031`**.

- Media de la columna antes de corregir: **52.2762**.
- Media después de corregir: **8.1238**.
- Desviación estándar antes: **402.8127**.
- Desviación estándar después: **3.7605**.

Si no se hubiera corregido, la estandarización usaría `(x - 52.2762) / 402.8127`. Un valor normal de 8 t quedaría en `(8 - 52.2762) / 402.8127 ≈ -0.11`, y uno de 15 t en `(15 - 52.2762) / 402.8127 ≈ -0.09`. Es decir, casi todos los registros reales quedarían comprimidos en un intervalo diminuto y serían prácticamente indistinguibles para el perceptrón. El gradiente sería muy pequeño, el entrenamiento avanzaría muy lento y el modelo no aprendería a separar los retrasos.

Además, el valor extremo distorsionaba la correlación: en los datos crudos `toneladas_recogidas` vs `ruta_retrasada` era **-0.09**; después de corregir `R031`, la correlación limpia es **0.7680**. Esto muestra cómo un solo valor mal escalado puede cambiar por completo la lectura de los datos.

---

## 6. Tarea 4 - Visualización con Seaborn

### Gráfico 1: dispersión de las dos variables numéricas por clase

**Archivo:** `src/charts_seaborn/seaborn_scatter_features_target.png`

Se graficó `toneladas_recogidas` en el eje X, `distancia_km` en el eje Y y el color representa `ruta_retrasada` (`0 = a tiempo`, `1 = retraso`).

**Qué muestra:** los recorridos con retraso tienden a concentrarse en la zona de mayor tonelaje y mayor distancia. Los recorridos a tiempo se concentran en tonelajes bajos y distancias cortas.

**Conclusión:** existe una separación visual clara, pero no perfecta. Hay solapamiento en la zona media (aproximadamente 8-12 t y 20-30 km), por lo que el perceptrón no podrá clasificar todos los casos correctamente.

### Gráfico 2: boxplot de distancia por clase

**Archivo:** `src/charts_seaborn/seaborn_boxplot_distancia_objetivo.png`

Se comparó `distancia_km` entre las clases `0` y `1`.

**Qué muestra:**

| Clase | Cantidad | Distancia media | Distancia mediana | Mínimo | Máximo |
|---|---:|---:|---:|---:|---:|
| A tiempo (0) | 46 | 19.93 km | 21.6 km | 5.0 km | 37.7 km |
| Retraso (1) | 34 | 26.69 km | 26.5 km | 7.1 km | 38.9 km |

**Conclusión:** los recorridos retrasados tienen una distancia típica mayor (mediana 26.5 km frente a 21.6 km). La distancia es un indicador útil, aunque hay traslape entre las dos distribuciones.

---

## 7. Tarea 5 - Perceptrón desde cero con NumPy

### Datos de entrada

- `X`: `toneladas_recogidas` y `distancia_km`.
- `y`: `ruta_retrasada`.
- Filas de entrenamiento: **80**.
- Clase 0: **46**; clase 1: **34**.

### Estandarización

Se calculó la media y la desviación estándar de cada columna de `X` y se usó:

```
X_escalado = (X - media) / desviacion
```

Valores guardados para predecir casos nuevos:

- Media: `[8.1238, 22.8025]`.
- Desviación: `[3.7369, 9.9881]`.

### Funciones implementadas en `PerceptronService`

- `sigmoid(z) = 1 / (1 + exp(-z))`.
- `predictProbability(X, w, b) = sigmoid(X @ w + b)`.
- Pérdida logarítmica promedio con recorte `epsilon = 1e-9`.
- Exactitud con umbral `0.5`.
- Gradientes: `(X.T @ error) / n` y `mean(error)`.
- Descenso del gradiente con `learning_rate = 0.1` y `epochs = 500`.

### Resultados del entrenamiento

| Métrica | Valor |
|---|---:|
| Pesos iniciales | `w1 = 0.0000`, `w2 = 0.0000`, `b = 0.0000` |
| Pesos finales | `w1 = 3.1076`, `w2 = 1.6720` |
| Sesgo final | `b = -0.6229` |
| Pérdida inicial | `0.6931` |
| Pérdida final | `0.1845` |
| Exactitud inicial | `42.50%` |
| Exactitud final | `91.25%` |
| Exactitud de la clase mayoritaria | `57.50%` |
| Registros mal clasificados | `7 de 80` |

La pérdida bajó de `0.6931` a `0.1845` y la exactitud subió de `42.50%` a `91.25%`, superando claramente la línea base de `57.50%`.

### Gráficos

- `src/charts_perceptron/curva_aprendizaje.png`: pérdida y exactitud por época.
- `src/charts_perceptron/frontera_decision.png`: puntos de las dos clases y recta de decisión en unidades originales.

---

## 8. Tarea 6 - Interpretación de resultados

### 1. ¿Qué significa el signo de `w1` y `w2`?

Ambos pesos son positivos:

- `w1 = 3.1076` (toneladas): manteniendo constante la distancia, un mayor tonelaje recogido aumenta la probabilidad de que la ruta termine con retraso.
- `w2 = 1.6720` (distancia): manteniendo constante el tonelaje, una mayor distancia aumenta la probabilidad de retraso.

Esto tiene sentido para Cartago: las rutas que recogen más residuos y recorren más kilómetros suelen necesitar más tiempo y están más expuestas a demoras. Sin embargo, los pesos describen asociaciones del modelo, no relaciones causales.

La relación con el tonelaje es especialmente fuerte: en los datos limpios, la correlación `toneladas_recogidas` vs `ruta_retrasada` es **0.7680**. La correlación `distancia_km` vs `ruta_retrasada` es **0.3342**.

### 2. ¿Los datos son aproximadamente linealmente separables?

No son perfectamente separables. El perceptrón deja **7 registros mal clasificados de 80** (`91.25%` de exactitud). La frontera es una recta y separa bien la mayor parte de los datos, pero hay puntos de las dos clases que se solapan, especialmente en rutas intermedias.

### 3. Dos registros nuevos

| Toneladas | Distancia | Probabilidad de retraso | Clase predicha | ¿Coincide con lo esperado? |
|---:|---:|---:|---:|---|
| 5.0 | 7.0 km | `0.28%` | 0 (a tiempo) | Sí: ruta corta y poca carga |
| 13.0 | 38.0 km | `99.75%` | 1 (retraso) | Sí: ruta larga y mucha carga |

Los casos se escalaron con la media y la desviación del entrenamiento, no con sus propios valores.

### 4. Recomendación concreta para la entidad local

Priorizar el monitoreo y la planeación de las rutas largas y con mayor tonelaje. Los números del parcial lo respaldan:

- Tasa de retraso con distancia `>= 30 km`: **68.18%** (`15/22`).
- Tasa de retraso con distancia `< 30 km`: **32.76%** (`19/58`).
- Tasa global de retraso: **42.50%**.
- Correlación tonelaje vs retraso: **0.7680**; distancia vs retraso: **0.3342**.

Recomendaciones concretas:

1. Asignar más capacidad, vehículos o personal a las rutas con distancia mayor a 30 km.
2. Hacer seguimiento en tiempo real de las rutas con tonelaje alto.
3. Revisar la planeación de rutas largas para reducir traslados y tiempos muertos.
4. Usar el modelo como alerta temprana, no como decisión automática.

### 5. Limitaciones del modelo

- Solo usa **2 variables**; no incluye clima, tráfico, hora, tipo de vehículo, personal, mantenimiento ni estado de las vías.
- El dataset es pequeño (**80 registros**) y de una sola ciudad.
- No se hizo separación entrenamiento/prueba: las métricas son sobre los mismos datos de entrenamiento y pueden ser optimistas.
- El modelo es lineal; no captura relaciones no lineales ni interacciones complejas.
- La limpieza supone que `R031` estaba en kilogramos y que `R035` tenía un error de signo. Son decisiones razonables, pero siguen siendo supuestos.
- Los pesos no son relaciones causales.
- El umbral de decisión es fijo en `0.5`; no se calibró la probabilidad.
- Hay desbalance moderado de clases (46 vs 34).

---

## 9. Tarea 7 - Entregables

Archivos incluidos:

- `Dockerfile`
- `docker-compose.yml` con `container_name: parcial2_ia`
- `requirements.txt` sin Scikit-Learn
- `src/parcial2.py`
- `src/data/grupo_07.csv` (original)
- `data/grupo_07_limpio.csv` (limpio)
- `src/charts_seaborn/seaborn_scatter_features_target.png`
- `src/charts_seaborn/seaborn_boxplot_distancia_objetivo.png`
- `src/charts_perceptron/curva_aprendizaje.png`
- `src/charts_perceptron/frontera_decision.png`
- `src/eda_summary.md` (resumen EDA generado automáticamente)
- `README.md`

Para el repositorio público se recomienda registrar al menos tres commits:

```bash
git commit -m "Parcial 2: entorno Docker y estructura del proyecto"
git commit -m "Parcial 2: limpieza, EDA y visualizaciones Seaborn"
git commit -m "Parcial 2: perceptrón NumPy, interpretación y README"
```

---

## 10. Conclusión general

El ejercicio muestra que la calidad de los datos cambia por completo las conclusiones: un único valor mal escalado (`R031 = 3700.0`) distorsionaba la media (de `8.12` a `52.28`), la desviación (de `3.76` a `402.81`) y hasta el signo de la correlación entre tonelaje y retraso. Después de limpiar, el perceptrón alcanza `91.25%` de exactitud frente a `57.50%` de la clase mayoritaria, y permite identificar que las rutas más largas y con mayor tonelaje son las más propensas a retrasarse. El modelo es útil como herramienta exploratoria y de alerta temprana, pero requiere más variables y validación fuera de muestra antes de usarse para decisiones reales.
