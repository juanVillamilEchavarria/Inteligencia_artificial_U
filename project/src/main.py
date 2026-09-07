from controllers.MovementController import MovementController
from services.MovementStatisticsService import MovementStatisticsService
from services.ReportGenerator import ReportGenerator

service = MovementStatisticsService()
controller = MovementController(service)

print('Total de ingresos: ', controller.getTotalIncomes())
print("Total de gastos:", controller.getTotalExpenses())
print("Promedio de ingresos: ", controller.getIncomesAverage())
print("Promedio de gastos: ", controller.getExpensesAverage())
print("Maximo ingreso: ", controller.getMaxIncome())
print("Minimo ingreso: ", controller.getMinIncome())
print("Maximo gasto: ", controller.getMaxExpense())
print("Minimo gasto: ", controller.getMinExpense())


report = ReportGenerator(controller)
report.generate()