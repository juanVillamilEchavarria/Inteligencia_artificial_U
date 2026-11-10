"""Reporte del experimento de la compuerta XOR."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class XorRow:
    """Predicciones de los dos modelos para una fila de XOR."""

    x1: int
    x2: int
    expected: int
    singleNeuron: int
    network: int


@dataclass(frozen=True)
class XorReport:
    """Comparación entre una neurona y una red neuronal.

    Attributes:
        rows: Predicciones para las cuatro combinaciones de XOR.
        singleNeuronAccuracy: Exactitud de la regresión logística.
        networkAccuracy: Exactitud del perceptrón multicapa.
    """

    rows: Tuple[XorRow, ...]
    singleNeuronAccuracy: float
    networkAccuracy: float
