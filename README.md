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
project/src/
├── main.py                          # Entry point: estadísticas financieras básicas
├── eda_proyectos.py                 # Entry point: EDA con NumPy + gráficos Matplotlib
├── data_preparation.py              # Entry point: pipeline completo de preparación de datos
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
│   └── MovementFilteringKeys.py     # Claves de filtrado (cuenta, categoria, tipo, fecha)
│
├── dto/                             # Data Transfer Objects de estadísticas
│   └── MovementNumPyDTO.py          # Stats NumPy (median, mean, std, min, max...)
│
├── services/                        # Lógica de negocio pura (cálculos)
│   ├── StatisticsService.py         # Estadísticas con Python puro
│   └── NumpyStatisticsService.py    # Estadísticas con NumPy (EDA)
│
├── pipelines/                       # Pipelines de procesamiento de datos
│   └── transform/
│       ├── DataPreparationPipeline.py   # Orquestador: ejecuta steps en orden
│       ├── DataPreparationRunner.py     # Composition root: ensambla el pipeline
│       ├── DataPreparationContext.py    # Estado compartido inmutable entre steps
│       ├── steps/                       # Cada paso del pipeline (SRP)
│       │   ├── DataPreparationStep.py       # ABC: contrato de los steps
│       │   ├── LoadDataStep.py              # Carga datos vía Gateway
│       │   ├── EdaStep.py                   # Genera EdaReport (DTO tipado)
│       │   ├── CleanDataStep.py             # Limpieza + CleaningReport (DTO)
│       │   ├── FeatureEngineeringStep.py    # Columnas derivadas (monto_log, es_fin_semana...)
│       │   ├── EncodingStep.py              # pd.get_dummies() en categóricas
│       │   └── PersistStep.py               # Guarda CSV preparado
│       └── dtos/                        # DTOs tipados del pipeline
│           ├── EdaReport.py               # Hallazgos EDA (shape, nulos, outliers...)
│           └── CleaningReport.py          # Registro de imputaciones realizadas
│
├── outputs/                         # Generadores de artefactos (NO lógica de negocio)
│   ├── visualization/
│   │   ├── MatplotlibChartRenderer.py   # Gráficos Matplotlib → charts/
│   │   └── SeabornChartRenderer.py      # Gráficos Seaborn → charts_seaborn/
│   └── reporting/
│       ├── FinancialReportGenerator.py  # Informe financiero Markdown
│       └── EdaReportGenerator.py        # Resumen EDA Markdown desde DTOs
│
├── controllers/                     # Fachadas (adaptadores hacia entry points)
│   ├── MovementController.py        # Expone estadísticas básicas
│   └── MovementGraphicsController.py # Expone generación de gráficos
│
└── helpers/                         # Utilidades compartidas
    └── output_helpers.py            # print_separator() para CLI
```

**Principios de la arquitectura:**
- **services/**: solo lógica de negocio (cálculos estadísticos). Sin prints ni generación de artefactos.
- **outputs/**: generadores de artefactos (imágenes, reportes). Reciben datos ya procesados.
- **pipelines/**: flujos de transformación de datos descompuestos en steps atómicos y extensibles, con estado compartido **inmutable** (`DataPreparationContext`, `dataclasses.replace`) y resultados en **DTOs tipados** (nunca dicts inseguros).
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

Se analizaron las siguientes variables del dataset de 49 transacciones financieras:

- **`monto`** (numérica continua): Valor de cada transacción en pesos colombianos (COP).
- **`tipo_movimiento`** (categórica binaria): Clasifica cada transacción como "Ingreso" o "Gasto".
- **`categoria`** (categórica nominal): Categoría principal asignada a cada movimiento.

### Estadísticas Calculadas con NumPy

| Métrica | Ingresos | Gastos | Todos los montos |
|---------|----------|--------|-----------------|
| Cantidad | 14 | 35 | 49 |
| Suma total | $40,835,100.00 | $14,534,900.00 | $55,369,000.00 |
| Media | $2,916,792.86 | $415,282.86 | $1,129,979.59 |
| Mediana | $775,000.00 | $220,000.00 | $250,000.00 |
| Desv. Estándar | $6,287,456.32 | $640,891.45 | $4,267,891.23 |
| Mínimo | $120,000.00 | $5,000.00 | $5,000.00 |
| Máximo | $25,000,000.00 | $3,500,000.00 | $25,000,000.00 |

### Patrones y Relaciones Observadas

1. **Alta asimetría en ingresos**: La media ($2.9M) es mucho mayor que la mediana ($775K), lo que indica que pocos valores extremos (venta de vehículo por $25M) jalan el promedio hacia arriba. Esto confirma la presencia de **outliers** que el Puntaje Z deberá detectar.

2. **Gastos más homogéneos**: La desviación estándar de gastos ($640K) es proporcionalmente menor que la de ingresos, indicando un patrón de consumo más estable y predecible.

3. **Distribución sesgada a la derecha**: El histograma muestra que la mayoría de transacciones se concentran en montos bajos (< $500K), con una cola larga hacia valores altos.

4. **Categorías con alta variabilidad**: "Educación" y "Tecnología" presentan los montos más altos y dispersos, mientras que "Transporte" tiene los más bajos y consistentes.

### Impacto en el Modelo de IA

1. **Puntaje Z**: La alta desviación estándar en ingresos confirma que el umbral de detección de anomalías debe ser calculado por separado para ingresos y gastos. Un umbral global generaría falsos positivos.

2. **Naive Bayes**: La variedad de descripciones asociadas a montos similares sugiere que el modelo de clasificación semántica encontrará patrones útiles en el texto libre para diferenciar sub-categorías.

3. **Preprocesamiento**: Se recomienda aplicar normalización logarítmica a los montos antes de alimentar modelos de ML, dada la asimetría de la distribución.

### Gráficos Generados

| Gráfico | Archivo | Descripción |
|---------|---------|-------------|
| Histograma de montos | `charts/histograma_montos.png` | Distribución de todos los montos con líneas de media y mediana |
| Dispersión monto vs tipo | `charts/dispersion_monto_tipo.png` | Relación entre monto y tipo de movimiento |
| Boxplot por categoría | `charts/boxplot_gastos_categoria.png` | Distribución de gastos por categoría |

---

## Preparación de Datos

Esta sección documenta el pipeline completo de preparación de datos implementado siguiendo la arquitectura por servicios del proyecto, utilizando **Pandas** para manipulación y **Seaborn** para visualización.

### Ejecución del Pipeline

```bash
cd project
python src/data_preparation.py
```

### 1. Valores Nulos Encontrados y Manejo

**Hallazgo**: El dataset original (50 transacciones, 8 columnas) **no presenta valores nulos** en ningún campo (`total_nulls = 0`).

**Estrategia implementada en `MovementDataPreparationService.clean_data()`**:
- Aunque no hay nulos en el dataset actual, el servicio incluye lógica robusta de imputación:
  - **Variables numéricas** (`monto`, etc.): Imputación con **mediana** (robusta a outliers)
  - **Variables categóricas** (`categoria`, `cuenta`, etc.): Imputación con **moda** (valor más frecuente)
- Conversión de `fecha` a `datetime` con `errors='coerce'` para manejar formatos inválidos

**Justificación**: La mediana se prefiere sobre la media para variables financieras debido a la alta asimetría (skewness = 6.3) y presencia de outliers extremos (venta de vehículo $25M), que distorsionan la media.

### 2. Variables Categóricas Codificadas

**Método**: `pd.get_dummies()` (One-Hot Encoding) aplicado en `MovementDataPreparationService.encode_categorical_variables()`

| Variable Original | Cardinalidad | Columnas Dummy Generadas | Prefijo |
|-------------------|--------------|--------------------------|---------|
| `categoria` | 13 únicas | 13 | `categoria_` |
| `tipo_movimiento` | 2 (Ingreso/Gasto) | 2 | `tipo_movimiento_` |
| `cuenta` | 11 únicas | 11 | `cuenta_` |
| **Total** | — | **26 columnas dummy** | — |

**Dataset final**: 50 filas × 39 columnas (8 originales + 5 derivadas + 26 dummies)

**Ejemplos de columnas generadas**:
- `categoria_Alimentación`, `categoria_Transporte`, `categoria_Otros Ingresos`, ...
- `tipo_movimiento_Gasto`, `tipo_movimiento_Ingreso`
- `cuenta_Banco Bogota `, `cuenta_Nequi`, `cuenta_Bancolombia`, ...

### 3. Columnas Derivadas Creadas

| Columna | Tipo | Fórmula / Lógica | Propósito |
|---------|------|------------------|-----------|
| `monto_log` | Numérica continua | `np.log1p(monto)` | **Normalización para ML**: Reduce asimetría extrema (skew 6.3 → ~1.2), estabiliza varianza, mejora convergencia en modelos (Z-score, Naive Bayes, regresión) |
| `es_ingreso` | Binaria (0/1) | `(tipo_movimiento == 'Ingreso').astype(int)` | **Target binario / Feature**: Permite clasificación supervisada y separación rápida Ingreso/Gasto en modelos |
| `mes` | Numérica discreta (1-12) | `fecha.dt.month` | **Estacionalidad**: Detectar patrones mensuales (ej. gastos navideños, matrículas) |
| `dia_semana` | Numérica discreta (0-6) | `fecha.dt.dayofweek` (Lun=0) | **Patrones semanales**: Diferenciar días laborables vs fines de semana |
| `es_fin_semana` | Binaria (0/1) | `(dia_semana >= 5).astype(int)` | **Feature conductual**: Identificar comportamiento de gasto distinto en fines de semana |

**Impacto en modelos futuros**:
- `monto_log`: Esencial para **Puntaje Z** (asume normalidad) y **Naive Bayes** (Gaussiano)
- `es_ingreso`: Target natural para clasificación binaria
- `es_fin_semana` + `mes`: Features temporales para detectar estacionalidad en **reportes enriquecidos**

### 4. Hallazgos de las Visualizaciones Seaborn

Se generaron **9 gráficos** en `charts_seaborn/`:

| Gráfico | Archivo | Hallazgo Principal |
|---------|---------|-------------------|
| **Histograma Monto** | `seaborn_histograma_monto.png` | Distribución **extremadamente sesgada a derecha** (cola larga). Mayoría transacciones < $500K. Outliers visibles > $5M. |
| **Histograma Log(Monto)** | `seaborn_histograma_monto_log.png` | Transformación log **normaliza la distribución** (aprox. gaussiana), validando uso de `monto_log` para modelos paramétricos. |
| **Boxplot por Categoría** | `seaborn_boxplot_categoria.png` | **Alta variabilidad inter-categoría**: "Otros Ingresos" y "Independiente" tienen medianas altas y outliers; "Transporte" y "Entretenimiento" son bajos y consistentes. |
| **Boxplot por Tipo** | `seaborn_boxplot_tipo.png` | **Ingresos**: Mediana $625K, outliers hasta $25M. **Gastos**: Mediana $165K, outliers hasta $3.5M. Confirma necesidad de **umbrales Z-score separados**. |
| **Scatter Fecha vs Monto** | `seaborn_scatter_monto_fecha.png` | **Eventos puntuales**: Junio 2024 muestra cluster de gastos altos (matrícula $2.5M, laptop $3.5M). Venta vehículo agosto 2026 ($25M) es outlier temporal claro. |
| **Regresión Log(Monto) vs Tiempo** | `seaborn_regplot_monto_log_fecha.png` | **Tendencia ligeramente positiva** en log-monto a lo largo del tiempo, sugiriendo crecimiento gradual de montos promedio. |
| **Barplot Categoría × Tipo** | `seaborn_barplot_categoria_tipo.png` | **Asimetría categórica**: "Otros Ingresos" domina ingresos ($29M+); "Otros Gastos", "Servicios Públicos", "Vivienda" lideran gastos. "Independiente" aparece en ambos. |
| **Heatmap Correlación** | `seaborn_correlation_heatmap.png` | **Correlaciones clave**: `monto` ↔ `monto_log` (0.98), `es_ingreso` ↔ `monto` (0.31), `es_fin_semana` ↔ `monto` (~0.05 sin relación). Features temporales débilmente correlacionadas con monto. |
| **Pairplot** | `seaborn_pairplot.png` | **Separación visual** Ingreso/Gasto clara en `monto` y `monto_log`. `es_fin_semana` no discrimina montos. |

### 5. Hallazgos Relevantes para el Proyecto

1. **Outliers críticos detectados**: 10 transacciones (20%) son outliers por IQR. La venta de vehículo ($25M) y matrícula ($2.5M) son **eventos atípicos reales**, no errores. El **Puntaje Z debe usar umbrales por tipo de movimiento**.

2. **Asimetría extrema corregida**: `monto_log` reduce skewness de **6.3 → 1.2**, haciendo los datos aptos para modelos que asumen normalidad.

3. **Desbalance de clases**: 72% Gastos / 28% Ingresos. Modelo Naive Bayes requerirá **class_weight='balanced'** o sampling.

4. **Cardinalidad alta en `cuenta` (11)**: 11 cuentas para 50 transacciones → riesgo de overfitting. Considerar **agrupar cuentas minoritarias** o usar **Target Encoding** en futuras iteraciones.

5. **Patrón temporal**: Junio 2024 concentra gastos extraordinarios (educación, tecnología). Feature `mes` captura esto para alertas estacionales.

6. **Fin de semana no es predictor**: `es_fin_semana` correlación ~0.05 con monto → no útil como feature principal, pero puede servir en interacciones.

### 6. Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `data_prepared.csv` | Dataset completo listo para ML (50×39) |
| `charts_seaborn/seaborn_histograma_monto.png` | Histograma monto original |
| `charts_seaborn/seaborn_histograma_monto_log.png` | Histograma monto normalizado |
| `charts_seaborn/seaborn_boxplot_categoria.png` | Boxplot por categoría |
| `charts_seaborn/seaborn_boxplot_tipo.png` | Boxplot Ingreso vs Gasto |
| `charts_seaborn/seaborn_scatter_monto_fecha.png` | Dispersión temporal |
| `charts_seaborn/seaborn_regplot_monto_log_fecha.png` | Regresión temporal log-monto |
| `charts_seaborn/seaborn_barplot_categoria_tipo.png` | Barras apiladas categoría×tipo |
| `charts_seaborn/seaborn_correlation_heatmap.png` | Matriz correlación numérica |
| `charts_seaborn/seaborn_pairplot.png` | Pairplot variables clave |

### 7. Arquitectura de Servicios Utilizada

El pipeline respeta la arquitectura por capas del proyecto:

```
src/
├── api/MovementsGateWay.py                    # Data Access (JSON → Collection)
├── app_collections/MovementsCollection.py     # Domain Collection + to_dataframe()
├── entities/Movement.py                       # Domain Entity
├── services/
│   ├── MovementDataPreparationService.py      # 🆕 EDA, Limpieza, Encoding, Features (Pandas)
│   └── MovementSeabornGraphicsService.py      # 🆕 Visualizaciones Seaborn (SRP)
├── controllers/
│   └── MovementDataPreparationController.py   # 🆕 Facade para preparation service
├── data_preparation.py                        # 🆕 Entry Point CLI
└── helpers/output_helpers.py                  # Shared: print_separator()
```

**Principios aplicados**:
- **SRP**: Servicios separados para preparación (`MovementDataPreparationService`) y visualización Seaborn (`MovementSeabornGraphicsService`)
- **Dependency Injection**: Controller recibe Service por constructor
- **Single Source of Truth**: `MovementsGateWay` única fuente de datos
- **Extensibilidad**: Nuevos servicios no modifican existentes (`MovementGraphicsService` matplotlib intacto)