"""Paso 3: predecir un número con regresión lineal."""

from controllers.RegressionController import RegressionController
from helpers.output_helpers import print_separator
from helpers.project_paths import REGRESSION_PLOT_PATH
from outputs.visualization.RegressionChartRenderer import RegressionChartRenderer
from pipelines.regression.RegressionRunner import RegressionRunner
from pipelines.transform.RegressionDataPreparationRunner import (
    RegressionDataPreparationRunner,
)


def main() -> None:
    """Genera los datos, entrena la regresión y muestra sus métricas."""
    print_separator("CLASE 12 - REGRESIÓN: RENDIMIENTO DE CULTIVOS")

    print("\n[1/3] Generando y preparando los datos de rendimiento...")
    preparedData = RegressionDataPreparationRunner().run()

    if preparedData.dfRaw is not None:
        print("\nPrimeros datos:")
        print(preparedData.dfRaw.head().to_string(index=False))
    if preparedData.y is not None:
        print(
            f"\nRendimiento promedio: "
            f"{preparedData.y.mean():.0f} kg/ha"
        )

    print("\n[2/3] Entrenando la regresión lineal...")
    context = RegressionController(RegressionRunner()).train(preparedData)
    report = context.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte de regresión.")

    print("\nMétricas con los datos de prueba:")
    print(f"MAE  = {report.mae:.1f} kg/ha")
    print(f"RMSE = {report.rmse:.1f} kg/ha")
    print(f"R²   = {report.r2:.3f}")

    print("\nEfecto de cada variable (al subir una desviación estándar):")
    for name, coefficient in zip(report.featureNames, report.coefficients):
        print(f"  {name}: {coefficient:+.1f} kg/ha")

    print("\n[3/3] Generando el gráfico real vs. predicho...")
    if preparedData.y_test is None or context.yPredicted is None:
        raise RuntimeError("Faltan datos para generar el gráfico de regresión.")

    chartPath = RegressionChartRenderer().generateRealVsPredicted(
        preparedData.y_test,
        context.yPredicted,
        report.r2,
        REGRESSION_PLOT_PATH,
    )
    print(f"Gráfico guardado: {chartPath}")
    print(
        "Dataset guardado: "
        f"{preparedData.metadata.get('outputPath', 'data/rendimiento_cartago.csv')}"
    )

    print_separator("REGRESIÓN COMPLETADA EXITOSAMENTE")


if __name__ == "__main__":
    main()
