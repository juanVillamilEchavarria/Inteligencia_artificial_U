# Clase 12 - Scikit-Learn: entrenar, evaluar y guardar modelos

Implementación de la actividad práctica de la Clase 12 usando la misma filosofía de arquitectura del proyecto `project/`: capas separadas, pipelines con pasos atómicos, contextos inmutables, DTOs tipados, servicios sin efectos secundarios y entry points delgados.

> **Fuente de los datos:** la carpeta `clase10/` no existe en el repositorio. El dataset `cultivos_cartago.csv` se copió desde `clase_9/data/cultivos_cartago.csv`, que contiene los mismos 120 lotes, 4 columnas y la misma variable objetivo `cosecha_exitosa`.

## 1. Qué incluye

Los cinco pasos de la clase:

| Paso | Script | Resultado |
|---|---|---|
| 1 | `src/clasificar_cultivos.py` | Compara regresión logística, KNN y árbol; matriz de confusión; guarda el mejor modelo |
| 2 | `src/usar_modelo.py` | Carga el modelo y predice 3 lotes nuevos |
| 3 | `src/regresion_rendimiento.py` | Genera datos simulados, entrena regresión lineal y mide MAE, RMSE y R² |
| 4 | `src/red_xor.py` | Compara una neurona contra una red neuronal en XOR |
| 5 | `src/profundidad_arbol.py` | Entrena árboles de profundidad 1 a 12 y muestra el sobreajuste |

No se incluye la sección del modelo del proyecto final porque depende de los datos y el repositorio de cada grupo. El README deja indicado cómo adaptar el paso 1.

## 2. Arquitectura

```text
clase_12/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── data/
│   ├── cultivos_cartago.csv
│   └── rendimiento_cartago.csv        # lo genera el paso 3
├── notebooks/
└── src/
    ├── api/
    │   └── CropDataGateway.py         # acceso al CSV
    ├── entities/
    │   └── CropLot.py                 # entidad de dominio
    ├── app_collections/
    │   └── CropLotsCollection.py      # colección + to_dataframe()
    ├── enums/
    │   └── CropColumns.py             # nombres de columnas
    ├── dto/
    │   ├── CandidateModel.py
    │   └── PredictionResult.py
    ├── services/
    │   ├── ClassificationService.py
    │   ├── RegressionService.py
    │   ├── SyntheticDataService.py
    │   ├── XorService.py
    │   ├── OverfittingService.py
    │   └── ModelPersistenceService.py
    ├── pipelines/
    │   ├── core/                      # Pipeline y PipelineStep genéricos
    │   ├── transform/                 # carga, validación, selección y split
    │   ├── classification/            # comparación y selección del mejor modelo
    │   ├── regression/                # entrenamiento y evaluación de regresión
    │   ├── xor/                       # experimento XOR
    │   └── overfitting/               # estudio de profundidad
    ├── controllers/                   # fachadas de cada caso de uso
    ├── outputs/visualization/         # gráficos con Matplotlib
    ├── helpers/                       # rutas y utilidades de consola
    ├── charts/                        # PNG generados
    ├── models/                        # .joblib generado
    └── los cinco entry points
```

### Responsabilidades

- **`api/`**: única fuente de lectura del CSV.
- **`entities/` y `app_collections/`**: representación tipada de los lotes y conversión a DataFrame.
- **`services/`**: lógica pura de Scikit-Learn, métricas y persistencia. No imprimen ni grafican.
- **`pipelines/`**: orquestación. Cada paso recibe un contexto `@dataclass(frozen=True)` y devuelve una copia con `dataclasses.replace`.
- **`controllers/`**: fachadas que desacoplan los scripts de los pipelines.
- **`outputs/`**: solo generan artefactos (imágenes) a partir de datos ya procesados.
- **`helpers/`**: rutas canónicas y utilidades de terminal.
- **Entry points**: composición, ejecución y presentación de resultados.

## 3. Ejecución con Docker

Desde `clase_12/`:

```bash
docker compose up -d --build
docker exec -it ia_python bash
cd /app/src
python clasificar_cultivos.py
python usar_modelo.py
python regresion_rendimiento.py
python red_xor.py
python profundidad_arbol.py
exit
```

Si existe un contenedor anterior con el mismo nombre:

```bash
docker stop ia_python
docker rm ia_python
docker compose up -d --build
```

## 4. Ejecución sin Docker

Con Python 3.14 y las dependencias instaladas:

```bash
cd clase_12
pip install -r requirements.txt
cd src
python clasificar_cultivos.py
python usar_modelo.py
python regresion_rendimiento.py
python red_xor.py
python profundidad_arbol.py
```

## 5. Salidas esperadas

- `src/models/modelo_cultivos.joblib`: mejor modelo de clasificación.
- `src/charts/matriz_confusion.png`: matriz de confusión del mejor modelo.
- `src/charts/real_vs_predicho.png`: gráfico de regresión.
- `src/charts/sobreajuste_arbol.png`: curvas de entrenamiento y prueba.
- `data/rendimiento_cartago.csv`: dataset simulado de regresión.

Los resultados son cercanos a los de la guía: la regresión logística suele ganar por F1, la regresión lineal alcanza un R² alrededor de 0.90, XOR pasa de 50 % con una neurona a 100 % con la red, y el árbol empieza a memorizar desde profundidades cercanas a 7.

## 6. Decisiones de diseño

- Se usa **Scikit-Learn** para el entrenamiento y la evaluación, en lugar de reimplementar la matemática con NumPy.
- Se usa **Matplotlib** para los gráficos; no se requiere Seaborn.
- Los artefactos se separan en `src/charts/` y `src/models/` para no mezclar código con salidas.
- Se mantiene un `Pipeline` genérico en `pipelines/core/` para no repetir cuatro orquestadores idénticos; cada caso de uso conserva su runner y sus pasos.
- El dataset de cultivos no se mueve: se copió desde `clase_9/data/` a `clase_12/data/`.

## 7. Adaptación al proyecto final

Para el proyecto final, el esquema es el mismo:

1. Crear `src/modelo_proyecto.py` a partir de `clasificar_cultivos.py` si se predice una clase, o de `regresion_rendimiento.py` si se predice un número.
2. Reemplazar el gateway y las columnas por los datos limpios del proyecto.
3. Convertir columnas de texto con `pd.get_dummies` o `TfidfVectorizer` dentro del `Pipeline`.
4. Mantener `test_size=0.2`, `random_state=42` y `stratify=y` en clasificación.
5. Comparar al menos dos modelos con validación cruzada y elegir la métrica según el error más grave.
6. Guardar el mejor modelo con `joblib` y crear `src/usar_modelo.py` para la demostración.
