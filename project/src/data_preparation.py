from helpers.output_helpers import print_separator
from pipelines.transform.DataPreparationRunner import DataPreparationRunner
from outputs.visualization.SeabornChartRenderer import SeabornChartRenderer
from outputs.reporting.EdaReportGenerator import EdaReportGenerator


def main():
    print_separator("PREPARACIÓN DE DATOS - LEO COUNTER AI (PIPELINE)")

    print("\n[1/3] Ejecutando pipeline de preparación de datos...")
    runner = DataPreparationRunner(outputPath='data_prepared.csv')
    context = runner.run()

    print("\n[2/3] Generando visualizaciones Seaborn...")
    seabornRenderer = SeabornChartRenderer(context.dfPrepared)
    generatedFiles = seabornRenderer.generateAll()

    print("\n[3/3] Generando resumen EDA en Markdown...")
    edaReportGenerator = EdaReportGenerator()
    edaSummaryPath = edaReportGenerator.generate(
        context.edaReport,
        context.cleaningReport,
        'eda_summary.md'
    )

    print("\nResumen final:")
    print(f"     Dataset original: {context.dfRaw.shape[0]} filas x {context.dfRaw.shape[1]} columnas")
    print(f"     Dataset preparado: {context.dfPrepared.shape[0]} filas x {context.dfPrepared.shape[1]} columnas")
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
