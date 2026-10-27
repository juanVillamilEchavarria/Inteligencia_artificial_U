"""Fachada para consultar estadísticas básicas de los recorridos."""

from services.RecorridoStatisticsService import RecorridoStatisticsService


class RecorridoController:
    """Expone los cálculos estadísticos sin acoplar los entry points al servicio."""

    def __init__(self, recorridoService: RecorridoStatisticsService):
        """Recibe el servicio que contiene la lógica de cálculo."""
        self.service = recorridoService

    def getDelayRate(self) -> float:
        """Devuelve la proporción de recorridos retrasados."""
        return self.service.getDelayRate()

    def getAverageTonnage(self) -> float:
        """Devuelve el promedio de toneladas recogidas."""
        return self.service.getAverageTonnage()

    def getAverageDistance(self) -> float:
        """Devuelve el promedio de distancia recorrida."""
        return self.service.getAverageDistance()

    def getDelayRateByRoute(self) -> dict[str, float]:
        """Devuelve la tasa de retraso por ruta."""
        return self.service.getDelayRateByRoute()

    def getDelayRateByDistanceThreshold(self, threshold: float) -> dict[str, float]:
        """Devuelve la tasa de retraso por encima y por debajo de una distancia."""
        return self.service.getDelayRateByDistanceThreshold(threshold)
