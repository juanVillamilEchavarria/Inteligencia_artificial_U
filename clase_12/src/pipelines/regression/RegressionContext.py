"""Estado compartido del pipeline de regresión."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import numpy as np

from pipelines.regression.dtos.RegressionReport import RegressionReport
from pipelines.transform.DataPreparationContext import DataPreparationContext


@dataclass(frozen=True)
class RegressionContext:
    """Datos que van dejando los pasos de la regresión lineal."""

    data: Optional[DataPreparationContext] = None
    model: Optional[Any] = None
    yPredicted: Optional[np.ndarray] = None
    report: Optional[RegressionReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
