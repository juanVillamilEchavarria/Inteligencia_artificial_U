"""Reporte del pipeline de regresión."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RegressionReport:
    """Métricas y coeficientes del modelo de regresión lineal.

    Attributes:
        mae: Error absoluto medio en kg/ha.
        rmse: Raíz del error cuadrático medio en kg/ha.
        r2: Coeficiente de determinación.
        coefficients: Coeficiente de cada variable de entrada.
        intercept: Término independiente del modelo.
        featureNames: Variables usadas como entrada.
        trainCount: Cantidad de registros de entrenamiento.
        testCount: Cantidad de registros de prueba.
        averageYield: Rendimiento promedio del dataset completo.
    """

    mae: float
    rmse: float
    r2: float
    coefficients: Tuple[float, ...]
    intercept: float
    featureNames: Tuple[str, ...]
    trainCount: int
    testCount: int
    averageYield: float
