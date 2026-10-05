from helpers.output_helpers import print_separator


def main():
    from api.SalesDataGateway import SalesDataGateway
    from services.SalesStatisticsService import SalesStatisticsService
    from services.SalesNumPyStatisticsService import SalesNumPyStatisticsService
    from services.SalesMLPreparationService import SalesMLPreparationService
    from services.SalesGraphicsService import SalesGraphicsService
    from controllers.SalesController import SalesController
    from controllers.SalesGraphicsController import SalesGraphicsController
    from controllers.SalesMLController import SalesMLController
    from services.SalesReportGenerator import SalesReportGenerator

    print_separator("PIPELINE COMPLETO DE VENTAS - ARQUITECTURA REFACTORIZADA")

    print("\n[1/5] Cargando datos...")
    gateway = SalesDataGateway('ventas_tienda.csv')
    collection = gateway.get_data()
    print(f"     {collection.count()} transacciones cargadas")

    print("\n[2/5] Generando estadísticas e informe...")
    stats_service = SalesStatisticsService(collection)
    controller = SalesController(stats_service)
    report = SalesReportGenerator(controller)
    report.generate('informe_ventas.md')
    print("\n[3/5] Ejecutando EDA y generando gráficos...")
    numpy_service = SalesNumPyStatisticsService(collection)
    graphics_service = SalesGraphicsService(numpy_service)
    graphics_controller = SalesGraphicsController(graphics_service)
    graphics_controller.generate_all()

    print("\n[4/5] Preparando datos para Machine Learning...")
    ml_service = SalesMLPreparationService(collection)
    ml_controller = SalesMLController(ml_service)
    ml_dto = ml_controller.prepare_and_save('ventas_preparadas_ml.csv')

    print("\n[5/5] Resumen del pipeline:")
    print(f"     Transacciones procesadas: {collection.count()}")
    print(f"     Total ventas: ${stats_service.get_total_sales():,.2f}")
    print(f"     Features ML: {len(ml_dto.feature_names)}")
    print(f"     Samples ML: {len(ml_dto.X)}")
    print(f"     Informe: informe_ventas.md")
    print(f"     Dataset ML: ventas_preparadas_ml.csv")
    print(f"     Gráficos: charts/")

    print_separator("PIPELINE COMPLETADO EXITOSAMENTE")


if __name__ == "__main__":
    main()