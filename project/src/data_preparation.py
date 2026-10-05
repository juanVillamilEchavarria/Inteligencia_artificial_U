from helpers.output_helpers import print_separator
from controllers.MovementDataPreparationController import MovementDataPreparationController
from services.MovementSeabornGraphicsService import MovementSeabornGraphicsService
from services.MovementDataPreparationService import MovementDataPreparationService
from services.ReportGenerator import ReportGenerator


def main():
    print_separator("PREPARACIÓN DE DATOS - LEO COUNTER AI (PANDAS + SEABORN)")

    print("\n[1/3] Ejecutando pipeline de preparación de datos...")
    prep_service = MovementDataPreparationService()
    prep_controller = MovementDataPreparationController(prep_service)

    df_prepared = prep_controller.prepare_data()
    prep_controller.save_prepared_data('data_prepared.csv')

    eda_findings = prep_controller.get_eda_findings()
    
    print("\n[2/3] Generando visualizaciones Seaborn...")
    seaborn_service = MovementSeabornGraphicsService(prep_service)
    generated_files = seaborn_service.generate_all()

    print("\n[3/3] Generando resumen EDA en Markdown...")
    report_generator = ReportGenerator.__new__(ReportGenerator)
    eda_summary_path = report_generator.generate_eda_summary(eda_findings, 'eda_summary.md')

    print("\nResumen final:")
    print(f"     Dataset original: {prep_service.df_raw.shape[0]} filas x {prep_service.df_raw.shape[1]} columnas")
    print(f"     Dataset preparado: {df_prepared.shape[0]} filas x {df_prepared.shape[1]} columnas")
    print(f"     Columnas derivadas: monto_log, es_ingreso, mes, dia_semana, es_fin_semana")
    print(f"     Variables codificadas: categoria, tipo_movimiento, cuenta (pd.get_dummies)")
    print(f"     Dataset guardado: data_prepared.csv")
    print(f"     Resumen EDA guardado: {eda_summary_path}")
    print(f"     Gráficos Seaborn generados ({len(generated_files)}):")
    for f in generated_files:
        print(f"       - {f}")

    print_separator("PREPARACIÓN COMPLETADA EXITOSAMENTE")


if __name__ == "__main__":
    main()