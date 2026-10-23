"""Reporte de los cambios realizados durante la limpieza."""

from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class ImputationRecord:
    """Describe cómo se completó una columna con valores nulos.

    Attributes:
        column: Nombre de la columna imputada.
        strategy: Estrategia usada, ``median`` o ``mode``.
        filledValue: Valor que se usó para completar los nulos.
        nullsCount: Cantidad de nulos que se llenaron.
    """

    column: str
    strategy: str
    filledValue: Any
    nullsCount: int


@dataclass(frozen=True)
class CleaningReport:
    """Resume el estado del dataset antes y después de limpiarlo."""

    rowsBefore: int
    rowsAfter: int
    columnsBefore: int
    columnsAfter: int
    nullsBefore: int
    nullsAfter: int
    duplicatesRemoved: int
    imputations: Tuple[ImputationRecord, ...]
    fechaConverted: bool
    normalizedColumns: Tuple[str, ...] = ()
    outliersKept: int = 0
    invalidDatesRemoved: int = 0
    invalidAmountsRemoved: int = 0
