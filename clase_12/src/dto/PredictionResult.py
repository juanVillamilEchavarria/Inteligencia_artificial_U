"""Resultado de clasificar un lote nuevo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionResult:
    """Probabilidad y etiqueta asignadas a un lote.

    Attributes:
        precipitacion_mm: Lluvia del lote nuevo.
        temperatura_c: Temperatura del lote nuevo.
        probability: Probabilidad de que la cosecha sea exitosa.
        label: 1 si se predice exitosa, 0 si no.
    """

    precipitacion_mm: float
    temperatura_c: float
    probability: float
    label: int
