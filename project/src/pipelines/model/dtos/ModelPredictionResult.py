"""Resultado de clasificar un movimiento nuevo con el modelo de Scikit-Learn."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPredictionResult:
    """Probabilidad y etiqueta asignadas a un caso.

    Attributes:
        monto: Monto original en pesos.
        mes: Mes del movimiento (1-12).
        diaSemana: Día de la semana (0 = lunes, 6 = domingo).
        probability: Probabilidad de que sea ingreso.
        label: 1 si se clasifica como ingreso, 0 si es gasto.
    """

    monto: float
    mes: int
    diaSemana: int
    probability: float
    label: int
