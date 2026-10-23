"""Estado compartido entre los pasos de preparación de datos."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import pandas as pd

from pipelines.transform.dtos.EdaReport import EdaReport
from pipelines.transform.dtos.CleaningReport import CleaningReport


@dataclass(frozen=True)
class DataPreparationContext:
    """Datos y reportes que se van construyendo durante la preparación."""

    dfRaw: Optional[pd.DataFrame] = None
    dfClean: Optional[pd.DataFrame] = None
    dfPrepared: Optional[pd.DataFrame] = None
    edaReport: Optional[EdaReport] = None
    cleaningReport: Optional[CleaningReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)