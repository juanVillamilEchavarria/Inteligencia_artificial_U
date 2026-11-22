"""Estado compartido entre los pasos del pipeline de modelos."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

import pandas as pd

from dto.CandidateModel import CandidateModel
from pipelines.model.dtos.ModelReport import ModelReport
from pipelines.model.dtos.ModelScore import ModelScore


@dataclass(frozen=True)
class ModelTrainingContext:
    """Datos que van dejando los pasos del pipeline.

    Cada paso recibe una copia y devuelve una nueva con los campos que completó.
    """

    dfPrepared: Optional[pd.DataFrame] = None
    featureNames: Tuple[str, ...] = ()
    targetName: str = "es_ingreso"
    X: Optional[pd.DataFrame] = None
    y: Optional[pd.Series] = None
    XTrain: Optional[pd.DataFrame] = None
    XTest: Optional[pd.DataFrame] = None
    yTrain: Optional[pd.Series] = None
    yTest: Optional[pd.Series] = None
    candidates: Tuple[CandidateModel, ...] = ()
    scores: Tuple[ModelScore, ...] = ()
    bestModelName: str = ""
    bestModel: Optional[Any] = None
    report: Optional[ModelReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
