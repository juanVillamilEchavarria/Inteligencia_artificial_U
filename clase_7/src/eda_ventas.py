import numpy as np
from services.SalesNumPyStatisticsService import SalesNumPyStatisticsService
from services.SalesGraphicsService import SalesGraphicsService
from controllers.SalesGraphicsController import SalesGraphicsController
from helpers.output_helpers import print_separator
from dto.SaleNumPyDTO import SaleNumPyDTO


def print_stats(title: str, stats: SaleNumPyDTO):
    print(f"\n   {title}")
    print(f"     Cantidad    : {stats.count}")
    print(f"     Suma total  : ${stats.sum:,.2f}")
    print(f"     Media       : ${stats.average:,.2f}")  
    print(f"     Mediana     : ${stats.median:,.2f}")
    print(f"     Desv. Std   : ${stats.std:,.2f}")
    print(f"     Mínimo      : ${stats.min:,.2f}")
    print(f"     Máximo      : ${stats.max:,.2f}")


def main():
    from api.SalesDataGateway import SalesDataGateway
    
    gateway = SalesDataGateway('ventas_tienda.csv')
    collection = gateway.get_data()
    
    numpy_service = SalesNumPyStatisticsService(collection)
    graphics_service = SalesGraphicsService(numpy_service)
    graphics_controller = SalesGraphicsController(graphics_service)

    print_separator("ANÁLISIS EXPLORATORIO DE DATOS - VENTAS")

    total_venta_stats = numpy_service.get_total_venta_stats()
    edad_stats = numpy_service.get_edad_stats()

    print_stats("TOTAL VENTA", total_venta_stats)
    print_stats("EDAD CLIENTE", edad_stats)

    print_separator("VENTAS POR CATEGORÍA")
    category_stats = numpy_service.get_stats_by_category()
    for cat, stats in category_stats.items():
        print(f"\n   {cat}")
        print(f"     Total: ${stats.sum:,.2f} | Media: ${stats.average:,.2f} | Std: ${stats.std:,.2f}")

    print_separator("VENTAS POR MÉTODO DE PAGO")
    payment_stats = numpy_service.get_stats_by_payment_method()
    for method, stats in payment_stats.items():
        print(f"\n   {method}")
        print(f"     Total: ${stats.sum:,.2f} | Media: ${stats.average:,.2f} | Std: ${stats.std:,.2f}")

    graphics_controller.generate_all()

    print_separator("EDA COMPLETADO")
    print("  Gráficos guardados en: /charts/")
    print()


if __name__ == "__main__":
    main()