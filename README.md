# Leo Counter AI - Inteligencia Artificial para Análisis Financiero Inteligente

## Problemática

Los usuarios de **Leo Counter** (gestor de finanzas open-source para hogares y PyMEs) registran diariamente decenas de transacciones financieras que se categorizan manualmente o mediante reglas básicas. Sin embargo, existen tres problemas que limitan la retroalimentacion de sus usuarios finales:

1. **Categorización superficial**: El sistema maneja categorías principales (Alimentación, Transporte, Entretenimiento, etc.), pero dentro de cada categoría pueden existir sub-categorías diminutas que el usuario no identifica. Por ejemplo, dentro de "Alimentación" puede haber "supermercado", "restaurantes", "cafeterías", "comida rápida", pero el usuario solo ve el total general sin comprender patrones específicos de consumo.

2. **Detección reactiva de anomalías**: Actualmente, las fugas de dinero o consumos inusuales solo se detectan cuando el usuario revisa  los reportes. No existe un sistema proactivo que alerte sobre transacciones atípicas en tiempo real (como una compra de $15,000 cuando el promedio mensual es $2,000).

3. **Reportes genéricos**: Los dashboards y analíticas actuales muestran KPIs y diferentes estadisticas (ingresos vs egresos, evolución mensual, etc.), pero no proporcionan insights accionables ni desgloses detallados adaptados al comportamiento específico de cada usuario.

Al no tener un soporte inteligente, las analiticas y reportes pueden no ser tan detallados, puntuales e interactivos, dificultando la comprension profunda del usuario final con respecto a sus estadisticas  

El proyecto se enmarca en **Cartago, Valle del Cauca**: hogares y pequeñas y medianas empresas que llevan sus finanzas en Leo Counter y necesitan entender mejor sus ingresos, gastos y patrones de consumo sin depender de una categorización manual.

---

## Estado del proyecto final (2026-2)

El repositorio cubre el ciclo completo exigido por el lineamiento:

| Componente | Estado | Dónde |
|---|---|---|
| Datos crudos y fuente documentada | ✅ 120 movimientos | `project/data/datos_originales.json` + `project/data/README.md` |
| Preparación con Pandas | ✅ | `project/src/data_preparation.py` |
| Perceptrón desde cero con NumPy | ✅ con división train/test | `project/src/perceptron_proyecto.py` |
| Comparación de modelos de Scikit-Learn | ✅ 3 modelos + GridSearchCV | `project/src/modelo_proyecto.py` |
| Predicción de casos nuevos sin reentrenar | ✅ | `project/src/usar_modelo.py` |
| Interfaz de valor agregado | ✅ menú en consola con Rich (colores, tablas y barras de probabilidad) | `project/src/interfaz_consola.py` |
| Gráficos de análisis y evaluación | ✅ 10 Seaborn + 2 perceptrón + 4 evaluación | `project/src/charts*` |

### Resultados principales (conjunto de prueba, 30 filas)

| Modelo | Exactitud | Precisión | Recall | F1 macro | F1 Ingreso | ROC-AUC | CV F1 macro |
|---|---:|---:|---:|---:|---:|---:|---:|
| Regresión logística | 0.7333 | 0.5000 | 0.7500 | 0.7000 | 0.6000 | 0.8693 | 0.6924 |
| **Random Forest (GridSearchCV)** | **0.8667** | **0.8333** | 0.6250 | **0.8137** | **0.7143** | **0.9318** | **0.7683** |
| Red neuronal (MLP) | 0.7667 | 0.5714 | 0.5000 | 0.6889 | 0.5333 | 0.7614 | 0.7330 |

**Mejor modelo:** `Random Forest (GridSearchCV)` con `max_depth=3`, `min_samples_leaf=1` y `n_estimators=200`, seleccionado por **F1 macro de validación cruzada** (no por el conjunto de prueba). Se guarda en `project/src/modelo_final.joblib` y sus métricas en `project/src/modelo_metricas.json`.

**Informe final (APA 7):** [`project/Informe_Final_Grupo05_LeoCounterAI.docx`](project/Informe_Final_Grupo05_LeoCounterAI.docx) (la versión PDF se entrega en AVACO).

**Integrantes:** Juan Esteban Villamil Echavarría y Santiago Hidalgo López.

### Ejecución rápida con Docker

```bash
cd project
docker compose build

# 1) Preparar datos, EDA y gráficos
docker compose run --rm app python src/data_preparation.py

# 2) Perceptrón desde cero
docker compose run --rm app python src/perceptron_proyecto.py

# 3) Comparar modelos y guardar el mejor
docker compose run --rm app python src/modelo_proyecto.py

# 4) Predecir casos nuevos sin reentrenar
docker compose run --rm app python src/usar_modelo.py

# 5) Interfaz interactiva (menú en consola con Rich)
docker compose run --rm -it app python src/interfaz_consola.py
```

---

## Estructura del Proyecto

```
project/
├── data/
│   ├── datos_originales.json        # 120 movimientos crudos (UUID v7 únicos)
│   ├── proyecto_limpio.csv          # Dataset limpio exportado por el pipeline
│   └── README.md                    # Fuente, diccionario y calidad de los datos
└── src/
    ├── main.py                          # Entry point: estadísticas financieras básicas
    ├── eda_proyectos.py                 # Entry point: EDA con NumPy + gráficos Matplotlib
    ├── data_preparation.py              # Entry point: pipeline completo de preparación
    ├── perceptron_proyecto.py           # Entry point: perceptrón desde cero (Avance 2)
    ├── modelo_proyecto.py               # Entry point: comparación de modelos + joblib
    ├── usar_modelo.py                   # Entry point: carga el modelo y predice
    ├── interfaz_consola.py              # Valor agregado: menú interactivo con Rich
    ├── modelo_final.joblib              # Mejor modelo serializado
    ├── modelo_metricas.json             # Métricas legibles del modelo
    │
    ├── api/                             # Acceso a datos
    │   └── MovementsGateWay.py          # Lee data/datos_originales.json (futuro: API real)
    │
    ├── entities/                        # Entidades de dominio
    │   └── Movement.py                  # Movimiento financiero
    │
    ├── app_collections/                 # Colecciones de dominio
    │   └── MovementsCollection.py       # Colección tipada con filtrado por Enum
    │
    ├── enums/                           # Value Objects
    │   ├── MovementFilteringKeys.py     # Claves de filtrado
    │   └── ModelColumns.py              # Variables de entrada y objetivo del modelo
    │
    ├── dto/                             # DTOs compartidos
    │   ├── MovementNumPyDTO.py          # Stats NumPy
    │   ├── PerceptronTrainingDTO.py     # Pesos, sesgo e historial de entrenamiento
    │   └── CandidateModel.py            # Nombre + Pipeline de Scikit-Learn
    │
    ├── services/                        # Lógica de negocio pura (cálculos)
    │   ├── StatisticsService.py         # Estadísticas con Python puro
    │   ├── NumpyStatisticsService.py    # Estadísticas con NumPy (EDA)
    │   ├── PerceptronService.py         # Sigmoide, pérdida, gradientes y fit (NumPy puro)
    │   ├── SklearnModelService.py       # Modelos, GridSearchCV, CV y métricas
    │   └── ModelPersistenceService.py   # Guardado y carga con joblib + JSON
    │
    ├── pipelines/
    │   ├── transform/                   # Pipeline de preparación de datos
    │   │   ├── DataPreparationPipeline.py   # Orquestador
    │   │   ├── DataPreparationRunner.py     # Composition root
    │   │   ├── DataPreparationContext.py    # Estado inmutable
    │   │   ├── steps/
    │   │   │   ├── DataPreparationStep.py       # ABC
    │   │   │   ├── LoadDataStep.py              # Carga vía Gateway
    │   │   │   ├── EdaStep.py                   # Genera EdaReport
    │   │   │   ├── CleanDataStep.py             # Limpieza + CleaningReport
    │   │   │   ├── FeatureEngineeringStep.py    # monto_log, es_ingreso, mes...
    │   │   │   ├── EncodingStep.py              # pd.get_dummies()
    │   │   │   └── PersistStep.py               # Guarda data/proyecto_limpio.csv
    │   │   └── dtos/
    │   │       ├── EdaReport.py
    │   │       └── CleaningReport.py
    │   ├── train/                       # Pipeline de entrenamiento del perceptrón
    │   │   ├── PerceptronTrainingPipeline.py    # Orquestador
    │   │   ├── PerceptronTrainingRunner.py      # Composition root
    │   │   ├── PerceptronTrainingContext.py     # Estado inmutable
    │   │   ├── steps/
    │   │   │   ├── TrainingStep.py              # ABC
    │   │   │   ├── LoadPreparedDataStep.py      # Carga el CSV preparado
    │   │   │   ├── SelectFeaturesStep.py        # Target + dos entradas
    │   │   │   ├── SplitDataStep.py             # División train/test estratificada
    │   │   │   ├── StandardizeStep.py           # Estandarización solo con train
    │   │   │   ├── TrainPerceptronStep.py       # Descenso del gradiente
    │   │   │   └── EvaluateStep.py              # Pesos, pérdida y exactitud
    │   │   └── dtos/
    │   │       ├── PerceptronReport.py
    │   │       └── PredictionResult.py
    │   └── model/                       # Pipeline de comparación de modelos
    │       ├── ModelTrainingPipeline.py         # Orquestador
    │       ├── ModelTrainingRunner.py           # Composition root
    │       ├── ModelTrainingContext.py          # Estado inmutable
    │       ├── steps/
    │       │   ├── ModelTrainingStep.py         # ABC
    │       │   ├── LoadPreparedDataStep.py      # Carga el CSV preparado
    │       │   ├── SelectFeaturesStep.py        # Features sin fuga de información
    │       │   ├── SplitDataStep.py             # División train/test
    │       │   ├── BuildCandidateModelsStep.py  # LR, Random Forest y MLP
    │       │   ├── TuneRandomForestStep.py      # GridSearchCV
    │       │   ├── TrainAndEvaluateModelsStep.py# Métricas + CV
    │       │   ├── SelectBestModelStep.py       # Mejor F1 macro de CV
    │       │   ├── PersistModelStep.py          # modelo_final.joblib + JSON
    │       │   └── BuildModelReportStep.py      # Reporte final
    │       └── dtos/
    │           ├── ModelScore.py
    │           ├── ModelReport.py
    │           └── ModelPredictionResult.py
    │
    ├── outputs/                         # Generadores de artefactos (sin lógica de negocio)
    │   ├── visualization/
    │   │   ├── MatplotlibChartRenderer.py       # Gráficos Matplotlib → src/charts/
    │   │   ├── SeabornChartRenderer.py          # Gráficos Seaborn → src/charts_seaborn/
    │   │   ├── PerceptronChartRenderer.py       # Curva y frontera → src/charts_perceptron/
    │   │   └── EvaluationChartRenderer.py       # Evaluación → src/charts_modelos/
    │   └── reporting/
    │       ├── FinancialReportGenerator.py
    │       └── EdaReportGenerator.py
    │
    ├── controllers/                     # Fachadas hacia los entry points
    │   ├── MovementController.py
    │   ├── MovementGraphicsController.py
    │   ├── PerceptronController.py
    │   └── ModelController.py           # Entrena, carga y predice con sklearn
    │
    └── helpers/
        ├── output_helpers.py            # print_separator() para CLI
        └── project_paths.py             # Rutas canónicas del proyecto
```

**Principios de la arquitectura:**
- **services/**: solo lógica de negocio (cálculos estadísticos y matemática del perceptrón). Sin prints ni generación de artefactos.
- **outputs/**: generadores de artefactos (imágenes, reportes). Reciben datos ya procesados.
- **pipelines/**: flujos descompuestos en steps atómicos y extensibles, con estado compartido **inmutable** (`@dataclass(frozen=True)` + `dataclasses.replace`) y resultados en **DTOs tipados**.
- **controllers/**: fachadas simples que desacoplan los entry points de los services.
- **Sin fuga de información**: el escalado vive dentro del `Pipeline` de Scikit-Learn y la media/desviación del perceptrón se calcula solo con `train`. El conjunto de prueba se usa una única vez para reportar.
- **Selección honesta**: el mejor modelo se elige por **F1 macro de validación cruzada**, no por el resultado en prueba.

---

## Datos

### Diccionario de variables

El archivo real del proyecto es **`project/data/datos_originales.json`**:

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `id` | texto | Identificador único UUID v7 (sin repeticiones) | `01a16a35-9daa-7678-9d67-e162dc8c9b7f` |
| `nombre` | texto | Nombre corto del movimiento | `Compra de mercado` |
| `cuenta` | texto | Cuenta o medio de pago | `Nequi` |
| `categoria` | texto | Categoría principal | `Alimentación` |
| `tipo_movimiento` | texto | `Ingreso` o `Gasto` | `Gasto` |
| `monto` | texto numérico | Monto en pesos colombianos (COP) | `125000.00` |
| `fecha` | texto ISO | Fecha del movimiento | `2024-03-15` |
| `descripcion` | texto | Descripción en lenguaje natural | `Mercado semanal en D1` |

### Origen de los datos

Los datos provienen del **sistema Leo Counter** (gestor de finanzas personales para hogares y PyMEs). Para el proyecto se usa una muestra **anonimizada y ampliada con movimientos sintéticos coherentes**: 120 transacciones (86 gastos y 34 ingresos) entre marzo de 2024 y septiembre de 2026, con montos, cuentas, categorías y descripciones realistas. No contienen información personal real.

El detalle de la fuente, la calidad y la estructura está en **`project/data/README.md`**. El acceso a datos está aislado en `src/api/MovementsGateWay.py`, de modo que en el futuro se puede reemplazar el archivo JSON por la API real de Leo Counter sin cambiar el resto del sistema.

---

## Objetivo

### Objetivo general

Construir y evaluar un prototipo reproducible de inteligencia artificial que clasifique los movimientos financieros de **Leo Counter** como **Ingreso** o **Gasto**, usando un perceptrón implementado desde cero con NumPy y modelos de Scikit-Learn integrados en un `Pipeline`.

### Objetivos específicos (implementados)

1. **Preparar los datos**: limpiar y documentar 120 movimientos, crear variables derivadas (`monto_log`, `mes`, `dia_semana`, `es_fin_semana`, `es_ingreso`) y exportar un dataset listo para aprendizaje automático (`data/proyecto_limpio.csv`).
2. **Entender el modelo por dentro**: implementar un perceptrón con sigmoide, pérdida logarítmica y descenso del gradiente usando solo NumPy, con división entrenamiento/prueba y estandarización calculada únicamente con entrenamiento.
3. **Comparar modelos de Scikit-Learn**: regresión logística, Random Forest (optimizado con `GridSearchCV`) y red neuronal `MLPClassifier`, con validación cruzada estratificada y **F1 macro** como métrica principal, dado el desbalance de clases.
4. **Usar el modelo sin reentrenar**: serializar el mejor modelo con `joblib` y usarlo desde `usar_modelo.py` y desde una interfaz de consola con **Rich**, todo reproducible con Docker.

### Alcance y trabajo futuro

La versión entregada resuelve la **clasificación binaria Ingreso/Gasto** a partir del monto y del calendario. Las ideas iniciales del proyecto quedan como **trabajo futuro**:

- **Clasificación semántica de sub-categorías** (por ejemplo, Naive Bayes multinomial o TF-IDF sobre la `descripcion`) para pasar de "Alimentación" a "supermercado", "restaurantes" o "cafeterías".
- **Detección de anomalías** con Puntaje Z calculado por separado para ingresos y gastos (el EDA ya muestra que un umbral global generaría falsos positivos).
- **Reportes enriquecidos y alertas** integrados a Leo Counter, con confirmación humana de cada predicción y registro de correcciones para reentrenar.

**Resultado final**: un primer componente inteligente para Leo Counter que sugiere la clase de cada movimiento con una probabilidad interpretable, y una base de código por capas (pipelines, servicios y controladores) sobre la que se pueden agregar los modelos futuros.

## Análisis Exploratorio de Datos (EDA)

### Variables Analizadas

Se analizaron las siguientes variables del dataset de **120 transacciones financieras**:

- **`monto`** (numérica continua): Valor de cada transacción en pesos colombianos (COP).
- **`tipo_movimiento`** (categórica binaria): Clasifica cada transacción como "Ingreso" o "Gasto".
- **`categoria`** (categórica nominal): Categoría principal asignada a cada movimiento.

### Estadísticas Calculadas con NumPy

| Métrica | Ingresos | Gastos | Todos los montos |
|---------|----------|--------|-----------------|
| Cantidad | 34 | 86 | 120 |
| Suma total | $99,006,100.00 | $37,661,800.00 | $136,667,900.00 |
| Media | $2,911,944.12 | $437,927.91 | $1,138,899.17 |
| Mediana | $2,750,000.00 | $165,000.00 | $250,000.00 |
| Desv. Estándar | $4,252,897.38 | $615,382.25 | $2,557,255.32 |
| Mínimo | $91,000.00 | $5,000.00 | $5,000.00 |
| Máximo | $25,000,000.00 | $3,500,000.00 | $25,000,000.00 |

### Patrones y Relaciones Observadas

1. **Asimetría extrema por outliers**: La media de todos los montos ($1.14M) es más de cuatro veces la mediana ($250K). La venta de vehículo ($25M) y la matrícula ($2.5M) jalan el promedio hacia arriba, lo que confirma la necesidad de **`monto_log`** y de umbrales separados por tipo de movimiento.

2. **Ingresos más dispersos que gastos**: La desviación estándar de ingresos ($4.25M) es casi siete veces la de gastos ($615K). Los ingresos incluyen salarios mensuales estables y eventos extraordinarios; los gastos son más predecibles.

3. **Distribución sesgada a la derecha**: El histograma muestra que la mayoría de transacciones se concentran en montos bajos (< $500K), con una cola larga hacia valores altos. La transformación logarítmica reduce la asimetría de 7.10 a -0.05.

4. **Categorías con alta variabilidad**: "Vivienda", "Nómina" y "Servicios Públicos" concentran la mayor cantidad de movimientos; "Tecnología" y "Educación" presentan los montos más altos y dispersos, mientras que "Transporte" tiene los más bajos y consistentes.

5. **Desbalance de clases**: 86 gastos (71.7 %) frente a 34 ingresos (28.3 %). Por eso el modelado usa `class_weight='balanced'`, validación cruzada estratificada y **F1 macro** como métrica principal.

### Impacto en el Modelo de IA

1. **Puntaje Z**: La alta desviación estándar en ingresos confirma que el umbral de detección de anomalías debe ser calculado por separado para ingresos y gastos. Un umbral global generaría falsos positivos.

2. **Naive Bayes**: La variedad de descripciones asociadas a montos similares sugiere que el modelo de clasificación semántica encontrará patrones útiles en el texto libre para diferenciar sub-categorías.

3. **Preprocesamiento**: Se recomienda aplicar normalización logarítmica a los montos antes de alimentar modelos de ML, dada la asimetría de la distribución.

### Gráficos Generados

| Gráfico | Archivo | Descripción |
|---------|---------|-------------|
| Histograma de montos | `src/charts/histograma_montos.png` | Distribución de todos los montos con líneas de media y mediana |
| Dispersión monto vs tipo | `src/charts/dispersion_monto_tipo.png` | Relación entre monto y tipo de movimiento |
| Boxplot por categoría | `src/charts/boxplot_gastos_categoria.png` | Distribución de gastos por categoría |

---

## Preparación de Datos

Esta sección documenta el pipeline completo de preparación de datos implementado siguiendo la arquitectura por servicios del proyecto, utilizando **Pandas** para manipulación y **Seaborn** para visualización.

### Ejecución del Pipeline

```bash
cd project
python src/data_preparation.py
```

### 1. Limpieza de Datos y Tabla Antes / Después

**Hallazgo**: El dataset original tiene **120 transacciones y 8 columnas**, sin valores nulos, sin filas duplicadas exactas y con **120 IDs UUID v7 únicos** (sin repeticiones).

**Estrategia implementada en `CleanDataStep`**:
- **Normalización de texto**: `strip()` y colapso de espacios en `id`, `nombre`, `cuenta`, `categoria`, `tipo_movimiento` y `descripcion`. Esto corrigió el valor `'Banco Bogota '`.
- **Tipos**: `monto` se convierte a numérico y `fecha` a `datetime` con `errors='coerce'`.
- **Valores imposibles**: se descartan filas con fechas inválidas o montos no numéricos/no positivos, y se reporta cuántas se eliminaron (0 en este dataset).
- **Duplicados**: se aplica `drop_duplicates()` y se reporta el número eliminado (0 en este dataset).
- **Nulos**: imputación con **mediana** para variables numéricas y **moda** para categóricas (0 en este dataset).
- **Outliers**: **no se eliminan**. Se conservan 18 transacciones (15 %) y se usa `monto_log` para reducir su impacto, porque corresponden a eventos reales como la venta de un vehículo ($25M) y una matrícula.

**Tabla antes / después**:

| Momento | Filas | Columnas | Nulos |
|---------|------:|---------:|------:|
| Dataset original | 120 | 8 | 0 |
| Después de limpieza | 120 | 8 | 0 |
| Después de preparación | 120 | 39 | 0 |

**Justificación**: La mediana se prefiere sobre la media para variables financieras debido a la alta asimetría (skewness = 7.10) y a los outliers extremos, que distorsionan la media.

### 2. Variables Categóricas Codificadas

**Método**: `pd.get_dummies()` (One-Hot Encoding) aplicado en `EncodingStep`.

| Variable Original | Cardinalidad | Columnas Dummy Generadas | Prefijo |
|-------------------|--------------|--------------------------|---------|
| `categoria` | 13 únicas | 13 | `categoria_` |
| `tipo_movimiento` | 2 (Ingreso/Gasto) | 2 | `tipo_movimiento_` |
| `cuenta` | 11 únicas | 11 | `cuenta_` |
| **Total** | — | **26 columnas dummy** | — |

**Dataset final**: 120 filas × 39 columnas (8 originales + 5 derivadas + 26 dummies).

**Ejemplos de columnas generadas**:
- `categoria_Alimentación`, `categoria_Transporte`, `categoria_Otros Ingresos`, ...
- `tipo_movimiento_Gasto`, `tipo_movimiento_Ingreso`
- `cuenta_Banco Bogota`, `cuenta_Nequi`, `cuenta_Bancolombia`, ...

### 3. Columnas Derivadas Creadas

| Columna | Tipo | Fórmula / Lógica | Propósito |
|---------|------|------------------|-----------|
| `monto_log` | Numérica continua | `np.log1p(monto)` | **Normalización para ML**: reduce asimetría extrema (skew 7.10 → -0.05), estabiliza varianza y mejora la convergencia |
| `es_ingreso` | Binaria (0/1) | `(tipo_movimiento == 'Ingreso').astype(int)` | **Variable objetivo**: clasificación binaria Ingreso/Gasto |
| `mes` | Numérica discreta (1-12) | `fecha.dt.month` | **Estacionalidad**: patrones mensuales |
| `dia_semana` | Numérica discreta (0-6) | `fecha.dt.dayofweek` (Lun=0) | **Patrones semanales** |
| `es_fin_semana` | Binaria (0/1) | `(dia_semana >= 5).astype(int)` | **Feature conductual** |

**Impacto en modelos futuros**:
- `monto_log`: esencial para **Puntaje Z** (asume normalidad) y **Naive Bayes** (Gaussiano).
- `es_ingreso`: target natural para clasificación binaria y para el perceptrón del Avance 2.
- `es_fin_semana` + `mes`: features temporales para reportes enriquecidos.

### 4. Hallazgos de las Visualizaciones Seaborn

Se generaron **10 gráficos** en `project/src/charts_seaborn/`:

| Gráfico | Archivo | Hallazgo Principal |
|---------|---------|-------------------|
| **Histograma Monto** | `seaborn_histograma_monto.png` | Distribución **extremadamente sesgada a derecha** (cola larga). Mayoría de transacciones < $500K. Outliers visibles > $5M. |
| **Histograma Log(Monto)** | `seaborn_histograma_monto_log.png` | La transformación log **normaliza la distribución** (aprox. gaussiana), validando `monto_log` para modelos paramétricos. |
| **Boxplot por Categoría** | `seaborn_boxplot_categoria.png` | **Alta variabilidad inter-categoría**: "Otros Ingresos" e "Independiente" tienen medianas altas y outliers; "Transporte" y "Entretenimiento" son bajos y consistentes. |
| **Boxplot por Tipo** | `seaborn_boxplot_tipo.png` | **Ingresos**: mediana **$2,750,000**, outliers hasta $25M. **Gastos**: mediana **$165,000**, outliers hasta $3.5M. Confirma la necesidad de **umbrales Z-score separados**. |
| **Scatter Fecha vs Monto** | `seaborn_scatter_monto_fecha.png` | **Eventos puntuales**: junio 2024 muestra un clúster de transacciones (con **30 transacciones** en el mes más activo). La venta de vehículo de agosto 2026 ($25M) es un outlier temporal claro. |
| **Regresión Log(Monto) vs Tiempo** | `seaborn_regplot_monto_log_fecha.png` | **Tendencia ligeramente positiva** en log-monto a lo largo del tiempo. |
| **Barplot Categoría × Tipo** | `seaborn_barplot_categoria_tipo.png` | **Asimetría categórica**: "Otros Ingresos" domina ingresos; "Otros Gastos", "Servicios Públicos" y "Vivienda" lideran gastos. "Independiente" aparece en ambos. |
| **Heatmap Correlación** | `seaborn_correlation_heatmap.png` | **Correlaciones clave**: `monto` ↔ `monto_log` (**0.604**), `es_ingreso` ↔ `monto_log` (**0.551**), `es_ingreso` ↔ `monto` (**0.438**), `es_fin_semana` ↔ `monto` (**0.009**). |
| **Scatter Entradas × Target** | `seaborn_scatter_features_target.png` | Relaciona directamente `monto_log` y `mes` con `es_ingreso`. Los ingresos tienden a concentrarse en montos más altos. Es el gráfico de soporte del perceptrón. |
| **Pairplot** | `seaborn_pairplot.png` | **Separación visual** Ingreso/Gasto en `monto_log`. `es_fin_semana` no discrimina montos. |

### 5. Hallazgos Relevantes para el Proyecto

1. **Outliers críticos detectados**: **18 transacciones (15%)** son outliers por IQR sobre **120 registros**. La venta de vehículo ($25M) y la matrícula ($2.5M) son **eventos atípicos reales**, no errores. El **Puntaje Z debe usar umbrales por tipo de movimiento**.

2. **Asimetría extrema corregida**: `monto_log` reduce skewness de **7.10 → -0.05**, haciendo los datos aptos para modelos que asumen normalidad.

3. **Desbalance de clases**: **71.7% Gastos / 28.3% Ingresos** (86 gastos / 34 ingresos). El perceptrón obtiene 81.11% de exactitud en train y 76.67% en test frente a la clase mayoritaria; en Scikit-Learn se compararon modelos con validación cruzada estratificada.

4. **Cardinalidad moderada en `cuenta`**: Se unificaron cuentas a **11 entidades únicas** tras limpieza para evitar overfitting.

5. **Patrón temporal**: junio 2024 concentra la mayor actividad financiera (**30 transacciones**). La feature `mes` captura esto para alertas estacionales.

6. **Fin de semana no es predictor**: `es_fin_semana` tiene correlación **0.009** con monto.

### 6. Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `data/proyecto_limpio.csv` | Dataset completo listo para ML (**120 × 39**) |
| `src/eda_summary.md` | Resumen EDA de los 120 registros + tabla antes/después |
| `src/charts_seaborn/*.png` | 10 gráficos Seaborn |
| `src/charts_perceptron/curva_aprendizaje.png` | Pérdida y exactitud por época (perceptrón) |
| `src/charts_perceptron/frontera_decision.png` | Frontera de decisión del perceptrón |
| `src/charts_modelos/*.png` | Gráficos de evaluación de Scikit-Learn (Matriz de confusión, Curva ROC, etc.) |
| `src/modelo_final.joblib` | Modelo entrenado serializado (Random Forest / GridSearchCV) |
| `src/modelo_metricas.json` | Métricas y parámetros del mejor modelo |

### 7. Arquitectura de Servicios Utilizada

El pipeline respeta la arquitectura por capas del proyecto:

```
src/
├── api/MovementsGateWay.py                    # Data Access (JSON → Collection)
├── app_collections/MovementsCollection.py     # Domain Collection + to_dataframe()
├── entities/Movement.py                       # Domain Entity
├── pipelines/transform/                       # Pipeline de preparación
│   ├── DataPreparationPipeline.py             # Orquestador
│   ├── DataPreparationRunner.py               # Composition root
│   ├── DataPreparationContext.py              # Estado inmutable
│   ├── steps/                                 # Un step por responsabilidad (SRP)
│   │   ├── LoadDataStep.py
│   │   ├── EdaStep.py
│   │   ├── CleanDataStep.py
│   │   ├── FeatureEngineeringStep.py
│   │   ├── EncodingStep.py
│   │   └── PersistStep.py
│   └── dtos/
│       ├── EdaReport.py
│       └── CleaningReport.py
├── pipelines/train/                           # Pipeline del perceptrón
│   ├── PerceptronTrainingPipeline.py
│   ├── PerceptronTrainingRunner.py
│   ├── PerceptronTrainingContext.py
│   ├── steps/
│   └── dtos/
├── services/PerceptronService.py               # Matemática pura con NumPy
├── outputs/visualization/PerceptronChartRenderer.py
├── controllers/PerceptronController.py
├── data_preparation.py                        # Entry point de preparación
└── perceptron_proyecto.py                     # Entry point del perceptrón
```

**Principios aplicados**:
- **SRP**: cada step tiene una única responsabilidad; el modelo matemático vive en `PerceptronService` y los gráficos en su propio renderer.
- **Dependency Injection**: runner y controller reciben sus dependencias por constructor.
- **Single Source of Truth**: `MovementsGateWay` es la única fuente de datos crudos.
- **Estado inmutable**: los contextos son `@dataclass(frozen=True)` y cada step devuelve una copia con `dataclasses.replace`.
- **DTOs tipados**: los resultados no se pasan como diccionarios sueltos.

---

## Proyecto Final: Modelos Scikit-Learn e Interfaz de Consola

Esta sección resume los entregables consolidados del proyecto final: dataset ampliado a **120 registros** con IDs únicos UUID v7, análisis visual Seaborn, perceptrón entrenado con NumPy, pipeline de clasificación con modelos Scikit-Learn (Regresión Logística, Random Forest con GridSearchCV y MLPClassifier), script de predicción `usar_modelo.py` e interfaz interactiva por consola.

### 1. Ajustes y calidad de datos (120 registros)

- Dataset ampliado a **120 transacciones** (50 originales + 70 nuevos registros coherentes: 86 gastos / 34 ingresos, con fechas entre 2024-03-15 y 2026-09-25).
- Se regeneraron los **IDs como UUID v7 únicos** (120 IDs sin repetición para 120 transacciones), sin alterar montos, fechas, cuentas, categorías ni descripciones.
- Se normalizaron espacios en columnas de texto; por ejemplo, `'Banco Bogota '` pasó a `'Banco Bogota'`.
- Se verificó que no hay nulos, filas duplicadas exactas, montos no positivos ni fechas inválidas.
- Se conservaron los **18 outliers** (15%) porque son eventos financieros reales; `monto_log` reduce su influencia.
- El dataset limpio se exporta a **`project/data/proyecto_limpio.csv`** (120 filas × 39 columnas).

### 2. Perceptrón implementado (NumPy)

- **Variable objetivo**: `es_ingreso` (1 = Ingreso, 0 = Gasto).
- **Entradas**: `monto_log` y `mes`, estandarizadas **solo con la media y desviación del conjunto de entrenamiento** (sin fuga de información del test).
- **Modelo**: sigmoide + pérdida logarítmica + descenso del gradiente, implementado únicamente con **NumPy** (sin Scikit-Learn).
- **Entrenamiento**: 90 filas de train (de 120), `learning_rate = 0.1`, 500 épocas; evaluación separada sobre 30 filas de test.
- **Pipeline**: `pipelines/train/` con steps atómicos (`LoadPreparedDataStep`, `SelectFeaturesStep`, `SplitDataStep`, `StandardizeStep`, `TrainPerceptronStep`, `EvaluateStep`).
- **Gráficos**: `src/charts_perceptron/curva_aprendizaje.png` y `src/charts_perceptron/frontera_decision.png`.

### 3. Resultados del perceptrón

| Métrica | Valor |
|---|---:|
| Filas de entrenamiento | 90 |
| Filas de prueba | 30 |
| Clase 0 (Gasto) train | 64 |
| Clase 1 (Ingreso) train | 26 |
| Pesos finales | `w1 = 1.6713`, `w2 = -0.2344` |
| Sesgo | `b = -1.3967` |
| Pérdida inicial | 0.6931 |
| Pérdida final (train) | 0.4203 |
| Pérdida final (test) | 0.3893 |
| Exactitud inicial | 28.89% |
| Exactitud final (train) | 81.11% |
| Exactitud final (test) | 76.67% |
| Exactitud de la clase mayoritaria (test) | 73.33% |

**Interpretación**:
- `w1 > 0`: a mayor `monto_log`, mayor probabilidad de que el movimiento sea un ingreso.
- `w2 < 0`: dentro de este dataset, los meses más avanzados del año se asocian levemente con mayor probabilidad de gasto.
- `b < 0`: con montos bajos el modelo tiende a predecir gasto.
- El modelo supera la línea base (76.67% en test vs 73.33% de la clase mayoritaria), pero los datos no son perfectamente separables: hay gastos altos que se confunden con ingresos.
- El split 75/25 con estandarización entrenada solo en train permite evaluar el rendimiento real del modelo sin sobreestimar con datos vistos.

### 4. Predicción de casos nuevos

| Monto | Mes | Probabilidad de ingreso | Decisión |
|---:|---:|---:|---|
| $8.000 | 6 | 0.83% | Gasto |
| $3.500.000 | 4 | 75.48% | Ingreso |
| $250.000 | 5 | 18.98% | Gasto |

### 5. Modelos Scikit-Learn (entregable final)

Sobre el mismo dataset (120 registros, features `monto_log`, `mes`, `dia_semana` y `es_fin_semana`) se implementó el pipeline `pipelines/model/` con split 75/25 estratificado, validación cruzada `StratifiedKFold(5)` y `scoring='f1_macro'`:

| Modelo | Exactitud | F1 macro | ROC-AUC | F1 media CV |
|---|---:|---:|---:|---:|
| Regresión logística (`class_weight='balanced'`) | 0.7333 | 0.7000 | 0.8693 | 0.6924 |
| **Random Forest (GridSearchCV)** | **0.8667** | **0.8137** | **0.9318** | **0.7683** |
| Red neuronal (MLP) `(16, 8)`, solver `lbfgs` | 0.7667 | 0.6889 | 0.7614 | 0.7330 |

**Mejor modelo**: **Random Forest** con `max_depth=3, min_samples_leaf=1, n_estimators=200` (seleccionado por F1 macro de validación cruzada). Artefactos: `src/modelo_final.joblib`, `src/modelo_metricas.json` y gráficos en `src/charts_modelos/`.

### 6. Interfaz de consola y uso del modelo

- **`usar_modelo.py`**: carga `modelo_final.joblib` (con el scaler y las features serializadas) y predice sobre transacciones nuevas.
- **`interfaz_consola.py`**: interfaz de consola construida con **Rich**: predice movimientos personalizados (acepta montos como `250.000`), muestra la probabilidad con una barra de color y un nivel de confianza, prueba un lote de ejemplo, compara los modelos (resaltando el mejor valor de cada métrica y la matriz de confusión) y explica el modelo por dentro (hiperparámetros e importancia de cada variable).

### 7. Cómo ejecutar con Docker

El `Dockerfile` instala las dependencias como root antes de cambiar a `USER app`, y el `docker-compose.yml` habilita `stdin_open`/`tty` para la interfaz interactiva. Desde la carpeta `project/`:

```bash
# Construir la imagen (solo la primera vez o si cambian dependencias)
docker compose build

# 1) Generar el dataset limpio, el resumen EDA y los gráficos Seaborn
docker compose run --rm app python src/data_preparation.py

# 2) Entrenar el perceptrón y generar sus gráficos
docker compose run --rm app python src/perceptron_proyecto.py

# 3) Entrenar los modelos Scikit-Learn y serializar el mejor
docker compose run --rm app python src/modelo_proyecto.py

# 4) Predecir una transacción nueva con el modelo final
docker compose run --rm app python src/usar_modelo.py

# 5) Menú interactivo (requiere tty)
docker compose run --rm -it app python src/interfaz_consola.py
```

También se puede ejecutar sin Docker desde `project/`:

```bash
python3 src/data_preparation.py
python3 src/perceptron_proyecto.py
python3 src/modelo_proyecto.py
python3 src/usar_modelo.py
python3 src/interfaz_consola.py
```

El perceptrón y los modelos Scikit-Learn requieren que exista `data/proyecto_limpio.csv`; si no existe, los scripts indican que se debe ejecutar primero `data_preparation.py`.

---

## Conclusiones del Aprendizaje beta de neuronas

Durante el entrenamiento de neuronas artificiales (`clase_8/src/main.py` y `clase_8/src/neuronas_logicas.py`) se implementó un **perceptrón simple** con función de activación **escalón** y la regla de aprendizaje del perceptrón (`peso += tasa_aprendizaje * error * entrada`), partiendo de parámetros iniciales `w1 = 0.5`, `w2 = 0.5`, `b = -0.7` y una **tasa de aprendizaje de 0.1**.

### Resultados del entrenamiento

| Compuerta | Épocas necesarias | Parámetros finales | ¿Convergió? |
|-----------|-------------------|--------------------|-------------|
| AND | 1 | `w1=0.5, w2=0.5, b=-0.7` (sin cambios) | Sí |
| OR | 2 | `w1=0.6, w2=0.6, b=-0.5` | Sí |
| NOT | 16 | `w1=-0.2, b=0.1` | Sí |
| XOR | Nunca | — | No |

### ¿Cuántas épocas necesitó cada compuerta para aprender?

- **AND: 1 época.** Los parámetros iniciales ya resuelven esta compuerta desde el arranque: `z(0,0) = -0.7 → 0`, `z(0,1) = -0.2 → 0`, `z(1,0) = -0.2 → 0`, `z(1,1) = +0.3 → 1`. El error total es 0 en la primera época y no se realiza ningún ajuste.
- **OR: 2 épocas.** En la época 1 falla en las entradas `(0,1)` y `(1,0)` (error total = 2), porque `z = -0.2` queda justo debajo del umbral. Tras subir los pesos y el bias converge con `w1 = w2 = 0.6, b = -0.5`.
- **NOT: 16 épocas.** El error oscila en un patrón `1, 2, 1, 2, ...` hasta llegar a 0 en la época 16. La solución de NOT exige `w1 < 0` y `b ≥ 0`, pero se inicializó con `w1 = +0.5` y `b = -0.7` (ambos del signo equivocado), por lo que el algoritmo necesita muchas iteraciones para "darles la vuelta". Por eso en el código se le dio un límite de 20 épocas a NOT y solo 10 a OR.
- **XOR: nunca converge** (ver punto 4).

### ¿Fue necesario ajustar la tasa de aprendizaje? ¿Por qué?

**No.** Se mantuvo en `0.1` para todas las compuertas y todas las linealmente separables convergieron:

- Por el **teorema de convergencia del perceptrón**, si los datos son linealmente separables el algoritmo converge en un número finito de pasos con **cualquier** tasa de aprendizaje positiva. La tasa afecta el tamaño de cada salto de ajuste, no la capacidad de converger.
- Con `0.1` cada corrección mueve un peso solo `±0.1`, produciendo ajustes pequeños y estables. Una tasa mayor (p. ej. `0.5`) habría reducido las épocas del NOT, pero no era necesaria para que aprendiera.
- Lo que sí se ajustó fue el **número máximo de épocas** (20 para NOT vs 10 para OR), y fue suficiente.

### ¿Qué diferencias encontró entre la compuerta AND y la OR?

- **Geometría de la frontera de decisión:** ambas son linealmente separables (una línea separa los 1s de los 0s), pero al lado contrario: en AND solo `(1,1)` activa (la región de 1s es una esquina del plano); en OR activa todo excepto `(0,0)` (la región de 0s es una esquina).
- **Punto de partida:** con `(0.5, 0.5, -0.7)` la neurona "nace" sabiendo AND, por eso converge en 1 época. Esa misma configuración falla en OR para `(0,1)` y `(1,0)` porque `z = -0.2 < 0` queda justo debajo del umbral; OR necesita una frontera más "permisiva", y de hecho su solución final tiene un bias mayor (`-0.5` vs `-0.7`).
- **Velocidad de aprendizaje:** AND 1 época, OR 2. En la práctica ambas son problemas triviales para el perceptrón por ser linealmente separables; la diferencia dramática surge al compararlas con XOR.

### ¿Por qué la compuerta XOR no puede ser aprendida por una sola neurona?

Porque **XOR no es linealmente separable**. Una neurona con función escalón solo puede trazar una frontera de decisión **recta** (`escalon(w1·x1 + w2·x2 + b)`), pero en XOR las salidas 1 — `(0,1)` y `(1,0)` — están en **diagonales opuestas**, y ninguna línea puede dejarlas de un lado mientras los 0s — `(0,0)` y `(1,1)` — quedan del otro.

Demostración por contradicción con las restricciones de XOR:

1. `(0,0) → 0` exige `b < 0`
2. `(0,1) → 1` exige `w2 + b ≥ 0`, es decir `w2 ≥ -b > 0`
3. `(1,0) → 1` exige `w1 ≥ -b > 0`
4. Entonces `w1 + w2 + b ≥ -b > 0` implica `(1,1) → 1`, pero XOR exige `(1,1) → 0`. **Contradicción: no existe solución.**

Empíricamente, al entrenar con la misma regla durante 1000 épocas el error nunca llega a 0: los pesos quedan oscilando sin encontrar una frontera posible. Este es el problema que **Minsky y Papert demostraron formalmente en 1969** en su libro *Perceptrons*, lo que frenó la investigación en redes neuronales y desató el **primer invierno de la IA**. La solución requiere una **red multicapa con capa oculta** (p. ej. `XOR = OR(AND(x1,x2), AND(NOT x1, NOT x2))` con neuronas ocultas) entrenada con descenso de gradiente y **backpropagation**: precisamente la motivación histórica para pasar del perceptrón simple a las redes neuronales profundas.