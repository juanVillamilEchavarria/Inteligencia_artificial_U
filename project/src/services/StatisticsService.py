"""Cálculos estadísticos básicos sobre los movimientos financieros."""

from api.MovementsGateWay import MovementsGateWay
from app_collections.MovementsCollection import MovementsCollection
from enums.MovementFilteringKeys import MovementFilteringKeys
from entities.Movement import Movement


class StatisticsService:
    """Consulta los movimientos y calcula totales, promedios y extremos."""

    def __init__(self):
        """Carga los movimientos desde la fuente de datos."""
        self.movements: MovementsCollection = MovementsGateWay.getData()

    def getExpenses(self) -> list[Movement]:
        """Devuelve únicamente los movimientos de tipo Gasto."""
        return self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Gasto')

    def getIncomes(self):
        """Devuelve únicamente los movimientos de tipo Ingreso."""
        return self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Ingreso')

    def getTotalExpenses(self):
        """Suma los montos de todos los gastos."""
        return sum(mov.monto for mov in self.getExpenses())

    def getTotalIncomes(self):
        """Suma los montos de todos los ingresos."""
        return sum(mov.monto for mov in self.getIncomes())

    def getExpensesAverage(self):
        """Calcula el gasto promedio; retorna 0 si no hay gastos."""
        expenses = self.getExpenses()
        if len(expenses) == 0:
            return 0
        return self.getTotalExpenses() / len(expenses)

    def getIncomesAverage(self):
        """Calcula el ingreso promedio; retorna 0 si no hay ingresos."""
        incomes = self.getIncomes()
        if len(incomes) == 0:
            return 0
        return self.getTotalIncomes() / len(incomes)

    def getTotalExpensesForAnAccount(self, account: str):
        """Suma los gastos asociados a una cuenta específica."""
        movements = self.movements.getByKey(MovementFilteringKeys.CUENTA, account)
        total = 0
        for movimiento in movements:
            if movimiento['tipo_movimiento'] == 'Gasto':
                total += movimiento['monto']
        return total

    def getTotalIncomesForAnAccount(self, account: str):
        """Suma los ingresos asociados a una cuenta específica."""
        movements = self.movements.getByKey(MovementFilteringKeys.CUENTA, account)
        total = 0
        for movimiento in movements:
            if movimiento['tipo_movimiento'] == 'Ingreso':
                total += movimiento['monto']
        return total

    def getMinExpense(self):
        """Devuelve el gasto de menor valor."""
        return min(mov.monto for mov in self.getExpenses())

    def getMaxExpense(self):
        """Devuelve el gasto de mayor valor."""
        return max(mov.monto for mov in self.getExpenses())

    def getMinIncome(self):
        """Devuelve el ingreso de menor valor."""
        return min(mov.monto for mov in self.getIncomes())

    def getMaxIncome(self):
        """Devuelve el ingreso de mayor valor."""
        return max(mov.monto for mov in self.getIncomes())
