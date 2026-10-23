"""Fachada para consultar estadísticas básicas de los movimientos."""

from services.StatisticsService import StatisticsService


class MovementController:
    """Expone los cálculos de estadísticas sin acoplar los entry points al servicio."""

    def __init__(self, movementService: StatisticsService):
        """Recibe el servicio que contiene la lógica de cálculo."""
        self.service = movementService

    def getTotalIncomes(self):
        """Devuelve la suma total de los ingresos."""
        return self.service.getTotalIncomes()

    def getTotalExpenses(self):
        """Devuelve la suma total de los gastos."""
        return self.service.getTotalExpenses()

    def getExpensesAverage(self):
        """Devuelve el promedio de los gastos."""
        return self.service.getExpensesAverage()

    def getIncomesAverage(self):
        """Devuelve el promedio de los ingresos."""
        return self.service.getIncomesAverage()

    def getMaxIncome(self):
        """Devuelve el ingreso de mayor valor."""
        return self.service.getMaxIncome()

    def getMinIncome(self):
        """Devuelve el ingreso de menor valor."""
        return self.service.getMinIncome()

    def getMaxExpense(self):
        """Devuelve el gasto de mayor valor."""
        return self.service.getMaxExpense()

    def getMinExpense(self):
        """Devuelve el gasto de menor valor."""
        return self.service.getMinExpense()
