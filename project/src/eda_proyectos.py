"""Análisis exploratorio con NumPy y gráficos básicos con Matplotlib."""

from services.NumpyStatisticsService import NumpyStatisticsService
from outputs.visualization.MatplotlibChartRenderer import MatplotlibChartRenderer
from controllers.MovementGraphicsController import MovementGraphicsController
from helpers.output_helpers import print_separator
from helpers.project_paths import CHARTS_DIR
from dto.MovementNumPyDTO import MovementNumPyDTO

def print_stats(title: str, stats: MovementNumPyDTO):
    """Imprime las estadísticas de un conjunto de montos."""
    print(f"\n   {title}")
    print(f"     Cantidad    : {stats.count}")
    print(f"     Suma total  : ${stats.sum:,.2f}")
    print(f"     Media       : ${stats.average:,.2f}")
    print(f"     Mediana     : ${stats.median:,.2f}")
    print(f"     Desv. Std   : ${stats.std:,.2f}")
    print(f"     Mínimo      : ${stats.min:,.2f}")
    print(f"     Máximo      : ${stats.max:,.2f}")


def main():
    """Calcula las estadísticas, las muestra y genera los gráficos del EDA."""
    numpy_service = NumpyStatisticsService()
    chart_renderer = MatplotlibChartRenderer(numpy_service)
    graphics_controller = MovementGraphicsController(chart_renderer)

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
    print(f"  Gráficos guardados en: {CHARTS_DIR}/")
    print()


if __name__ == "__main__":
    main()
