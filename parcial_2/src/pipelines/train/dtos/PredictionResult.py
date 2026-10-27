"""Resultado de clasificar un recorrido nuevo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionResult:
    """Probabilidad y etiqueta asignadas a un recorrido nuevo."""

    toneladas: float
    distancia: float
    probability: float
    label: int
