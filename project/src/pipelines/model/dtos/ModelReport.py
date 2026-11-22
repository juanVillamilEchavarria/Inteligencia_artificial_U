"""Reporte final de la comparación de modelos."""

from dataclasses import dataclass
from typing import Tuple

from pipelines.model.dtos.ModelScore import ModelScore


@dataclass(frozen=True)
class ModelReport:
    """Reúne las métricas, el mejor modelo y las rutas de los artefactos.

    Attributes:
        scores: Métricas de cada modelo candidato.
        bestModelName: Modelo seleccionado por F1 macro de validación cruzada.
        featureNames: Variables usadas como entrada.
        targetName: Variable que se intenta predecir.
        trainCount: Cantidad de filas de entrenamiento.
        testCount: Cantidad de filas de prueba.
        modelPath: Ruta del archivo joblib con el mejor modelo.
        metricsPath: Ruta del JSON con las métricas legibles.
        bestParams: Hiperparámetros del mejor modelo, si se optimizaron.
        bestConfusionMatrix: Matriz de confusión del mejor modelo en prueba.
    """

    scores: Tuple[ModelScore, ...]
    bestModelName: str
    featureNames: Tuple[str, ...]
    targetName: str
    trainCount: int
    testCount: int
    modelPath: str
    metricsPath: str
    bestParams: str = ""
    bestConfusionMatrix: Tuple[Tuple[int, int], Tuple[int, int]] = ((0, 0), (0, 0))
