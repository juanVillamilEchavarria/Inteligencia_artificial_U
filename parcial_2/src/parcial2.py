"""Entry point del Parcial 2 - Grupo 07: rutas de recolección de residuos."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np

from controllers.PerceptronController import PerceptronController
from controllers.RecorridoGraphicsController import RecorridoGraphicsController
from helpers.output_helpers import print_separator
from helpers.project_paths import (
    CLEAN_DATASET_PATH,
    EDA_SUMMARY_PATH,
    PERCEPTRON_CHARTS_DIR,
    SEABORN_CHARTS_DIR,
)
from outputs.reporting.DataQualityReportGenerator import DataQualityReportGenerator
from outputs.visualization.PerceptronChartRenderer import PerceptronChartRenderer
from outputs.visualization.SeabornChartRenderer import SeabornChartRenderer
from pipelines.transform.DataPreparationRunner import DataPreparationRunner
from pipelines.train.PerceptronTrainingRunner import PerceptronTrainingRunner


def print_inspection(context) -> None:
    """Muestra las salidas solicitadas para la carga e inspección."""
    report = context.edaReport
    dfRaw = context.dfRaw

    print_separator("TAREA 2 - CARGA E INSPECCIÓN")
    print("\nPrimeras 5 filas:")
    print(dfRaw.head().to_string(index=False))

    print(f"\nForma del DataFrame (shape): {report.shape}")
    print(f"Filas: {report.shape[0]} | Columnas: {report.shape[1]}")

    print("\nTipos de datos:")
    for column, dtype in report.dtypes.items():
        print(f"  {column:<22} {dtype}")

    print("\nCantidad de nulos por columna:")
    for column, count in report.nullCounts.items():
        print(f"  {column:<22} {count}")

    print(f"\nFilas duplicadas exactas: {report.duplicatesExact}")
    print(f"IDs de recorrido duplicados: {report.duplicatesById}")
    print(f"Rutas únicas: {report.uniqueRoutes}")
    print(f"Distribución por ruta: {report.routeDist}")
    print(f"Distribución de la clase objetivo: {report.targetDist}")

    print("\nRespuesta a la pregunta clave:")
    print("  Ninguna columna numérica aparece con un tipo que no debería tener.")
    print("  'toneladas_recogidas' y 'distancia_km' son float64 porque contienen")
    print("  decimales y, en el caso de la distancia, valores nulos. La columna")
    print("  'ruta_retrasada' es int64 porque solo contiene 0 y 1. El problema de")
    print("  R031 (3700.0) no es de tipo, sino de escala/unidades.")


def print_cleaning(context) -> None:
    """Muestra el reporte de calidad y limpieza de datos."""
    report = context.cleaningReport

    print_separator("TAREA 3 - CALIDAD Y LIMPIEZA")
    print(f"Filas antes de limpiar: {report.rowsBefore}")
    print(f"Filas después de limpiar: {report.rowsAfter}")
    print(f"Columnas antes/después: {report.columnsBefore} / {report.columnsAfter}")
    print(f"Nulos antes/después: {report.nullsBefore} / {report.nullsAfter}")
    print(f"Duplicados exactos eliminados: {report.duplicatesRemoved}")
    print(f"IDs duplicados detectados: {', '.join(report.duplicateIds)}")
    print(f"Filas inválidas restantes eliminadas: {report.invalidRowsRemoved}")

    print("\nProblemas corregidos:")
    for correction in report.corrections:
        print(
            f"  - {correction.recorridoId}: {correction.column} "
            f"{correction.originalValue} -> {correction.correctedValue}. "
            f"{correction.reason}"
        )
    for imputation in report.imputations:
        print(
            f"  - {imputation.column}: {imputation.nullsCount} nulos imputados "
            f"con {imputation.strategy} = {imputation.filledValue:.4f}."
        )

    print("\nDistribución de clases antes:", report.targetCountsBefore)
    print("Distribución de clases después:", report.targetCountsAfter)

    print("\nPregunta clave: valor más sospechoso")
    print(
        f"  {report.suspiciousColumn} = {report.suspiciousValue:.4f}. "
        "Corresponde a R031 y parece un valor en kilogramos exportado como toneladas."
    )
    print(
        f"  Media antes de corregir: {report.meanBefore:.4f} | "
        f"Media después: {report.meanAfter:.4f}"
    )
    print(
        f"  Desviación antes: {report.stdBefore:.4f} | "
        f"Desviación después: {report.stdAfter:.4f}"
    )
    print(
        "  Si no se corrigiera, la estandarización (x - 52.276) / 402.813 dejaría"
    )
    print(
        "  casi todos los valores reales entre -0.11 y -0.09, es decir, casi"
    )
    print(
        "  indistinguibles. El perceptrón recibiría entradas casi constantes, el"
    )
    print(
        "  gradiente sería mínimo y el modelo no aprendería a separar los retrasos."
    )
    print(f"\nDataset limpio guardado en: {context.metadata.get('outputPath')}")


def print_training(report, context) -> None:
    """Muestra pesos, pérdidas y exactitud del perceptrón."""
    print_separator("TAREA 5 - PERCEPTRÓN DESDE CERO CON NUMPY")
    print(f"Filas de entrenamiento: {report.positiveCount + report.negativeCount}")
    print(f"Clase 0 (a tiempo): {report.negativeCount}")
    print(f"Clase 1 (retraso): {report.positiveCount}")
    print(f"Variables de entrada: {', '.join(report.featureNames)}")
    print(f"Media de entradas: {np.round(context.means, 4).tolist()}")
    print(f"Desviación de entradas: {np.round(context.stds, 4).tolist()}")
    print("Pesos iniciales: w1=0.0000, w2=0.0000, b=0.0000")
    print(
        f"Pesos finales: w1={report.weights[0]:.4f}, "
        f"w2={report.weights[1]:.4f}, b={report.bias:.4f}"
    )
    print(f"Pérdida inicial: {report.initialLoss:.4f}")
    print(f"Pérdida final: {report.finalLoss:.4f}")
    print(f"Exactitud inicial: {report.initialAccuracy:.2%}")
    print(f"Exactitud final: {report.finalAccuracy:.2%}")
    print(f"Exactitud de la clase mayoritaria: {report.baselineAccuracy:.2%}")
    print(f"Registros mal clasificados: {report.misclassifiedCount}")


def print_interpretation(context, report) -> None:
    """Imprime los datos de soporte para la interpretación de la Tarea 6."""
    df = context.dfClean
    threshold = 30.0
    highDistance = df.loc[df["distancia_km"] >= threshold, "ruta_retrasada"]
    lowDistance = df.loc[df["distancia_km"] < threshold, "ruta_retrasada"]
    correlation = df["distancia_km"].corr(df["ruta_retrasada"])

    signW1 = "positivo" if report.weights[0] > 0 else "negativo"
    signW2 = "positivo" if report.weights[1] > 0 else "negativo"

    print_separator("TAREA 6 - INTERPRETACIÓN")
    print(f"Signo de w1 (toneladas): {signW1} ({report.weights[0]:.4f})")
    print(f"Signo de w2 (distancia): {signW2} ({report.weights[1]:.4f})")
    print(f"Correlación distancia vs retraso: {correlation:.4f}")
    print(
        f"Tasa de retraso con distancia >= {threshold:.0f} km: "
        f"{highDistance.mean():.2%} ({int(highDistance.sum())}/{len(highDistance)})"
    )
    print(
        f"Tasa de retraso con distancia < {threshold:.0f} km: "
        f"{lowDistance.mean():.2%} ({int(lowDistance.sum())}/{len(lowDistance)})"
    )
    print(f"Tasa global de retraso: {df['ruta_retrasada'].mean():.2%}")


def main():
    """Ejecuta preparación, visualización, perceptrón e interpretación."""
    print_separator("PARCIAL 2 - GRUPO 07 - RESIDUOS CARTAGO")

    print("\n[1/5] Ejecutando pipeline de preparación de datos...")
    preparationRunner = DataPreparationRunner(outputPath=str(CLEAN_DATASET_PATH))
    context = preparationRunner.run()
    print_inspection(context)
    print_cleaning(context)

    print("\n[2/5] Generando visualizaciones Seaborn...")
    seabornRenderer = SeabornChartRenderer(
        context.dfClean,
        chartsDir=f"{SEABORN_CHARTS_DIR}/",
    )
    graphicsController = RecorridoGraphicsController(seabornRenderer)
    seabornFiles = graphicsController.generateAll()

    print("\n[3/5] Generando resumen EDA en Markdown...")
    edaSummaryPath = DataQualityReportGenerator().generate(
        context.edaReport,
        context.cleaningReport,
        str(EDA_SUMMARY_PATH),
        preparedShape=context.dfPrepared.shape,
    )

    print("\n[4/5] Entrenando el perceptrón desde cero...")
    trainingRunner = PerceptronTrainingRunner(
        dataPath=str(CLEAN_DATASET_PATH),
        targetName="ruta_retrasada",
        featureNames=("toneladas_recogidas", "distancia_km"),
        learningRate=0.1,
        epochs=500,
    )
    trainContext = trainingRunner.run()
    report = trainContext.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte del perceptrón.")
    print_training(report, trainContext)

    print("\nGenerando gráficos del perceptrón...")
    perceptronRenderer = PerceptronChartRenderer(
        trainContext.dfPrepared,
        report,
        trainContext.means,
        trainContext.stds,
        chartsDir=f"{PERCEPTRON_CHARTS_DIR}/",
    )
    perceptronFiles = perceptronRenderer.generateAll()

    print("\n[5/5] Prediciendo dos recorridos nuevos...")
    controller = PerceptronController(trainingRunner)
    newCases = [
        (5.0, 7.0),
        (13.0, 38.0),
    ]
    predictions = controller.predictNewCases(trainContext, newCases)
    for prediction in predictions:
        label = "Retraso (1)" if prediction.label == 1 else "A tiempo (0)"
        print(
            f"  Toneladas {prediction.toneladas:>4.1f} | "
            f"Distancia {prediction.distancia:>5.1f} km | "
            f"Probabilidad de retraso {prediction.probability:.2%} -> {label}"
        )

    print_interpretation(context, report)

    print_separator("RESUMEN FINAL")
    print(f"Dataset original: {context.dfRaw.shape[0]} filas x {context.dfRaw.shape[1]} columnas")
    print(
        f"Dataset limpio: {context.dfPrepared.shape[0]} filas x "
        f"{context.dfPrepared.shape[1]} columnas"
    )
    print(f"Duplicados eliminados: {context.cleaningReport.duplicatesRemoved}")
    print(f"Nulos imputados: {context.cleaningReport.nullsBefore}")
    print(f"Dataset limpio guardado: {context.metadata.get('outputPath')}")
    print(f"Resumen EDA guardado: {edaSummaryPath}")
    print("Gráficos Seaborn generados:")
    for file in seabornFiles:
        print(f"  - {file}")
    print("Gráficos del perceptrón generados:")
    for file in perceptronFiles:
        print(f"  - {file}")
    print_separator("PROCESO COMPLETADO EXITOSAMENTE")


if __name__ == "__main__":
    main()
