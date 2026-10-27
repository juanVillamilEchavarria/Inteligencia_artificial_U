"""Reporte de los cambios realizados durante la limpieza."""

from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class ImputationRecord:
    """Describe cómo se completó una columna con valores nulos."""

    column: str
    strategy: str
    filledValue: Any
    nullsCount: int


@dataclass(frozen=True)
class CorrectionRecord:
    """Describe un valor corregido durante la limpieza."""

    recorridoId: str
    column: str
    originalValue: Any
    correctedValue: Any
    reason: str


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
    duplicateIds: Tuple[str, ...]
    imputations: Tuple[ImputationRecord, ...]
    corrections: Tuple[CorrectionRecord, ...]
    invalidRowsRemoved: int
    normalizedColumns: Tuple[str, ...]
    targetCountsBefore: Dict[int, int]
    targetCountsAfter: Dict[int, int]
    suspiciousColumn: str
    suspiciousValue: float
    meanBefore: float
    meanAfter: float
    stdBefore: float
    stdAfter: float
