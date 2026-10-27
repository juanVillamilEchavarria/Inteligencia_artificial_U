# Resumen EDA y limpieza - Grupo 07

## Dimensiones
- Filas: 84
- Columnas: 5

## Valores nulos y duplicados
- Total de nulos: 3
- Columnas con nulos: {'distancia_km': 3}
- Duplicados exactos: 4
- IDs duplicados: 4

## Distribuciones
- Rutas únicas: 5
- Distribución por ruta: {'Ruta 2': 20, 'Ruta 1': 19, 'Ruta 3': 16, 'Ruta 5': 15, 'Ruta 4': 14}
- Distribución del objetivo: {0: 47, 1: 37}

## Estadísticas numéricas
| Columna | Media | Desv. estándar | Mínimo | Mediana | Máximo |
|---|---:|---:|---:|---:|---:|
| toneladas_recogidas | 52.2762 | 402.8127 | 2.3000 | 7.9500 | 3700.0000 |
| distancia_km | 22.1370 | 11.5981 | -24.4000 | 23.8000 | 38.9000 |
| ruta_retrasada | 0.4405 | 0.4994 | 0.0000 | 0.0000 | 1.0000 |

## Correlaciones
- `toneladasVsRetraso`: -0.0900
- `distanciaVsRetraso`: 0.3518
- `toneladasVsDistancia`: 0.1132

## Tabla antes / después
| Momento | Filas | Columnas | Nulos | Clase 0 | Clase 1 |
|---------|------:|---------:|------:|--------:|--------:|
| Dataset original | 84 | 5 | 3 | 47 | 37 |
| Después de limpieza | 80 | 5 | 0 | 46 | 34 |
| Después de preparación | 80 | 5 | 0 | - | - |

## Limpieza de datos
- Duplicados eliminados: 4
- IDs duplicados detectados: R019, R010, R008, R067
- Filas inválidas eliminadas: 0
- Columnas de texto normalizadas: recorrido_id, ruta

### Correcciones
| ID | Columna | Valor original | Valor corregido | Motivo |
|----|---------|---------------:|----------------:|--------|
| R031 | toneladas_recogidas | 3700.0 | 3.7 | Valor en kilogramos exportado como toneladas; se dividió entre 1000. |
| R035 | distancia_km | -24.4 | 24.4 | La distancia no puede ser negativa; se corrigió el signo. |

### Imputaciones
| Columna | Estrategia | Valor | Nulos imputados |
|---------|-----------|-------|----------------:|
| distancia_km | median | 23.9000 | 3 |

### Valor sospechoso
- toneladas_recogidas = 3700.0000. Media antes: 52.2762; media después: 8.1238. Desviación antes: 402.8127; después: 3.7605.

---
*Resumen generado automáticamente el 27/10/2026 01:40:02 por el módulo de preparación de datos del Grupo 07.*
