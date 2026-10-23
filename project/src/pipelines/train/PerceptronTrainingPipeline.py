"""Pipeline que ejecuta en orden los pasos de entrenamiento del perceptrón."""

from typing import List

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep


class PerceptronTrainingPipeline:
    """Encadena pasos sobre un contexto inmutable."""

    def __init__(self, steps: List[TrainingStep]):
        """Recibe los pasos en el orden en que deben ejecutarse."""
        self._steps = steps

    def run(self) -> PerceptronTrainingContext:
        """Ejecuta todos los pasos y devuelve el contexto final."""
        context = PerceptronTrainingContext()
        for step in self._steps:
            print(f"  → {step.name}")
            context = step.execute(context)
        return context
