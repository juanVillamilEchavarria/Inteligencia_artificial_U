"""Estado compartido del pipeline de sobreajuste."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from pipelines.overfitting.dtos.OverfittingReport import (
    DepthScore,
    OverfittingReport,
)
from pipelines.transform.DataPreparationContext import DataPreparationContext


@dataclass(frozen=True)
class OverfittingContext:
    """Datos que van dejando los pasos del estudio de profundidad."""

    data: Optional[DataPreparationContext] = None
    scores: Tuple[DepthScore, ...] = ()
    report: Optional[OverfittingReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
