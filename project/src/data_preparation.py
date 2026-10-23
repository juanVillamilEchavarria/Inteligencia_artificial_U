"""Ejecuta la preparación del dataset, los gráficos y el resumen EDA."""

from helpers.output_helpers import print_separator
from helpers.project_paths import EDA_SUMMARY_PATH, PREPARED_DATASET_PATH, SEABORN_CHARTS_DIR
from pipelines.transform.DataPreparationRunner import DataPreparationRunner
from outputs.visualization.SeabornChartRenderer import SeabornChartRenderer
from outputs.reporting.EdaReportGenerator import EdaReportGenerator


def main():
    """Ejecuta el pipeline completo de preparación y reporta lo generado."""
    print_separator("PREPARACIÓN DE DATOS - LEO COUNTER AI (PIPELINE)")

    print("\n[1/3] Ejecutando pipeline de preparación de datos...")
    runner = DataPreparationRunner(outputPath=str(PREPARED_DATASET_PATH))
    context = runner.run()

    print("\n[2/3] Generando visualizaciones Seaborn...")
    seabornRenderer = SeabornChartRenderer(
        context.dfPrepared,
        chartsDir=f"{SEABORN_CHARTS_DIR}/",
    )
    generatedFiles = seabornRenderer.generateAll()

    print("\n[3/3] Generando resumen EDA en Markdown...")
    edaReportGenerator = EdaReportGenerator()
    edaSummaryPath = edaReportGenerator.generate(
        context.edaReport,
        context.cleaningReport,
        str(EDA_SUMMARY_PATH),
        preparedShape=context.dfPrepared.shape,
    )

    print("\nResumen final:")
    print(f"     Dataset original: {context.dfRaw.shape[0]} filas x {context.dfRaw.shape[1]} columnas")
    print(f"     Dataset preparado: {context.dfPrepared.shape[0]} filas x {context.dfPrepared.shape[1]} columnas")
    print(f"     Duplicados eliminados: {context.cleaningReport.duplicatesRemoved}")
    print(f"     Outliers conservados: {context.cleaningReport.outliersKept}")
    print(f"     Columnas derivadas: {', '.join(context.metadata.get('derivedColumns', []))}")
    print(f"     Variables codificadas: {', '.join(context.metadata.get('encodedColumns', {}).keys())}")
    print(f"     Dataset guardado: {context.metadata.get('outputPath')}")
    print(f"     Resumen EDA guardado: {edaSummaryPath}")
    print(f"     Gráficos Seaborn generados ({len(generatedFiles)}):")
    for f in generatedFiles:
        print(f"       - {f}")

    print_separator("PREPARACIÓN COMPLETADA EXITOSAMENTE")


if __name__ == "__main__":
    main()
