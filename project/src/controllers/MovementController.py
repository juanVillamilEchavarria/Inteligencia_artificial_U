from services.MovementStatisticsService import MovementStatisticsService

class MovementController:
    def __init__(self, movementService: MovementStatisticsService):
        self.service = movementService

    def getTotalIncomes(self):
        return self.service.getTotalIncomes()
    def getTotalExpenses(self):
        return self.service.getTotalExpenses()
    def getExpensesAverage(self):
        return self.service.getExpensesAverage()
    def getIncomesAverage(self):
        return self.service.getIncomesAverage()
    def getMaxIncome(self):
        return self.service.getMaxIncome()
    def getMinIncome(self):
        return self.service.getMinIncome()
    def getMaxExpense(self):
        return self.service.getMaxExpense()
    def getMinExpense(self):
        return self.service.getMinExpense()