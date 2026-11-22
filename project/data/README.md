# Datos del proyecto

## `datos_originales.json`

Archivo crudo de entrada del sistema. Contiene **120 movimientos financieros**
(86 gastos y 34 ingresos) con la misma estructura que entrega el sistema
**Leo Counter**:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | texto | Identificador único UUID v7 (120 IDs distintos, sin repeticiones) |
| `nombre` | texto | Nombre corto del movimiento |
| `cuenta` | texto | Cuenta o medio de pago asociado |
| `categoria` | texto | Categoría principal del movimiento |
| `tipo_movimiento` | texto | `Ingreso` o `Gasto` |
| `monto` | texto numérico | Valor en pesos colombianos (COP) |
| `fecha` | texto ISO | Fecha del movimiento (`AAAA-MM-DD`) |
| `descripcion` | texto | Descripción en lenguaje natural |

**Fuente:** datos de ejemplo del sistema Leo Counter (gestor de finanzas
personales para hogares y PyMEs), anonimizados y ampliados con movimientos
sintéticos coherentes para el proyecto académico. No contienen información
personal real. El período cubierto va de marzo de 2024 a septiembre de 2026.

**Calidad de los datos:** el archivo conserva algunos detalles realistas que el
pipeline corrige, por ejemplo espacios sobrantes en nombres de cuentas
(`"Banco Bogota "`). El resto de campos está completo: no hay nulos, montos no
positivos ni fechas inválidas.

## `proyecto_limpio.csv`

Dataset generado automáticamente por `src/data_preparation.py`. Contiene las
columnas originales normalizadas, las variables derivadas (`monto_log`,
`es_ingreso`, `mes`, `dia_semana`, `es_fin_semana`) y las columnas one-hot de
`categoria`, `tipo_movimiento` y `cuenta`.

> Este archivo se regenera con el pipeline; no se edita a mano.
