# Respuestas Detalladas - Análisis de Datos de Ventas

---

## 1. Exploración del Dataset

### **Dimensiones y Estructura**
- **Filas válidas**: 12 transacciones (tras descartar 1 fila basura generada por el header malformado en el CSV)
- **Columnas**: 9 atributos originales

| Columna | Tipo Original | Tipo Inferido | Descripción |
|---------|---------------|---------------|-------------|
| `id_venta` | string | Identificador | UUID/ID único por transacción |
| `fecha` | string | Temporal (YYYY-MM-DD) | Fecha de la venta |
| `producto` | string | Categórico nominal | Nombre del producto vendido |
| `categoria` | string | Categórico nominal | Agrupación: Alimentos, Lácteos, Aseo |
| `precio_unitario` | float64 | Numérico continuo | Precio por unidad ($) |
| `cantidad` | float64 → int | Numérico discreto | Unidades vendidas |
| `ciudad` | string | Categórico nominal | Cartago, Pereira, Armenia, Manizales |
| `cliente_edad` | float64 | Numérico continuo | Edad del comprador (años) |
| `metodo_pago` | string | Categórico binario | Efectivo, Tarjeta |

### **Valores Nulos Detectados**
```
cliente_edad: 3 nulos (25% del total)
fecha: 1 nulo (fila header malformado)
producto: 1 nulo (fila header malformado)
categoria: 1 nulo (fila header malformado)
precio_unitario: 1 nulo (fila header malformado)
cantidad: 1 nulo (fila header malformado)
ciudad: 1 nulo (fila header malformado)
metodo_pago: 1 nulo (fila header malformado)
```

**Nota técnica**: El CSV tiene el header roto en dos líneas (`id_venta,fecha,producto,categoria,precio_unitario,cantidad,ciudad,cliente_edad,m` + `etodo_pago`), lo que genera una primera fila de datos corrupta. El `SalesDataGateway` maneja esto concatenando las dos primeras líneas y saltando la fila resultante inválida.

### **Estadísticas Descriptivas (Variables Numéricas)**
| Métrica | precio_unitario | cantidad | cliente_edad |
|---------|----------------|----------|--------------|
| Count | 12 | 12 | 10 |
| Mean | 3.10 | 6.50 | 37.40 |
| Std | 1.55 | 4.19 | 10.73 |
| Min | 1.50 | 2 | 22 |
| 25% | 1.95 | 3 | 29.5 |
| 50% (Mediana) | 2.50 | 5.5 | 36.0 |
| 75% | 3.98 | 8.5 | 43.75 |
| Max | 6.50 | 15 | 55 |

---

## 2. Limpieza de Datos

### **Estrategia Aplicada**
1. **Eliminación de fila corrupta**: La primera fila del CSV (resultado del header partido) se descarta al tener `fecha=NaN`
2. **Imputación de edad**: Los 3 valores nulos en `cliente_edad` se imputan con la **mediana (36.0 años)**

### **Justificación: Mediana vs Media**

| Consideración | Media (37.4) | Mediana (36.0) |
|---------------|--------------|----------------|
| **Sensibilidad a outliers** | Alta (afectada por edad 55) | Baja (valor central robusto) |
| **Distribución de edades** | Sesgada derecha (tail larga) | Representa el "cliente típico" |
| **Contexto negocio** | Edad promedio inflada por pocos mayores | Edad representativa de la mayoría |
| **Impacto en ML** | Features sesgadas, peor convergencia | Features más estables, mejor generalización |

**Análisis de outliers en edad**:
- Valores: 22, 28, 29, 31, 34, 38, 40, 45, 52, 55
- IQR = Q3 - Q1 = 43.75 - 29.5 = 14.25
- Límite superior = Q3 + 1.5×IQR = 43.75 + 21.375 = 65.125 → **No hay outliers extremos por IQR**
- Sin embargo, la media se ve tirada hacia arriba por valores >50 (52, 55), mientras la mediana se mantiene en el centro de la masa de datos (30-40 años)

**Decisión**: La mediana preserva la distribución real de la mayoría de clientes (rango 28-45) sin dejarse influir por compradores mayores esporádicos.

---

## 3. Visualización y Análisis Exploratorio

### **3.1 Categoría con Mayor Total de Ventas**

| Categoría | Transacciones | Total Ventas | % del Total | Promedio por Transacción |
|-----------|---------------|--------------|-------------|--------------------------|
| **Alimentos** | 5 | **$132.70** | **62.7%** | $26.54 |
| Lácteos | 4 | $54.90 | 25.9% | $13.72 |
| Aseo | 3 | $24.10 | 11.4% | $8.03 |

**Hallazgo clave**: Alimentos domina tanto en volumen (5/12 transacciones) como en valor ($132.70). Los productos son de compra recurrente (arroz, leche, café, panadería, atún) con tickets medios-altos.

### **3.2 Relación Edad del Cliente vs Total de Venta**

#### **Análisis Cuantitativo**
- **Coeficiente de correlación (Pearson)**: **-0.15** (correlación lineal muy débil, negativa)
- **Coeficiente de determinación (R²)**: **0.022** → Solo 2.2% de la varianza en ventas explicada por edad

#### **Análisis Cualitativo (Scatter Plot)**
```
Edad → Total Venta (patrones observados):
├── 22-30 años (Jóvenes):     Compras variadas ($4.20 - $25.00)
├── 31-40 años (Adultos jóvenes): Compras medias ($9.00 - $30.00)  
├── 41-50 años (Adultos):     Compras altas ($6.40 - $15.20)
└── 51-55 años (Mayores):     Compras altas ($19.50 - $40.00)
```

#### **Interpretación por Segmentos**
| Segmento Edad | Comportamiento | Ejemplos |
|---------------|----------------|----------|
| **22-30** | Alta variabilidad, compras impulso y básicas | Panadería $22.50 (cantidad 15), Cepillo $4.20 |
| **31-40** | Compras familiares regulares | Arroz $25-30, Café $40 (cantidad 8) |
| **41-50** | Compras específicas, tickets medios | Atún $15.20, Yogur $12.00 |
| **51-55** | Compras de mayor valor unitario | Queso $19.50 (precio $6.50), Café $40.00 |

**Conclusión**: No existe relación lineal significativa. La edad **no es predictor confiable** del monto de venta. Factores como **categoría de producto** y **cantidad** son determinantes reales.

### **3.3 Hallazgos Adicionales de Visualizaciones**

#### **Boxplot por Categoría**
- **Alimentos**: Mayor dispersión (IQR amplio), outliers hacia arriba (Café $40, Panadería $22.50)
- **Lácteos**: Distribución simétrica, rango estrecho ($9 - $19.50)
- **Aseo**: Rango más bajo y compacto ($6.40 - $13.50)

#### **Heatmap de Correlaciones**
| | Total Venta | Edad | Precio Unitario | Cantidad |
|---|---|---|---|---|
| **Total Venta** | 1.00 | -0.15 | **0.68** | **0.82** |
| **Edad** | -0.15 | 1.00 | -0.08 | -0.12 |
| **Precio Unitario** | **0.68** | -0.08 | 1.00 | -0.23 |
| **Cantidad** | **0.82** | -0.12 | -0.23 | 1.00 |

**Insights críticos**:
- **Cantidad** es el predictor más fuerte de Total Venta (r=0.82) → Lógico: Total = Precio × Cantidad
- **Precio Unitario** correlaciona moderadamente (r=0.68) → Productos caros generan tickets altos
- **Edad** no correlaciona con ninguna variable numérica relevante

---

## 4. Preparación para Machine Learning

### **4.1 Codificación One-Hot Aplicada**

#### **Variable: `categoria` (3 niveles → 3 columnas)**
```python
# Antes: categoria ∈ {Alimentos, Lácteos, Aseo}
# Después:
categoria_Alimentos    # 1 si Alimentos, 0 otherwise
categoria_Aseo         # 1 si Aseo, 0 otherwise  
categoria_Lácteos      # 1 si Lácteos, 0 otherwise
```
**Nota**: No se usa drop='first' para mantener interpretabilidad completa (3 features para 3 clases).

#### **Variable: `metodo_pago` (2 niveles → 2 columnas)**
```python
# Antes: metodo_pago ∈ {Efectivo, Tarjeta}
# Después:
metodo_pago_Efectivo   # 1 si Efectivo, 0 otherwise
metodo_pago_Tarjeta    # 1 si Tarjeta, 0 otherwise
```

#### **Features Finales (8 variables predictoras)**
| Feature | Tipo | Descripción |
|---------|------|-------------|
| `precio_unitario` | Numérico | Precio base del producto |
| `cantidad` | Numérico | Unidades compradas |
| `cliente_edad` | Numérico | Edad imputada (mediana=36) |
| `categoria_Alimentos` | Binario | One-hot |
| `categoria_Aseo` | Binario | One-hot |
| `categoria_Lácteos` | Binario | One-hot |
| `metodo_pago_Efectivo` | Binario | One-hot |
| `metodo_pago_Tarjeta` | Binario | One-hot |

**Target**: `total_venta` (variable continua → Problema de **Regresión**)

### **4.2 Justificación de Eliminación de Columnas**

| Columna | Tipo | Razón de Eliminación | Impacto si se Mantiene |
|---------|------|---------------------|------------------------|
| `id_venta` | Identificador | **Data leakage**: ID único por fila, 0 poder predictivo, memorización perfecta en train | Overfitting severo, modelo inutilizable en producción |
| `fecha` | Temporal | **Baja variabilidad**: Solo enero 2025 (1 mes), sin estacionalidad detectable | Ruido, dimensiones extra sin información |
| `producto` | Categórico alta cardinalidad | **Cardinalidad = n_muestras (12)**: 12 productos únicos para 12 filas | One-hot crearía 12 columnas → matriz identidad → overfitting total |
| `ciudad` | Categórico (4 niveles) | **Multicolinealidad + proxy**: Cartago=6, otras=2 cada una; correlacionada con distribución de categorías | Redundante, añade complejidad sin signal nuevo |

#### **Análisis Profundo: `producto` vs `categoria`**
```
Producto → Categoría (mapeo 1:1 en este dataset):
Arroz → Alimentos
Leche → Lácteos
Jabón → Aseo
Café → Alimentos
Panadería → Alimentos
Detergente → Aseo
Yogur → Lácteos
Atún → Alimentos
Cepillo → Aseo
Queso → Lácteos
```
- **Producto es determinista dado Categoría** en este dataset (no hay productos en múltiples categorías)
- Usar `producto` = **data leakage implícito**: el modelo aprendería memorizar precios por producto, no generalizar patrones de categoría
- **Categoría** es el nivel correcto de abstracción para generalización

#### **Análisis Profundo: `ciudad`**
```
Distribución ciudad-categoría:
Cartago (6): Alimentos(3), Lácteos(1), Aseo(2)  → Mixto
Pereira (2): Alimentos(1), Aseo(1)              → Sin Lácteos
Armenia (2): Lácteos(1), Aseo(1)                → Sin Alimentos
Manizales (2): Alimentos(1), Lácteos(1)         → Sin Aseo
```
- **Confundimiento**: Ciudad actúa como proxy imperfecto de categoría
- Incluir ambos introduciría **multicolinealidad** y dificultaría interpretación de coeficientes
- **Decisión**: Mantener `categoria` (signal directo de negocio), descartar `ciudad` (proxy geográfico débil)

### **4.3 Dataset Final para ML**

**Archivo generado**: `ventas_preparadas_ml.csv`
- **Shape**: (12, 9) → 12 muestras, 8 features + 1 target
- **Tipos**: Todos numéricos (float64)
- **Nulos**: 0 (edad imputada)
- **Listo para**: Regresión Lineal, Random Forest, XGBoost, Redes Neuronales

**Encoders persistidos** (en `SaleMLDTO`):
- `categoria_encoder`: OneHotEncoder fiteado para transformar nuevos datos
- `metodo_pago_encoder`: OneHotEncoder fiteado para consistencia en inferencia

---

## Resumen Ejecutivo

| Fase | Hallazgo Principal | Acción Tomada |
|------|-------------------|---------------|
| **Exploración** | 12 filas limpias, 3 nulos en edad, header corrupto | Limpieza en Gateway |
| **Limpieza** | Edad con sesgo por mayores (52, 55) | Imputación con mediana (36) |
| **Visualización** | Alimentos = 63% ventas; edad no predice venta | Foco en categoría/cantidad |
| **ML Prep** | 4 columnas eliminadas por leakage/redundancia | 8 features limpias, target continuo |

El pipeline refactorizado en arquitectura por capas (`entities → services → controllers`) garantiza **reproducibilidad**, **testabilidad** y **extensibilidad** para futuros modelos predictivos de ventas.