from outputs.visualization.MatplotlibChartRenderer import MatplotlibChartRenderer

class MovementGraphicsController:
    def __init__(self, chartRenderer: MatplotlibChartRenderer):
        self.service = chartRenderer

    def generateAll(self):
        self.service.generateAll()
    def generateAmountHistogram(self):
        self.service.generateAmountHistogram()
    def generateScatterPlot(self):
        self.service.generateScatterPlot()
    def generateCategoryBoxplot(self):
        self.service.generateCategoryBoxplot()
