from services.MovementGraphicsService import MovementGraphicsService

class MovementGraphicsController:
    def __init__(self, movementGraphicsService: MovementGraphicsService):
        self.service = movementGraphicsService

    def generateAll(self):
        self.service.generateAll()
    def generateAmountHistogram(self):
        self.service.generateAmountHistogram()
    def generateScatterPlot(self):
        self.service.generateScatterPlot()
    def generateCategoryBoxplot(self):
        self.service.generateCategoryBoxplot()
