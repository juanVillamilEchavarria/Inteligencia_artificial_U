# Leo Counter AI - Inteligencia Artificial para Análisis Financiero Inteligente

## Problemática

Los usuarios de **Leo Counter** (gestor de finanzas open-source para hogares y PyMEs) registran diariamente decenas de transacciones financieras que se categorizan manualmente o mediante reglas básicas. Sin embargo, existen tres problemas que limitan la retroalimentacion de sus usuarios finales:

1. **Categorización superficial**: El sistema maneja categorías principales (Alimentación, Transporte, Entretenimiento, etc.), pero dentro de cada categoría pueden existir sub-categorías diminutas que el usuario no identifica. Por ejemplo, dentro de "Alimentación" puede haber "supermercado", "restaurantes", "cafeterías", "comida rápida", pero el usuario solo ve el total general sin comprender patrones específicos de consumo.

2. **Detección reactiva de anomalías**: Actualmente, las fugas de dinero o consumos inusuales solo se detectan cuando el usuario revisa  los reportes. No existe un sistema proactivo que alerte sobre transacciones atípicas en tiempo real (como una compra de $15,000 cuando el promedio mensual es $2,000).

3. **Reportes genéricos**: Los dashboards y analíticas actuales muestran KPIs y diferentes estadisticas (ingresos vs egresos, evolución mensual, etc.), pero no proporcionan insights accionables ni desgloses detallados adaptados al comportamiento específico de cada usuario.

Al no tener un soporte inteligente, las analiticas y reportes pueden no ser tan detallados, puntuales e interactivos, dificultando la comprension profunda del usuario final con respecto a sus estadisticas  

---

## Estructura del Proyecto

```
project/
├── data/
│   └── proyecto_limpio.csv          # Dataset limpio exportado por el pipeline
└── src/
    ├── main.py                          # Entry point: estadísticas financieras básicas
    ├── eda_proyectos.py                 # Entry point: EDA con NumPy + gráficos Matplotlib
    ├── data_preparation.py              # Entry point: pipeline completo de preparación
    ├── perceptron_proyecto.py           # Entry point: perceptrón desde cero (Avance 2)
    │
    ├── api/                             # Acceso a datos
    │   └── MovementsGateWay.py          # Lee data.json (futuro: API real)
    │
    ├── entities/                        # Entidades de dominio
    │   └── Movement.py                  # Movimiento financiero
    │
    ├── app_collections/                 # Colecciones de dominio
    │   └── MovementsCollection.py       # Colección tipada con filtrado por Enum
    │
    ├── enums/                           # Value Objects
    │   └── MovementFilteringKeys.py     # Claves de filtrado
    │
    ├── dto/                             # DTOs compartidos
    │   ├── MovementNumPyDTO.py          # Stats NumPy
    │   └── PerceptronTrainingDTO.py     # Pesos, sesgo e historial de entrenamiento
    │
    ├── services/                        # Lógica de negocio pura (cálculos)
    │   ├── StatisticsService.py         # Estadísticas con Python puro
    │   ├── NumpyStatisticsService.py    # Estadísticas con NumPy (EDA)
    │   └── PerceptronService.py         # Sigmoide, pérdida, gradientes y fit (NumPy puro)
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
    │   └── train/                       # Pipeline de entrenamiento del perceptrón
    │       ├── PerceptronTrainingPipeline.py    # Orquestador
    │       ├── PerceptronTrainingRunner.py      # Composition root
    │       ├── PerceptronTrainingContext.py     # Estado inmutable
    │       ├── steps/
    │       │   ├── TrainingStep.py              # ABC
    │       │   ├── LoadPreparedDataStep.py      # Carga el CSV preparado
    │       │   ├── SelectFeaturesStep.py        # Target + dos entradas
    │       │   ├── StandardizeStep.py           # Estandarización
    │       │   ├── TrainPerceptronStep.py       # Descenso del gradiente
    │       │   └── EvaluateStep.py              # Pesos, pérdida y exactitud
    │       └── dtos/
    │           ├── PerceptronReport.py
    │           └── PredictionResult.py
    │
    ├── outputs/                         # Generadores de artefactos (sin lógica de negocio)
    │   ├── visualization/
    │   │   ├── MatplotlibChartRenderer.py       # Gráficos Matplotlib → src/charts/
    │   │   ├── SeabornChartRenderer.py          # Gráficos Seaborn → src/charts_seaborn/
    │   │   └── PerceptronChartRenderer.py       # Curva y frontera → src/charts_perceptron/
    │   └── reporting/
    │       ├── FinancialReportGenerator.py
    │       └── EdaReportGenerator.py
    │
    ├── controllers/                     # Fachadas hacia los entry points
    │   ├── MovementController.py
    │   ├── MovementGraphicsController.py
    │   └── PerceptronController.py
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

---

## Datos

### Información requerida

El sistema de IA necesita consumir los siguientes datos del sistema Leo Counter:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `id` | Identificador único de la transacción | `1042` |
| `name` | Nombre del establecimiento o entidad | `Walmart`, `Uber`, `Netflix` |
| `description` | Descripción en texto crudo del movimiento | `Compra semanal supermercado frutas verduras` |
| `amount` | Monto numérico de la transacción | `1850.50` |
| `date` | Fecha del movimiento | `2025-01-03` |
| `category_id` | Categoría principal asignada (del sistema actual) | `1` (Alimentación) |
| `tipo_movimiento_id` | Tipo de movimiento | `2` (Gastos) |
| `cuenta_id` | Cuenta asociada al movimiento | `1` (Nequi personal) |

### Origen de los datos

Los datos se obtendrán del **sistema Leo Counter existente** mediante dos posibles enfoques:

1. **Consumo de API existente**: Utilizar los endpoints REST actuales de Leo Counter que ya exponen los movimientos financieros (`/api/movimientos`) para obtener datos reales de producción en formato JSON.

2. **Endpoint dedicado para IA**: Crear un nuevo endpoint especializado (`/api/ai/analytics/transactions`) que proporcione un dataset enriquecido específicamente diseñado para el motor de IA, incluyendo:
   - Historial completo de transacciones del usuario
   - Categorías
   - Metadatos adicionales (cuenta de origen, tipo de movimiento, recurrencia)

**Fuente de datos**: Sistema Leo Counter autohospedado con datos reales de usuarios finales (hogares y PyMEs), garantizando diversidad de patrones de consumo, montos variados y descripciones en lenguaje natural.

---

## Objetivo

El sistema de IA logrará los siguientes objetivos al integrarse como feature de **Leo Counter**:

### 1. Clasificación Semántica Automática
Implementar un modelo **Naive Bayes Multinomial** que analice las descripciones en texto crudo de las transacciones para:
- Detectar automáticamente sub-categorías específicas dentro de las categorías principales
- Aprender patrones de lenguaje propios de cada usuario (ej: "tacos el pastor" → comida rápida, "despensa mensual" → supermercado)
- Sugerir categorizaciones más precisas y granulares

### 2. Detección Proactiva de Anomalías
Aplicar un modelo estadístico de **Puntaje Z** para:
- Identificar transacciones atípicas en tiempo real (montos que se desvían significativamente del comportamiento histórico)
- Alertar al usuario sobre posibles fugas de dinero o consumos inusuales
- Generar notificaciones automáticas vía el sistema de notificaciones existente de Leo Counter

### 3. Reportes y Analíticas Enriquecidas
Proporcionar insights avanzados y accionables:
- **Desglose detallado por sub-categorías**: Mostrar no solo "Alimentación: $5,000" sino "Supermercado: $3,200 | Restaurantes: $1,200 | Cafeterías: $600"
- **Detección de patrones de comportamiento**: "Gastas 40% más en cafeterías los lunes" o "Tus compras en Amazon aumentaron 200% este mes"
- **Recomendaciones personalizadas**: Sugerencias de ahorro basadas en los patrones detectados
- **Alertas inteligentes**: "Tu gasto en entretenimiento supera el presupuesto mensual en un 35%"

### 4. Mejora Continua del Sistema
- Retroalimentar el sistema de categorización actual de Leo Counter con las sub-categorías detectadas por la IA
- Crear un ciclo de aprendizaje donde el modelo mejore con cada transacción procesada
- Integrarse seamlessly con la arquitectura DDD y CQRS existente de Leo Counter mediante nuevos Domain Services

**Resultado final**: Transformar a Leo Counter de un gestor de transacciones a un **asistente financiero inteligente** que no solo registra datos, sino que los comprende, analiza y ayuda activamente al usuario a mejorar su salud financiera.

## Análisis Exploratorio de Datos (EDA)

### Variables Analizadas

Se analizaron las siguientes variables del dataset de 50 transacciones financieras:

- **`monto`** (numérica continua): Valor de cada transacción en pesos colombianos (COP).
- **`tipo_movimiento`** (categórica binaria): Clasifica cada transacción como "Ingreso" o "Gasto".
- **`categoria`** (categórica nominal): Categoría principal asignada a cada movimiento.

### Estadísticas Calculadas con NumPy

| Métrica | Ingresos | Gastos | Todos los montos |
|---------|----------|--------|-----------------|
| Cantidad | 14 | 36 | 50 |
| Suma total | $40,835,100.00 | $14,684,900.00 | $55,520,000.00 |
| Media | $2,916,792.86 | $407,913.89 | $1,110,400.00 |
| Mediana | $625,000.00 | $165,000.00 | $250,000.00 |
| Desv. Estándar | $6,261,617.28 | $701,730.50 | $3,549,888.83 |
| Mínimo | $120,000.00 | $5,000.00 | $5,000.00 |
| Máximo | $25,000,000.00 | $3,500,000.00 | $25,000,000.00 |

### Patrones y Relaciones Observadas

1. **Alta asimetría en ingresos**: La media ($2.9M) es mucho mayor que la mediana ($775K), lo que indica que pocos valores extremos (venta de vehículo por $25M) jalan el promedio hacia arriba. Esto confirma la presencia de **outliers** que el Puntaje Z deberá detectar.

2. **Gastos más homogéneos**: La desviación estándar de gastos ($701.7K) es proporcionalmente menor que la de ingresos ($6.26M), indicando un patrón de consumo más estable y predecible.

3. **Distribución sesgada a la derecha**: El histograma muestra que la mayoría de transacciones se concentran en montos bajos (< $500K), con una cola larga hacia valores altos.

4. **Categorías con alta variabilidad**: "Educación" y "Tecnología" presentan los montos más altos y dispersos, mientras que "Transporte" tiene los más bajos y consistentes.

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

**Hallazgo**: El dataset original tiene **50 transacciones y 8 columnas**, sin valores nulos y sin filas duplicadas exactas. Sin embargo, el archivo original contenía **16 IDs repetidos** que afectaban a 21 transacciones distintas; por eso los identificadores se regeneraron como **UUID v7 únicos** (50 IDs únicos para 50 filas), sin modificar los demás campos.

**Estrategia implementada en `CleanDataStep`**:
- **Normalización de texto**: `strip()` y colapso de espacios en `id`, `nombre`, `cuenta`, `categoria`, `tipo_movimiento` y `descripcion`. Esto corrigió el valor `'Banco Bogota '`.
- **Tipos**: `monto` se convierte a numérico y `fecha` a `datetime` con `errors='coerce'`.
- **Valores imposibles**: se descartan filas con fechas inválidas o montos no numéricos/no positivos, y se reporta cuántas se eliminaron (0 en este dataset).
- **Duplicados**: se aplica `drop_duplicates()` y se reporta el número eliminado (0 en este dataset).
- **Nulos**: imputación con **mediana** para variables numéricas y **moda** para categóricas (0 en este dataset).
- **Outliers**: **no se eliminan**. Se conservan 10 transacciones (20%) y se usa `monto_log` para reducir su impacto, porque corresponden a eventos reales como la venta de un vehículo ($25M) y una matrícula.

**Tabla antes / después**:

| Momento | Filas | Columnas | Nulos |
|---------|------:|---------:|------:|
| Dataset original | 50 | 8 | 0 |
| Después de limpieza | 50 | 8 | 0 |
| Después de preparación | 50 | 39 | 0 |

**Justificación**: La mediana se prefiere sobre la media para variables financieras debido a la alta asimetría (skewness = 6.3) y a los outliers extremos, que distorsionan la media.

### 2. Variables Categóricas Codificadas

**Método**: `pd.get_dummies()` (One-Hot Encoding) aplicado en `EncodingStep`.

| Variable Original | Cardinalidad | Columnas Dummy Generadas | Prefijo |
|-------------------|--------------|--------------------------|---------|
| `categoria` | 13 únicas | 13 | `categoria_` |
| `tipo_movimiento` | 2 (Ingreso/Gasto) | 2 | `tipo_movimiento_` |
| `cuenta` | 11 únicas | 11 | `cuenta_` |
| **Total** | — | **26 columnas dummy** | — |

**Dataset final**: 50 filas × 39 columnas (8 originales + 5 derivadas + 26 dummies).

**Ejemplos de columnas generadas**:
- `categoria_Alimentación`, `categoria_Transporte`, `categoria_Otros Ingresos`, ...
- `tipo_movimiento_Gasto`, `tipo_movimiento_Ingreso`
- `cuenta_Banco Bogota`, `cuenta_Nequi`, `cuenta_Bancolombia`, ...

### 3. Columnas Derivadas Creadas

| Columna | Tipo | Fórmula / Lógica | Propósito |
|---------|------|------------------|-----------|
| `monto_log` | Numérica continua | `np.log1p(monto)` | **Normalización para ML**: reduce asimetría extrema (skew 6.3 → ~1.2), estabiliza varianza y mejora la convergencia |
| `es_ingreso` | Binaria (0/1) | `(tipo_movimiento == 'Ingreso').astype(int)` | **Variable objetivo**: clasificación binaria Ingreso/Gasto |
| `mes` | Numérica discreta (1-12) | `fecha.dt.month` | **Estacionalidad**: patrones mensuales |
| `dia_semana` | Numérica discreta (0-6) | `fecha.dt.dayofweek` (Lun=0) | **Patrones semanales** |
| `es_fin_semana` | Binaria (0/1) | `(dia_semana >= 5).astype(int)` | **Feature conductual** |

**Impacto en modelos futuros**:
- `monto_log`: esencial para **Puntaje Z** (asume normalidad) y **Naive Bayes** (Gaussiano).
- `es_ingreso`: target natural para clasificación binaria y para el perceptrón del Avance 2.
- `es_fin_semana` + `mes`: features temporales para reportes enriquecidos.

### 4. Hallazgos de las Visualizaciones Seaborn

Se generaron **10 gráficos** en `src/charts_seaborn/`:

| Gráfico | Archivo | Hallazgo Principal |
|---------|---------|-------------------|
| **Histograma Monto** | `seaborn_histograma_monto.png` | Distribución **extremadamente sesgada a derecha** (cola larga). Mayoría de transacciones < $500K. Outliers visibles > $5M. |
| **Histograma Log(Monto)** | `seaborn_histograma_monto_log.png` | La transformación log **normaliza la distribución** (aprox. gaussiana), validando `monto_log` para modelos paramétricos. |
| **Boxplot por Categoría** | `seaborn_boxplot_categoria.png` | **Alta variabilidad inter-categoría**: "Otros Ingresos" e "Independiente" tienen medianas altas y outliers; "Transporte" y "Entretenimiento" son bajos y consistentes. |
| **Boxplot por Tipo** | `seaborn_boxplot_tipo.png` | **Ingresos**: mediana $625K, outliers hasta $25M. **Gastos**: mediana $165K, outliers hasta $3.5M. Confirma la necesidad de **umbrales Z-score separados**. |
| **Scatter Fecha vs Monto** | `seaborn_scatter_monto_fecha.png` | **Eventos puntuales**: junio 2024 muestra un clúster de gastos altos (matrícula $2.5M, laptop $3.5M). La venta de vehículo de agosto 2026 ($25M) es un outlier temporal claro. |
| **Regresión Log(Monto) vs Tiempo** | `seaborn_regplot_monto_log_fecha.png` | **Tendencia ligeramente positiva** en log-monto a lo largo del tiempo. |
| **Barplot Categoría × Tipo** | `seaborn_barplot_categoria_tipo.png` | **Asimetría categórica**: "Otros Ingresos" domina ingresos; "Otros Gastos", "Servicios Públicos" y "Vivienda" lideran gastos. "Independiente" aparece en ambos. |
| **Heatmap Correlación** | `seaborn_correlation_heatmap.png` | **Correlaciones clave**: `monto` ↔ `monto_log` (0.98), `es_ingreso` ↔ `monto` (0.31), `es_fin_semana` ↔ `monto` (~0.05). |
| **Scatter Entradas × Target** | `seaborn_scatter_features_target.png` | Relaciona directamente `monto_log` y `mes` con `es_ingreso`. Los ingresos tienden a concentrarse en montos más altos. Es el gráfico de soporte del perceptrón. |
| **Pairplot** | `seaborn_pairplot.png` | **Separación visual** Ingreso/Gasto en `monto_log`. `es_fin_semana` no discrimina montos. |

### 5. Hallazgos Relevantes para el Proyecto

1. **Outliers críticos detectados**: 10 transacciones (20%) son outliers por IQR. La venta de vehículo ($25M) y la matrícula ($2.5M) son **eventos atípicos reales**, no errores. El **Puntaje Z debe usar umbrales por tipo de movimiento**.

2. **Asimetría extrema corregida**: `monto_log` reduce skewness de **6.3 → 1.2**, haciendo los datos aptos para modelos que asumen normalidad.

3. **Desbalance de clases**: 72% Gastos / 28% Ingresos. El perceptrón obtiene 78% de exactitud frente a 72% de la clase mayoritaria; en el proyecto final se requerirá **class_weight='balanced'** o sampling.

4. **Cardinalidad alta en `cuenta` (11)**: 11 cuentas para 50 transacciones → riesgo de overfitting. Considerar **agrupar cuentas minoritarias** o usar **Target Encoding**.

5. **Patrón temporal**: junio 2024 concentra gastos extraordinarios (educación, tecnología). La feature `mes` captura esto para alertas estacionales.

6. **Fin de semana no es predictor**: `es_fin_semana` tiene correlación ~0.05 con monto.

### 6. Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `data/proyecto_limpio.csv` | Dataset completo listo para ML (50×39) |
| `src/eda_summary.md` | Resumen EDA + tabla antes/después |
| `src/charts_seaborn/*.png` | 10 gráficos Seaborn |
| `src/charts_perceptron/curva_aprendizaje.png` | Pérdida y exactitud por época |
| `src/charts_perceptron/frontera_decision.png` | Frontera de decisión del perceptrón |

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

## Avance 2: preparación, visualización y perceptrón desde cero

Esta sección resume el entregable del segundo corte: dataset limpio, análisis visual, perceptrón implementado con NumPy y plan hacia el proyecto final.

### 1. Ajustes y calidad de datos

- Se regeneraron los **IDs como UUID v7 únicos** (50 IDs para 50 transacciones), sin alterar montos, fechas, cuentas, categorías ni descripciones.
- Se normalizaron espacios en columnas de texto; por ejemplo, `'Banco Bogota '` pasó a `'Banco Bogota'`.
- Se verificó que no hay nulos, filas duplicadas exactas, montos no positivos ni fechas inválidas.
- Se conservaron los **10 outliers** (20%) porque son eventos financieros reales; `monto_log` reduce su influencia.
- El dataset limpio se exporta a **`project/data/proyecto_limpio.csv`** (50 filas × 39 columnas).

### 2. Perceptrón implementado

- **Variable objetivo**: `es_ingreso` (1 = Ingreso, 0 = Gasto).
- **Entradas**: `monto_log` y `mes`, ambas estandarizadas con media y desviación del conjunto de entrenamiento.
- **Modelo**: sigmoide + pérdida logarítmica + descenso del gradiente, implementado únicamente con **NumPy** (sin Scikit-Learn).
- **Entrenamiento**: 50 transacciones, `learning_rate = 0.1`, 500 épocas.
- **Pipeline**: `pipelines/train/` con steps atómicos (`LoadPreparedDataStep`, `SelectFeaturesStep`, `StandardizeStep`, `TrainPerceptronStep`, `EvaluateStep`).
- **Gráficos**: `src/charts_perceptron/curva_aprendizaje.png` y `src/charts_perceptron/frontera_decision.png`.

### 3. Resultados del perceptrón

| Métrica | Valor |
|---|---:|
| Filas de entrenamiento | 50 |
| Clase 0 (Gasto) | 36 |
| Clase 1 (Ingreso) | 14 |
| Pesos finales | `w1 = 1.3141`, `w2 = 0.1906` |
| Sesgo | `b = -1.2329` |
| Pérdida inicial | 0.6931 |
| Pérdida final | 0.4678 |
| Exactitud inicial | 28.00% |
| Exactitud final | 78.00% |
| Exactitud de la clase mayoritaria | 72.00% |

**Interpretación**:
- `w1 > 0`: a mayor `monto_log`, mayor probabilidad de que el movimiento sea un ingreso.
- `w2 > 0`: meses más avanzados del año aumentan ligeramente la probabilidad de ingreso.
- `b < 0`: con montos bajos y meses tempranos, el modelo tiende a predecir gasto.
- El modelo supera la línea base (78% vs 72%), pero los datos no son perfectamente separables: hay gastos altos que se confunden con ingresos.
- Limitaciones: solo dos variables, dataset pequeño, entrenamiento y evaluación sobre las mismas 50 filas y desbalance 72/28.

### 4. Predicción de casos nuevos

| Monto | Mes | Probabilidad de ingreso | Decisión |
|---:|---:|---:|---|
| $8.000 | 6 | 2.18% | Gasto |
| $3.500.000 | 4 | 60.65% | Ingreso |
| $250.000 | 5 | 20.24% | Gasto |

### 5. Cómo ejecutar con Docker

El `Dockerfile` y `docker-compose.yml` no se modificaron. Desde la carpeta `project/`:

```bash
# Construir la imagen (solo la primera vez o si cambian dependencias)
docker compose build

# 1) Generar el dataset limpio, el resumen EDA y los gráficos Seaborn
docker compose run --rm app python src/data_preparation.py

# 2) Entrenar el perceptrón y generar sus gráficos
docker compose run --rm app python src/perceptron_proyecto.py
```

También se puede ejecutar sin Docker desde `project/`:

```bash
python3 src/data_preparation.py
python3 src/perceptron_proyecto.py
```

El perceptrón requiere que exista `data/proyecto_limpio.csv`; si no existe, el script indica que se debe ejecutar primero `data_preparation.py`.

### 6. Plan hacia el proyecto final

- **Tipo de problema**: clasificación (primero binaria `es_ingreso`; luego clasificación semántica de subcategorías y detección de anomalías).
- **Modelos a comparar en la Clase 12**: regresión logística, árbol de decisión y bosque aleatorio. Complementariamente, Naive Bayes Multinomial para texto y Puntaje Z para anomalías.
- **Métrica principal**: F1-score macro y recall de la clase minoritaria (Ingreso), porque el dataset está desbalanceado y no conviene optimizar solo exactitud.
- **Demostración final**: cargar transacciones nuevas desde JSON/CSV, mostrar la probabilidad y la clase predicha, y luego extender la demostración a subcategorías y alertas de anomalías.
- **Cronograma**: entrega del Avance 2 (25 de octubre), comparación de modelos en la Clase 12 (9 de noviembre), integración y pruebas (16 de noviembre), sustentación final (23 o 30 de noviembre).

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