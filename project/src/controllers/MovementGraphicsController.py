"""Controlador de los gráficos exploratorios de movimientos."""

from outputs.visualization.MatplotlibChartRenderer import MatplotlibChartRenderer


class MovementGraphicsController:
    """Delega en el renderizador la generación de cada gráfico."""

    def __init__(self, chartRenderer: MatplotlibChartRenderer):
        """Recibe el renderizador que dibuja y guarda las figuras."""
        self.service = chartRenderer

    def generateAll(self):
        """Genera todos los gráficos exploratorios disponibles."""
        self.service.generateAll()

    def generateAmountHistogram(self):
        """Genera el histograma de montos."""
        self.service.generateAmountHistogram()

    def generateScatterPlot(self):
        """Genera el diagrama de dispersión de monto contra fecha."""
        self.service.generateScatterPlot()

    def generateCategoryBoxplot(self):
        """Genera el diagrama de caja de montos por categoría."""
        self.service.generateCategoryBoxplot()
