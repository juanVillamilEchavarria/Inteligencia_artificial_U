"""Paso 5: observar el sobreajuste en árboles de decisión."""

import pandas as pd

from controllers.OverfittingController import OverfittingController
from helpers.output_helpers import print_dataframe, print_separator
from helpers.project_paths import OVERFITTING_PLOT_PATH
from outputs.visualization.OverfittingChartRenderer import OverfittingChartRenderer
from pipelines.overfitting.OverfittingRunner import OverfittingRunner
from pipelines.transform.CropDataPreparationRunner import CropDataPreparationRunner


def main() -> None:
    """Entrena árboles de distinta profundidad y compara exactitudes."""
    print_separator("CLASE 12 - SOBREAJUSTE EN ÁRBOLES DE DECISIÓN")

    print("\n[1/2] Preparando los datos de cultivos...")
    preparedData = CropDataPreparationRunner().run()

    print("\n[2/2] Entrenando árboles de profundidad 1 a 12...")
    context = OverfittingController(OverfittingRunner()).train(preparedData)
    report = context.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte de sobreajuste.")

    table = pd.DataFrame(
        [
            {
                "Profundidad": score.depth,
                "Entrenamiento": score.trainAccuracy,
                "Prueba": score.testAccuracy,
            }
            for score in report.scores
        ]
    )
    print_dataframe("Exactitud por profundidad:", table)

    chartPath = OverfittingChartRenderer().generateOverfittingPlot(
        report,
        OVERFITTING_PLOT_PATH,
    )
    print(f"\nGráfico guardado: {chartPath}")
    print_separator("ESTUDIO COMPLETADO")


if __name__ == "__main__":
    main()
