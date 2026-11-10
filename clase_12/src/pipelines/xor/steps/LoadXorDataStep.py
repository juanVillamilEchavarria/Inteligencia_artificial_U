"""Paso que carga las cuatro filas de la compuerta XOR."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.xor.XorContext import XorContext
from services.XorService import XorService


class LoadXorDataStep(PipelineStep[XorContext]):
    """Deja X e y de XOR disponibles en el contexto."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Carga de datos XOR"

    def execute(self, context: XorContext) -> XorContext:
        """Carga las combinaciones y salidas esperadas."""
        X, y = XorService.get_xor_data()
        return replace(context, X=X, y=y)
