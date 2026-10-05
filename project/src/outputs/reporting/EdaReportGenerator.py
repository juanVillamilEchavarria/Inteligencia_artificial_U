from datetime import datetime

from pipelines.transform.dtos.EdaReport import EdaReport
from pipelines.transform.dtos.CleaningReport import CleaningReport


class EdaReportGenerator:
    def generate(self, edaReport: EdaReport, cleaningReport: CleaningReport = None,
                 outputPath: str = 'eda_summary.md') -> str:
        if edaReport is None:
            raise ValueError("No hay reporte de EDA para generar el resumen.")

        o = edaReport.outlierAnalysis
        v = edaReport.incomeVsExpense

        topCategories = dict(list(edaReport.categoriaDist.items())[:5])
        topAccounts = dict(list(edaReport.cuentaDist.items())[:5])

        cleaningSection = self._buildCleaningSection(cleaningReport)

        markdown = f"""# Resumen EDA - Leo Counter (Pandas + Seaborn)

## Dimensiones
- Filas: {edaReport.shape[0]}
- Columnas: {edaReport.shape[1]}

## Valores Nulos
- Total nulos: {edaReport.totalNulls}
- Columnas con nulos: {self._formatNonZeroDict(edaReport.nullCounts)}

## Distribución Tipo Movimiento
{edaReport.tipoMovimientoDist}

## Top 5 Categorías
{topCategories}

## Top 5 Cuentas
{topAccounts}

## Análisis Monto
- Skewness: {edaReport.montoSkew:.4f}
- Kurtosis: {edaReport.montoKurtosis:.4f}
- Outliers IQR: {o.count} ({o.percentage:.1f}%)
- Rango IQR: [${o.lowerBound:,.2f} , ${o.upperBound:,.2f}]

## Ingresos vs Gastos
- Ingresos: {v.incomeCount} (Media: ${v.incomeMean:,.0f}, Mediana: ${v.incomeMedian:,.0f}, Máx: ${v.incomeMax:,.0f})
- Gastos: {v.expenseCount} (Media: ${v.expenseMean:,.0f}, Mediana: ${v.expenseMedian:,.0f}, Máx: ${v.expenseMax:,.0f})

{cleaningSection}
---
*Resumen generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} por Leo Counter AI - Módulo de Preparación de Datos.*
"""
        with open(outputPath, 'w', encoding='utf-8') as file:
            file.write(markdown)

        return outputPath

    def _formatNonZeroDict(self, d: dict) -> str:
        nonZero = {k: v for k, v in d.items() if v > 0}
        return str(nonZero) if nonZero else "{}"

    def _buildCleaningSection(self, report: CleaningReport) -> str:
        if report is None:
            return ""

        lines = [
            "## Limpieza de Datos",
            f"- Filas antes: {report.rowsBefore}",
            f"- Filas después: {report.rowsAfter}",
            f"- Columna 'fecha' convertida a datetime: {'Sí' if report.fechaConverted else 'No'}",
        ]
        if report.imputations:
            lines.append("\n### Imputaciones realizadas")
            lines.append("| Columna | Estrategia | Valor | Nulos imputados |")
            lines.append("|---------|-----------|-------|----------------:|")
            for imp in report.imputations:
                lines.append(f"| {imp.column} | {imp.strategy} | {imp.filledValue} | {imp.nullsCount} |")
        else:
            lines.append("\nNo se requirieron imputaciones (dataset sin nulos).")

        return "\n".join(lines) + "\n"
