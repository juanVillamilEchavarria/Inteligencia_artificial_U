"""Reporte final del entrenamiento del perceptrón."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PerceptronReport:
    """Reúne el modelo ajustado y las métricas obtenidas."""

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
    misclassifiedCount: int
    losses: Tuple[float, ...]
    accuracies: Tuple[float, ...]
