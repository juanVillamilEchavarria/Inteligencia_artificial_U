# Leo Counter AI - Informe Estadístico de Finanzas

## Descripción de los Datos

El presente informe analiza un dataset de **50 transacciones financieras** extraídas del sistema Leo Counter, un gestor de finanzas open-source para hogares y PyMEs. Los datos incluyen movimientos de tipo **Ingreso** y **Gasto** registrados en múltiples cuentas (Banco Bogotá, Nequi, Bancolombia, Davivienda, DaviPlata, Efectivo, entre otras), con montos expresados en pesos colombianos (COP).

Cada registro contiene: identificador único (UUID), nombre de la transacción, cuenta asociada, categoría, tipo de movimiento, monto, fecha y descripción en texto libre. El período abarcado comprende desde agosto de 2026 hasta junio de 2024.

---

## Estadísticas Calculadas

### Resumen General

| Métrica | Valor |
|---------|------:|
| Total de movimientos | 50 |
| Cantidad de ingresos | 14 |
| Cantidad de gastos | 36 |
| Balance neto | $26,150,200.00 |

### Ingresos

| Métrica | Valor |
|---------|------:|
| Total de ingresos | $40,835,100.00 |
| Promedio por ingreso | $2,916,792.86 |
| Ingreso máximo | $25,000,000.00 |
| Ingreso mínimo | $120,000.00 |

### Gastos

| Métrica | Valor |
|---------|------:|
| Total de gastos | $14,684,900.00 |
| Promedio por gasto | $407,913.89 |
| Gasto máximo | $3,500,000.00 |
| Gasto mínimo | $5,000.00 |

---

## Interpretación de los Resultados

### Análisis del Balance
El balance neto de **$26,150,200.00** indica que los ingresos superan a los gastos en el período analizado. Sin embargo, este resultado debe interpretarse con cautela: el ingreso máximo de **$25,000,000.00** corresponde a una venta extraordinaria (vehículo), lo que distorsiona el promedio. Al excluir este valor atípico, el comportamiento financiero real podría ser significativamente diferente.

### Análisis de Ingresos
El promedio de ingresos de **$2,916,792.86** está fuertemente influenciado por transacciones extraordinarias. La brecha entre el ingreso mínimo (**$120,000.00**) y el máximo (**$25,000,000.00**) es de **$24,880,000.00**, lo que evidencia alta variabilidad en las fuentes de ingreso. Esto es relevante para el modelo de **Puntaje Z**, ya que transacciones como la venta del vehículo serían detectadas como anomalías estadísticas.

### Análisis de Gastos
El gasto promedio de **$407,913.89** refleja un patrón de consumo distribuido en múltiples categorías. El gasto máximo (**$3,500,000.00**) corresponde a una compra de tecnología (laptop), mientras que el mínimo (**$5,000.00**) es un pasaje de transporte público. La dispersión entre estos valores confirma la necesidad de implementar **sub-categorías** mediante Naive Bayes, ya que agrupar todos los gastos en una sola categoría oculta patrones importantes de consumo.

### Relación con el Proyecto de IA
Estas estadísticas son la base para:
1. **Detección de anomalías**: El Puntaje Z utilizará la media y desviación estándar de estos montos para identificar transacciones atípicas en tiempo real.
2. **Clasificación semántica**: Las descripciones en texto libre asociadas a estos montos alimentarán el modelo Naive Bayes para detectar sub-categorías ocultas.
3. **Reportes inteligentes**: Estas métricas básicas evolucionarán hacia insights accionables cuando se integre el módulo de IA al sistema Leo Counter.

---

*Informe generado automáticamente el 07/09/2026 17:32:38 por Leo Counter AI - Módulo de Estadísticas.*
