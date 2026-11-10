"""Estado compartido entre los pasos de preparación de datos."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

import pandas as pd


@dataclass(frozen=True)
class DataPreparationContext:
    """Datos que van dejando los pasos del pipeline de preparación.

    Cada paso recibe una copia y devuelve una nueva con los campos que completó.
    """

    dfRaw: Optional[pd.DataFrame] = None
    dfPrepared: Optional[pd.DataFrame] = None
    featureNames: Tuple[str, ...] = ()
    targetName: str = ""
    X: Optional[pd.DataFrame] = None
    y: Optional[pd.Series] = None
    X_train: Optional[pd.DataFrame] = None
    X_test: Optional[pd.DataFrame] = None
    y_train: Optional[pd.Series] = None
    y_test: Optional[pd.Series] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
