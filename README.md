# Leo Counter AI - Inteligencia Artificial para Análisis Financiero Inteligente

## Problemática

Los usuarios de **Leo Counter** (gestor de finanzas open-source para hogares y PyMEs) registran diariamente decenas de transacciones financieras que se categorizan manualmente o mediante reglas básicas. Sin embargo, existen tres problemas que limitan la retroalimentacion de sus usuarios finales:

1. **Categorización superficial**: El sistema maneja categorías principales (Alimentación, Transporte, Entretenimiento, etc.), pero dentro de cada categoría pueden existir sub-categorías diminutas que el usuario no identifica. Por ejemplo, dentro de "Alimentación" puede haber "supermercado", "restaurantes", "cafeterías", "comida rápida", pero el usuario solo ve el total general sin comprender patrones específicos de consumo.

2. **Detección reactiva de anomalías**: Actualmente, las fugas de dinero o consumos inusuales solo se detectan cuando el usuario revisa  los reportes. No existe un sistema proactivo que alerte sobre transacciones atípicas en tiempo real (como una compra de $15,000 cuando el promedio mensual es $2,000).

3. **Reportes genéricos**: Los dashboards y analíticas actuales muestran KPIs y diferentes estadisticas (ingresos vs egresos, evolución mensual, etc.), pero no proporcionan insights accionables ni desgloses detallados adaptados al comportamiento específico de cada usuario.

Al no tener un soporte inteligente, las analiticas y reportes pueden no ser tan detallados, puntuales e interactivos, dificultando la comprension profunda del usuario final con respecto a sus estadisticas  

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