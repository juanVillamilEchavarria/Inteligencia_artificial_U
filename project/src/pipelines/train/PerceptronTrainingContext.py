"""Estado compartido entre los pasos del entrenamiento del perceptrón."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd

from dto.PerceptronTrainingDTO import PerceptronTrainingDTO
from pipelines.train.dtos.PerceptronReport import PerceptronReport


@dataclass(frozen=True)
class PerceptronTrainingContext:
    """Datos que van dejando los pasos del pipeline.

    Cada paso recibe una copia y devuelve una nueva con los campos que completó.
    """

    dfPrepared: Optional[pd.DataFrame] = None
    featureNames: Tuple[str, ...] = ()
    targetName: str = "es_ingreso"
    X: Optional[np.ndarray] = None
    y: Optional[np.ndarray] = None
    XScaled: Optional[np.ndarray] = None
    means: Optional[np.ndarray] = None
    stds: Optional[np.ndarray] = None
    training: Optional[PerceptronTrainingDTO] = None
    report: Optional[PerceptronReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
