"""Cálculos estadísticos básicos sobre los recorridos de recolección."""

from api.RecorridosGateWay import RecorridosGateWay
from app_collections.RecorridosCollection import RecorridosCollection
from entities.Recorrido import Recorrido
from enums.RecorridoFilteringKeys import RecorridoFilteringKeys


class RecorridoStatisticsService:
    """Consulta los recorridos y calcula tasas, promedios y agrupaciones."""

    def __init__(self):
        """Carga los recorridos desde la fuente de datos."""
        self.recorridos: RecorridosCollection = RecorridosGateWay.getData()

    def getDelayed(self) -> list[Recorrido]:
        """Devuelve únicamente los recorridos que terminaron con retraso."""
        return self.recorridos.getByKey(RecorridoFilteringKeys.RUTA_RETRASADA, 1)

    def getOnTime(self) -> list[Recorrido]:
        """Devuelve únicamente los recorridos que terminaron a tiempo."""
        return self.recorridos.getByKey(RecorridoFilteringKeys.RUTA_RETRASADA, 0)

    def getDelayRate(self) -> float:
        """Calcula la proporción de recorridos retrasados."""
        total = self.recorridos.count()
        if total == 0:
            return 0.0
        return len(self.getDelayed()) / total

    def getAverageTonnage(self) -> float:
        """Calcula el promedio de toneladas recogidas."""
        items = self.recorridos.getItems()
        if not items:
            return 0.0
        return sum(item.toneladas_recogidas for item in items) / len(items)

    def getAverageDistance(self) -> float:
        """Calcula el promedio de distancia recorrida."""
        items = self.recorridos.getItems()
        if not items:
            return 0.0
        return sum(item.distancia_km for item in items) / len(items)

    def getDelayRateByRoute(self) -> dict[str, float]:
        """Calcula la tasa de retraso para cada ruta."""
        result = {}
        for ruta in sorted({item.ruta for item in self.recorridos.getItems()}):
            items = self.recorridos.getByKey(RecorridoFilteringKeys.RUTA, ruta)
            if not items:
                continue
            result[ruta] = sum(item.ruta_retrasada for item in items) / len(items)
        return result

    def getDelayRateByDistanceThreshold(self, threshold: float) -> dict[str, float]:
        """Compara la tasa de retraso por encima y por debajo de una distancia."""
        items = self.recorridos.getItems()
        groups = {"porDebajo": [], "porEncima": []}
        for item in items:
            key = "porEncima" if item.distancia_km >= threshold else "porDebajo"
            groups[key].append(item)

        result = {}
        for key, group in groups.items():
            if group:
                result[key] = sum(item.ruta_retrasada for item in group) / len(group)
        return result
