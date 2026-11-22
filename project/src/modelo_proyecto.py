"""Entrena y compara los modelos de Scikit-Learn, y guarda el mejor."""

import pandas as pd

from controllers.ModelController import ModelController
from helpers.output_helpers import print_separator
from helpers.project_paths import MODEL_METRICS_PATH, MODEL_PATH, PREPARED_DATASET_PATH
from outputs.visualization.EvaluationChartRenderer import EvaluationChartRenderer
from pipelines.model.ModelTrainingRunner import ModelTrainingRunner
from services.SklearnModelService import SklearnModelService


def main():
    """Ejecuta la comparación, muestra las métricas y genera los gráficos."""
    print_separator("MODELOS DE SCIKIT-LEARN - LEO COUNTER AI")

    runner = ModelTrainingRunner(
        dataPath=str(PREPARED_DATASET_PATH),
        targetName="es_ingreso",
        featureNames=("monto_log", "mes", "dia_semana", "es_fin_semana"),
        testSize=0.25,
        randomState=42,
        cvFolds=5,
        modelPath=MODEL_PATH,
        metricsPath=MODEL_METRICS_PATH,
    )

    print("\n[1/3] Ejecutando pipeline de comparación de modelos...")
    context = runner.run()

    report = context.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte de modelos.")

    table = pd.DataFrame(
        [
            {
                "Modelo": score.modelName,
                "Exactitud": round(score.accuracy, 4),
                "Precisión": round(score.precision, 4),
                "Recall": round(score.recall, 4),
                "F1 macro": round(score.f1Macro, 4),
                "F1 Ingreso": round(score.f1Class1, 4),
                "ROC-AUC": round(score.rocAuc, 4),
                "CV F1 macro": round(score.crossValidationMean, 4),
                "CV desv.": round(score.crossValidationStd, 4),
            }
            for score in report.scores
        ]
    )

    print("\n[2/3] Comparación de modelos (conjunto de prueba):")
    print(table.to_string(index=False))

    print(f"\nMejor modelo (F1 macro de validación cruzada): {report.bestModelName}")
    print(f"Filas de entrenamiento: {report.trainCount}")
    print(f"Filas de prueba: {report.testCount}")
    print(f"Variables de entrada: {', '.join(report.featureNames)}")
    if report.bestParams:
        print(f"Mejores hiperparámetros: {report.bestParams}")

    print("\nMatriz de confusión (filas = real, columnas = predicción):")
    for row in report.bestConfusionMatrix:
        print(f"  {list(row)}")

    if context.bestModel is not None:
        weights = SklearnModelService.describeModel(context.bestModel, report.featureNames)
        if weights:
            print("\nPeso de cada variable en el mejor modelo:")
            for name, value in sorted(weights.items(), key=lambda item: abs(item[1]), reverse=True):
                print(f"  {name:>14}: {value:+.4f}")

    print("\n[3/3] Generando gráficos de evaluación...")
    renderer = EvaluationChartRenderer(context)
    generatedFiles = renderer.generateAll()

    print(f"\nModelo guardado: {report.modelPath}")
    print(f"Métricas guardadas: {report.metricsPath}")
    print(f"Gráficos generados ({len(generatedFiles)}):")
    for generatedFile in generatedFiles:
        print(f"  - {generatedFile}")

    print_separator("COMPARACIÓN DE MODELOS COMPLETADA EXITOSAMENTE")


if __name__ == "__main__":
    main()
