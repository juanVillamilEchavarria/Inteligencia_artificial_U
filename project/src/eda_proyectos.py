import numpy as np
from services.MovementNumPyStatisticsService import MovementNumPyStatisticsService
from services.MovementGraphicsService import MovementGraphicsService
from controllers.MovementGraphicsController import MovementGraphicsController
from helpers.output_helpers import print_separator
from dto.MovementNumPyDTO import MovementNumPyDTO

def print_stats(title: str, stats: MovementNumPyDTO ):
    print(f"\n   {title}")
    print(f"     Cantidad    : {stats.count}")
    print(f"     Suma total  : ${stats.sum:,.2f}")
    print(f"     Media       : ${stats.average:,.2f}")  
    print(f"     Mediana     : ${stats.median:,.2f}")
    print(f"     Desv. Std   : ${stats.std:,.2f}")
    print(f"     Mínimo      : ${stats.min:,.2f}")
    print(f"     Máximo      : ${stats.max:,.2f}")


def main():
    numpy_service = MovementNumPyStatisticsService()
    graphics_service = MovementGraphicsService(numpy_service)
    graphics_controller = MovementGraphicsController(graphics_service)

    print_separator("ANÁLISIS EXPLORATORIO DE DATOS - LEO COUNTER AI")

    incomes_stats = numpy_service.getAllIncomesStats()
    expenses_stats = numpy_service.getAllExpensesStats()
    all_stats = numpy_service.getAllAmountsStats()

    print_stats("INGRESOS", incomes_stats)
    print_stats("GASTOS", expenses_stats)
    print_stats("TODOS LOS MONTOS", all_stats)

    print_separator("GASTOS POR CATEGORÍA")
    category_stats = numpy_service.getStatsByCategory()
    for cat, stats in category_stats.items():
        print(f"\n   {cat}")
        print(f"     Total: ${stats.sum:,.2f} | Media: ${stats.median:,.2f} | Std: ${stats.std:,.2f}")
    graphics_controller.generateAll()

    print_separator("EDA COMPLETADO")
    print("  Gráficos guardados en: /charts/")
    print()


if __name__ == "__main__":
    main()