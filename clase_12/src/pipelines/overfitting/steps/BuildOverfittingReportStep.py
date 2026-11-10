"""Paso que construye el reporte de sobreajuste."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.overfitting.dtos.OverfittingReport import OverfittingReport
from pipelines.overfitting.OverfittingContext import OverfittingContext


class BuildOverfittingReportStep(PipelineStep[OverfittingContext]):
    """Empaqueta los resultados de profundidad en un DTO."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Construcción del reporte de sobreajuste"

    def execute(self, context: OverfittingContext) -> OverfittingContext:
        """Crea el reporte final."""
        if not context.scores:
            raise ValueError("BuildOverfittingReportStep requiere scores.")

        report = OverfittingReport(scores=context.scores)
        return replace(context, report=report)
