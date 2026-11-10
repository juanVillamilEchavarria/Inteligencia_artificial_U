"""Reporte del experimento de sobreajuste con árboles de decisión."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DepthScore:
    """Exactitud de un árbol para una profundidad determinada."""

    depth: int
    trainAccuracy: float
    testAccuracy: float


@dataclass(frozen=True)
class OverfittingReport:
    """Resultados de entrenar árboles con profundidades crecientes.

    Attributes:
        scores: Exactitud de entrenamiento y prueba por profundidad.
    """

    scores: Tuple[DepthScore, ...]
