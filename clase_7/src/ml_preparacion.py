from helpers.output_helpers import print_separator


def main():
    from api.SalesDataGateway import SalesDataGateway
    from services.SalesMLPreparationService import SalesMLPreparationService
    from controllers.SalesMLController import SalesMLController

    print_separator("PREPARACIÓN DE DATOS PARA MACHINE LEARNING - VENTAS")

    gateway = SalesDataGateway('ventas_tienda.csv')
    collection = gateway.get_data()

    ml_service = SalesMLPreparationService(collection)
    ml_controller = SalesMLController(ml_service)

    ml_dto = ml_controller.prepare_and_save('ventas_preparadas_ml.csv')

    print_separator("DATAFRAME LISTO PARA MACHINE LEARNING (primeras 5 filas)")
    import pandas as pd
    df_ml = pd.DataFrame(ml_dto.X, columns=ml_dto.feature_names)
    df_ml['total_venta'] = ml_dto.y
    print(df_ml.head())

    print_separator("PREPARACIÓN ML COMPLETADA")
    print(f"  Features: {len(ml_dto.feature_names)}")
    print(f"  Samples: {len(ml_dto.X)}")
    print()


if __name__ == "__main__":
    main()