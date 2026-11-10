"""Paso 1: comparar tres modelos de clasificación y guardar el mejor."""

import pandas as pd

from controllers.ClassificationController import ClassificationController
from helpers.output_helpers import print_dataframe, print_separator
from helpers.project_paths import CLASSIFICATION_MODEL_PATH, CONFUSION_MATRIX_PATH
from outputs.visualization.ClassificationChartRenderer import (
    ClassificationChartRenderer,
)
from pipelines.classification.ClassificationRunner import ClassificationRunner
from pipelines.transform.CropDataPreparationRunner import CropDataPreparationRunner
from services.ModelPersistenceService import ModelPersistenceService


def main() -> None:
    """Ejecuta la preparación, la comparación y el guardado del modelo."""
    print_separator("CLASE 12 - COMPARACIÓN DE MODELOS DE CLASIFICACIÓN")

    print("\n[1/3] Preparando los datos de cultivos...")
    preparedData = CropDataPreparationRunner().run()

    if preparedData.X_train is None or preparedData.X_test is None:
        raise RuntimeError("La preparación no generó los conjuntos de datos.")
    print(
        f"Lotes para entrenar: {len(preparedData.X_train)} | "
        f"Lotes para probar: {len(preparedData.X_test)}"
    )

    print("\n[2/3] Entrenando y comparando los tres modelos...")
    controller = ClassificationController(
        runner=ClassificationRunner(modelPath=CLASSIFICATION_MODEL_PATH),
        storage=ModelPersistenceService(CLASSIFICATION_MODEL_PATH),
    )
    context = controller.train(preparedData)

    report = context.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte de clasificación.")

    table = pd.DataFrame(
        [
            {
                "Modelo": score.modelName,
                "Exactitud": score.accuracy,
                "Precisión": score.precision,
                "Recall": score.recall,
                "F1": score.f1,
                "Val. cruzada": score.crossValidation,
            }
            for score in report.scores
        ]
    )
    print_dataframe("Comparación de modelos (datos de prueba):", table)

    print(f"\nMejor modelo según F1: {report.bestModelName}")
    if report.weights:
        print(
            f"Pesos aprendidos: w1 = {report.weights[0]:.2f}, "
            f"w2 = {report.weights[1]:.2f}, b = {report.bias:.2f}"
        )

    print("\nMatriz de confusión (filas = valor real, columnas = predicción):")
    for row in report.confusionMatrix:
        print(f"  {list(row)}")

    print("\n[3/3] Generando la matriz de confusión...")
    chartPath = ClassificationChartRenderer().generateConfusionMatrix(
        report.confusionMatrix,
        report.bestModelName,
        CONFUSION_MATRIX_PATH,
    )
    print(f"Gráfico guardado: {chartPath}")
    print(f"Modelo guardado: {report.modelPath or CLASSIFICATION_MODEL_PATH}")

    print_separator("PROCESO COMPLETADO EXITOSAMENTE")


if __name__ == "__main__":
    main()
