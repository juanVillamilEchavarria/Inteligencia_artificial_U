"""Controlador de los gráficos exploratorios de recorridos."""

from outputs.visualization.SeabornChartRenderer import SeabornChartRenderer


class RecorridoGraphicsController:
    """Delega en el renderizador la generación de cada gráfico."""

    def __init__(self, chartRenderer: SeabornChartRenderer):
        """Recibe el renderizador que dibuja y guarda las figuras."""
        self.service = chartRenderer

    def generateAll(self) -> list:
        """Genera todos los gráficos exploratorios disponibles."""
        return self.service.generateAll()

    def generateScatterFeaturesTarget(self) -> str:
        """Genera la dispersión de las dos variables numéricas por clase."""
        return self.service.generateScatterFeaturesTarget()

    def generateBoxplotDistanceByTarget(self) -> str:
        """Genera el boxplot de distancia entre clases."""
        return self.service.generateBoxplotDistanceByTarget()
