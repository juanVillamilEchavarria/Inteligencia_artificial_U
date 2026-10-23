"""Resultado de clasificar un movimiento nuevo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionResult:
    """Probabilidad y etiqueta asignadas a un caso.

    Attributes:
        monto: Monto original en pesos.
        mes: Mes del movimiento.
        probability: Probabilidad de que sea ingreso.
        label: 1 si se clasifica como ingreso, 0 si es gasto.
    """

    monto: float
    mes: int
    probability: float
    label: int
