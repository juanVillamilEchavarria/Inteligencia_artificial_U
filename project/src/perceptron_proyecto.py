"""Entrena el perceptrón, genera sus gráficos y clasifica casos nuevos."""

import numpy as np

from controllers.PerceptronController import PerceptronController
from helpers.output_helpers import print_separator
from helpers.project_paths import PERCEPTRON_CHARTS_DIR, PREPARED_DATASET_PATH
from outputs.visualization.PerceptronChartRenderer import PerceptronChartRenderer
from pipelines.train.PerceptronTrainingRunner import PerceptronTrainingRunner


def main():
    """Ejecuta el entrenamiento, muestra métricas y predice casos de ejemplo."""
    print_separator("PERCEPTRÓN DESDE CERO - LEO COUNTER AI")

    runner = PerceptronTrainingRunner(
        dataPath=str(PREPARED_DATASET_PATH),
        targetName="es_ingreso",
        featureNames=("monto_log", "mes"),
        learningRate=0.1,
        epochs=500,
    )

    print("\n[1/3] Ejecutando pipeline de entrenamiento...")
    context = runner.run()

    report = context.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte del perceptrón.")

    print("\n[2/3] Generando gráficos del perceptrón...")
    renderer = PerceptronChartRenderer(
        context.dfPrepared,
        report,
        context.means,
        context.stds,
        chartsDir=f"{PERCEPTRON_CHARTS_DIR}/",
    )
    generatedFiles = renderer.generateAll()

    print("\n[3/3] Prediciendo casos nuevos...")
    controller = PerceptronController(runner)
    newCases = [
        (8000.0, 6),
        (3500000.0, 4),
        (250000.0, 5),
    ]
    predictions = controller.predictNewCases(context, newCases)

    print("\nResultados del modelo:")
    print(f"     Filas de entrenamiento : {report.positiveCount + report.negativeCount}")
    print(f"     Clase 0 (Gasto)        : {report.negativeCount}")
    print(f"     Clase 1 (Ingreso)      : {report.positiveCount}")
    print(f"     Variables de entrada   : {', '.join(report.featureNames)}")
    print(f"     Media de entradas      : {np.round(context.means, 4).tolist()}")
    print(f"     Desviación de entradas : {np.round(context.stds, 4).tolist()}")
    print(f"     Pesos finales          : w1={report.weights[0]:.4f}, w2={report.weights[1]:.4f}")
    print(f"     Sesgo (b)              : {report.bias:.4f}")
    print(f"     Pérdida inicial        : {report.initialLoss:.4f}")
    print(f"     Pérdida final          : {report.finalLoss:.4f}")
    print(f"     Exactitud inicial      : {report.initialAccuracy:.2%}")
    print(f"     Exactitud final        : {report.finalAccuracy:.2%}")
    print(f"     Exactitud de mayoría   : {report.baselineAccuracy:.2%}")

    print("\nPredicciones de casos nuevos:")
    for prediction in predictions:
        label = "Ingreso" if prediction.label == 1 else "Gasto"
        print(
            f"     Monto ${prediction.monto:>12,.0f} | Mes {prediction.mes:>2} | "
            f"Probabilidad {prediction.probability:.2%} -> {label}"
        )

    print(f"\nGráficos generados ({len(generatedFiles)}):")
    for generatedFile in generatedFiles:
        print(f"     - {generatedFile}")

    print_separator("ENTRENAMIENTO COMPLETADO EXITOSAMENTE")


if __name__ == "__main__":
    main()
