"""DTO con los resultados del análisis exploratorio de datos."""

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class EdaReport:
    """Resumen completo del dataset antes de aplicar la limpieza."""

    shape: Tuple[int, int]
    nullCounts: Dict[str, int]
    totalNulls: int
    dtypes: Dict[str, str]
    duplicatesExact: int
    duplicatesById: int
    uniqueRoutes: int
    routeDist: Dict[str, int]
    targetDist: Dict[int, int]
    numericSummary: Dict[str, Dict[str, float]]
    correlations: Dict[str, float]
    head: Dict = field(default_factory=dict)
    describe: Dict = field(default_factory=dict)
