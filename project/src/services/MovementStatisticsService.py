from api.MovementsGateWay import MovementsGateWay
from app_collections.MovementsCollection import MovementsCollection
from enums.MovementFilteringKeys import MovementFilteringKeys
from entities.Movement import Movement

class MovementStatisticsService:
    def __init__(self):
        self.movements : MovementsCollection = MovementsGateWay.getData()
    def getExpenses(self)-> list[Movement]:
        return self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Gasto')
    def getIncomes(self):
        return self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Ingreso')
    def getTotalExpenses(self):
        return sum(mov.monto for mov in self.getExpenses())

    def getTotalIncomes(self):
        return sum(mov.monto for mov in self.getIncomes())

    def getExpensesAverage(self):
        expenses = self.getExpenses()
        if len(expenses) == 0:
            return 0
        return self.getTotalExpenses() / len(expenses)

    def getIncomesAverage(self):
        incomes = self.getIncomes()
        if len(incomes) == 0:
            return 0
        return self.getTotalIncomes() / len(incomes)
    def getTotalExpensesForAnAccount(self, account: str):
        movements = self.movements.getByKey(MovementFilteringKeys.CUENTA, account)
        total = 0
        for movimiento in movements:
            if movimiento['tipo_movimiento'] == 'Gasto':
                total += movimiento['monto']
        return total
    def getTotalIncomesForAnAccount(self, account: str):
        movements = self.movements.getByKey(MovementFilteringKeys.CUENTA, account)
        total = 0
        for movimiento in movements:
            if movimiento['tipo_movimiento'] == 'Ingreso':
                total += movimiento['monto']
        return total
    def getMinExpense(self):
        return min(mov.monto for mov in self.getExpenses())
    def getMaxExpense(self):
        return max(mov.monto for mov in self.getExpenses())
    def getMinIncome(self):
        return min(mov.monto for mov in self.getIncomes())
    def getMaxIncome(self):
        return max(mov.monto for mov in self.getIncomes())
        
