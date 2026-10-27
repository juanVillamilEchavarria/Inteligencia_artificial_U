"""Estadísticas descriptivas de los recorridos usando NumPy."""

import numpy as np

from api.RecorridosGateWay import RecorridosGateWay
from app_collections.RecorridosCollection import RecorridosCollection
from dto.RecorridoNumPyDTO import RecorridoNumPyDTO


class NumpyStatisticsService:
    """Calcula medidas descriptivas y arreglos numéricos para el EDA."""

    def __init__(self):
        """Carga los recorridos desde la fuente de datos."""
        self.recorridos: RecorridosCollection = RecorridosGateWay.getData()

    def getTonnageArray(self) -> np.ndarray:
        """Retorna las toneladas recogidas como array NumPy."""
        return np.array([item.toneladas_recogidas for item in self.recorridos.getItems()])

    def getDistanceArray(self) -> np.ndarray:
        """Retorna las distancias como array NumPy."""
        return np.array([item.distancia_km for item in self.recorridos.getItems()])

    def getTargetArray(self) -> np.ndarray:
        """Retorna la variable objetivo como array NumPy."""
        return np.array([item.ruta_retrasada for item in self.recorridos.getItems()])

    def getStatsForArray(self, data: np.ndarray) -> RecorridoNumPyDTO:
        """Calcula las estadísticas descriptivas de un array."""
        if len(data) == 0:
            return RecorridoNumPyDTO(0, 0, 0, 0, 0, 0, 0)
        return RecorridoNumPyDTO(
            np.median(data),
            np.mean(data),
            np.std(data),
            np.min(data),
            np.max(data),
            len(data),
            np.sum(data),
        )

    def getTonnageStats(self) -> RecorridoNumPyDTO:
        """Estadísticas completas de las toneladas recogidas."""
        return self.getStatsForArray(self.getTonnageArray())

    def getDistanceStats(self) -> RecorridoNumPyDTO:
        """Estadísticas completas de las distancias."""
        return self.getStatsForArray(self.getDistanceArray())

    def getCorrelation(self, first: np.ndarray, second: np.ndarray) -> float:
        """Calcula la correlación de Pearson entre dos arrays."""
        return float(np.corrcoef(first, second)[0, 1])
