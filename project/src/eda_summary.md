# Resumen EDA - Leo Counter (Pandas + Seaborn)

## Dimensiones
- Filas: 120
- Columnas: 8

## Valores Nulos
- Total nulos: 0
- Columnas con nulos: {}

## Distribución Tipo Movimiento
{'Gasto': 86, 'Ingreso': 34}

## Top 5 Categorías
{'Vivienda': 16, 'Servicios Públicos': 16, 'Nómina': 15, 'Alimentación': 12, 'Entretenimiento': 10}

## Top 5 Cuentas
{'Nequi': 21, 'Banco Bogota': 20, 'Bancolombia': 17, 'Davivienda': 15, 'Efectivo': 12}

## Análisis Monto
- Skewness: 7.0951
- Kurtosis: 64.1520
- Outliers IQR: 18 (15.0%)
- Rango IQR: [$-1,694,375.00 , $3,056,625.00]

## Ingresos vs Gastos
- Ingresos: 34 (Media: $2,911,944, Mediana: $2,750,000, Máx: $25,000,000)
- Gastos: 86 (Media: $437,928, Mediana: $165,000, Máx: $3,500,000)

## Tabla antes / después
| Momento | Filas | Columnas | Nulos |
|---------|------:|---------:|------:|
| Dataset original | 120 | 8 | 0 |
| Después de limpieza | 120 | 8 | 0 |
| Después de preparación | 120 | 39 | 0 |

## Limpieza de Datos
- Filas antes: 120
- Filas después: 120
- Duplicados eliminados: 0
- Filas con fecha inválida eliminadas: 0
- Filas con monto inválido o no positivo eliminadas: 0
- Outliers conservados (IQR): 18
- Columnas de texto normalizadas: id, nombre, cuenta, categoria, tipo_movimiento, descripcion
- Columna 'fecha' convertida a datetime: Sí

No se requirieron imputaciones (dataset sin nulos).

---
*Resumen generado automáticamente el 22/11/2026 20:49:02 por Leo Counter AI - Módulo de Preparación de Datos.*
