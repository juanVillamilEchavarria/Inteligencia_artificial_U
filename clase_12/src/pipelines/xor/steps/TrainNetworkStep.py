"""Paso que entrena la red neuronal para XOR."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.xor.XorContext import XorContext
from services.XorService import XorService


class TrainNetworkStep(PipelineStep[XorContext]):
    """Entrena el perceptrón multicapa con una capa oculta."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento de la red neuronal"

    def execute(self, context: XorContext) -> XorContext:
        """Ajusta la red neuronal y la guarda en el contexto."""
        if context.X is None or context.y is None:
            raise ValueError("TrainNetworkStep requiere X e y.")
        model = XorService.train_network(context.X, context.y)
        return replace(context, network=model)
