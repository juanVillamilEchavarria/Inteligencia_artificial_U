"""Generación del resumen de calidad y EDA en formato Markdown."""

from datetime import datetime

from pipelines.transform.dtos.CleaningReport import CleaningReport
from pipelines.transform.dtos.EdaReport import EdaReport


class DataQualityReportGenerator:
    """Convierte los reportes de EDA y limpieza en un documento legible."""

    def generate(
        self,
        edaReport: EdaReport,
        cleaningReport: CleaningReport = None,
        outputPath: str = "eda_summary.md",
        preparedShape=None,
    ) -> str:
        """Escribe el resumen en Markdown y devuelve la ruta del archivo."""
        if edaReport is None:
            raise ValueError("No hay reporte de EDA para generar el resumen.")

        cleaningSection = self._buildCleaningSection(cleaningReport, preparedShape)
        correlations = "\n".join(
            f"- `{key}`: {value:.4f}" for key, value in edaReport.correlations.items()
        )
        numericSummary = "\n".join(
            f"| {column} | {values['mean']:.4f} | {values['std']:.4f} | "
            f"{values['min']:.4f} | {values['median']:.4f} | {values['max']:.4f} |"
            for column, values in edaReport.numericSummary.items()
        )

        markdown = f"""# Resumen EDA y limpieza - Grupo 07

## Dimensiones
- Filas: {edaReport.shape[0]}
- Columnas: {edaReport.shape[1]}

## Valores nulos y duplicados
- Total de nulos: {edaReport.totalNulls}
- Columnas con nulos: {self._formatNonZeroDict(edaReport.nullCounts)}
- Duplicados exactos: {edaReport.duplicatesExact}
- IDs duplicados: {edaReport.duplicatesById}

## Distribuciones
- Rutas únicas: {edaReport.uniqueRoutes}
- Distribución por ruta: {edaReport.routeDist}
- Distribución del objetivo: {edaReport.targetDist}

## Estadísticas numéricas
| Columna | Media | Desv. estándar | Mínimo | Mediana | Máximo |
|---|---:|---:|---:|---:|---:|
{numericSummary}

## Correlaciones
{correlations}

{cleaningSection}
---
*Resumen generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} por el módulo de preparación de datos del Grupo 07.*
"""
        with open(outputPath, "w", encoding="utf-8") as file:
            file.write(markdown)

        return outputPath

    def _formatNonZeroDict(self, values: dict) -> str:
        """Muestra solo las columnas que realmente tienen nulos."""
        nonZero = {key: value for key, value in values.items() if value > 0}
        return str(nonZero) if nonZero else "{}"

    def _buildCleaningSection(self, report: CleaningReport, preparedShape=None) -> str:
        """Construye la sección de limpieza con la tabla antes y después."""
        if report is None:
            return ""

        lines = [
            "## Tabla antes / después",
            "| Momento | Filas | Columnas | Nulos | Clase 0 | Clase 1 |",
            "|---------|------:|---------:|------:|--------:|--------:|",
            f"| Dataset original | {report.rowsBefore} | {report.columnsBefore} | "
            f"{report.nullsBefore} | {report.targetCountsBefore.get(0, 0)} | "
            f"{report.targetCountsBefore.get(1, 0)} |",
            f"| Después de limpieza | {report.rowsAfter} | {report.columnsAfter} | "
            f"{report.nullsAfter} | {report.targetCountsAfter.get(0, 0)} | "
            f"{report.targetCountsAfter.get(1, 0)} |",
        ]
        if preparedShape is not None:
            lines.append(
                f"| Después de preparación | {preparedShape[0]} | {preparedShape[1]} | 0 | - | - |"
            )

        lines.extend(
            [
                "",
                "## Limpieza de datos",
                f"- Duplicados eliminados: {report.duplicatesRemoved}",
                f"- IDs duplicados detectados: {', '.join(report.duplicateIds) or 'Ninguno'}",
                f"- Filas inválidas eliminadas: {report.invalidRowsRemoved}",
                f"- Columnas de texto normalizadas: "
                f"{', '.join(report.normalizedColumns) if report.normalizedColumns else 'Ninguna'}",
            ]
        )

        if report.corrections:
            lines.append("\n### Correcciones")
            lines.append("| ID | Columna | Valor original | Valor corregido | Motivo |")
            lines.append("|----|---------|---------------:|----------------:|--------|")
            for correction in report.corrections:
                lines.append(
                    f"| {correction.recorridoId} | {correction.column} | "
                    f"{correction.originalValue} | {correction.correctedValue} | "
                    f"{correction.reason} |"
                )

        if report.imputations:
            lines.append("\n### Imputaciones")
            lines.append("| Columna | Estrategia | Valor | Nulos imputados |")
            lines.append("|---------|-----------|-------|----------------:|")
            for imputation in report.imputations:
                lines.append(
                    f"| {imputation.column} | {imputation.strategy} | "
                    f"{imputation.filledValue:.4f} | {imputation.nullsCount} |"
                )

        lines.append("\n### Valor sospechoso")
        lines.append(
            f"- {report.suspiciousColumn} = {report.suspiciousValue:.4f}. "
            f"Media antes: {report.meanBefore:.4f}; media después: {report.meanAfter:.4f}. "
            f"Desviación antes: {report.stdBefore:.4f}; después: {report.stdAfter:.4f}."
        )
        return "\n".join(lines) + "\n"
