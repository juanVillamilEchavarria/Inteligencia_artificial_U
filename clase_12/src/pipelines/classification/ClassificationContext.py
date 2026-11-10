"""Estado compartido del pipeline de clasificación."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from dto.CandidateModel import CandidateModel
from pipelines.classification.dtos.ClassificationReport import (
    ClassificationReport,
    ModelScore,
)
from pipelines.transform.DataPreparationContext import DataPreparationContext


@dataclass(frozen=True)
class ClassificationContext:
    """Datos que van dejando los pasos de comparación de modelos."""

    data: Optional[DataPreparationContext] = None
    candidates: Tuple[CandidateModel, ...] = ()
    scores: Tuple[ModelScore, ...] = ()
    bestModelName: str = ""
    bestModel: Optional[Any] = None
    report: Optional[ClassificationReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
