"""Estado compartido del pipeline de XOR."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import numpy as np

from pipelines.xor.dtos.XorReport import XorReport


@dataclass(frozen=True)
class XorContext:
    """Datos que van dejando los pasos del experimento XOR."""

    X: Optional[np.ndarray] = None
    y: Optional[np.ndarray] = None
    singleNeuron: Optional[Any] = None
    network: Optional[Any] = None
    report: Optional[XorReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
