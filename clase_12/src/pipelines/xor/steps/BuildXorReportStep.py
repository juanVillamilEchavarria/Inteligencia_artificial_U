"""Paso que construye el reporte de XOR."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.xor.XorContext import XorContext
from services.XorService import XorService


class BuildXorReportStep(PipelineStep[XorContext]):
    """Compara las predicciones y exactitudes de los dos modelos."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Construcción del reporte XOR"

    def execute(self, context: XorContext) -> XorContext:
        """Crea el DTO con la tabla y las exactitudes."""
        if (
            context.X is None
            or context.y is None
            or context.singleNeuron is None
            or context.network is None
        ):
            raise ValueError("BuildXorReportStep requiere datos y ambos modelos.")

        report = XorService.build_report(
            context.X,
            context.y,
            context.singleNeuron,
            context.network,
        )
        return replace(context, report=report)
