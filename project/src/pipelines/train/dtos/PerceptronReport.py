"""Reporte final del entrenamiento del perceptrón."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PerceptronReport:
    """Reúne el modelo ajustado y las métricas obtenidas.

    Attributes:
        featureNames: Variables usadas como entrada.
        targetName: Variable que se intenta predecir.
        weights: Pesos finales del modelo.
        bias: Sesgo final del modelo.
        initialLoss: Pérdida antes de la primera actualización.
        finalLoss: Pérdida al terminar el entrenamiento.
        initialAccuracy: Exactitud antes de entrenar.
        finalAccuracy: Exactitud al terminar el entrenamiento.
        baselineAccuracy: Exactitud de clasificar siempre la clase mayoritaria.
        positiveCount: Cantidad de ejemplos de la clase 1.
        negativeCount: Cantidad de ejemplos de la clase 0.
        losses: Historial de pérdida por época.
        accuracies: Historial de exactitud por época.
    """

    featureNames: Tuple[str, ...]
    targetName: str
    weights: Tuple[float, ...]
    bias: float
    initialLoss: float
    finalLoss: float
    initialAccuracy: float
    finalAccuracy: float
    baselineAccuracy: float
    positiveCount: int
    negativeCount: int
    losses: Tuple[float, ...]
    accuracies: Tuple[float, ...]
