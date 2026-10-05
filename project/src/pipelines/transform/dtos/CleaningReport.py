from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class ImputationRecord:
    column: str
    strategy: str
    filledValue: Any
    nullsCount: int


@dataclass(frozen=True)
class CleaningReport:
    rowsBefore: int
    rowsAfter: int
    imputations: Tuple[ImputationRecord, ...]
    fechaConverted: bool