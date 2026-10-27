"""Resultado del entrenamiento del perceptrón."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PerceptronTrainingDTO:
    """Pesos, sesgo e historial obtenidos al entrenar el modelo."""

    weights: Tuple[float, ...]
    bias: float
    losses: Tuple[float, ...]
    accuracies: Tuple[float, ...]
