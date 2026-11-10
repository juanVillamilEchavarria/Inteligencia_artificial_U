"""Paso que entrena una sola neurona."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.xor.XorContext import XorContext
from services.XorService import XorService


class TrainSingleNeuronStep(PipelineStep[XorContext]):
    """Entrena la regresión logística que representa una neurona."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento de una neurona"

    def execute(self, context: XorContext) -> XorContext:
        """Ajusta el modelo de una sola neurona."""
        if context.X is None or context.y is None:
            raise ValueError("TrainSingleNeuronStep requiere X e y.")
        model = XorService.train_single_neuron(context.X, context.y)
        return replace(context, singleNeuron=model)
