"""Resultado del entrenamiento del perceptrón."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PerceptronTrainingDTO:
    """Pesos, sesgo e historial obtenidos al entrenar el modelo.

    Attributes:
        weights: Pesos finales de cada variable de entrada.
        bias: Sesgo final del modelo.
        losses: Pérdida registrada en cada época.
        accuracies: Exactitud registrada en cada época.
    """

    weights: Tuple[float, ...]
    bias: float
    losses: Tuple[float, ...]
    accuracies: Tuple[float, ...]
