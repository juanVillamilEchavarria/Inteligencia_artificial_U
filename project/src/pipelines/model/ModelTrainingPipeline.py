"""Pipeline que ejecuta en orden los pasos de comparación de modelos."""

from typing import List

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep


class ModelTrainingPipeline:
    """Encadena pasos sobre un contexto inmutable."""

    def __init__(self, steps: List[ModelTrainingStep]):
        """Recibe los pasos en el orden en que deben ejecutarse."""
        self._steps = steps

    def run(self) -> ModelTrainingContext:
        """Ejecuta todos los pasos y devuelve el contexto final."""
        context = ModelTrainingContext()
        for step in self._steps:
            print(f"  → {step.name}")
            context = step.execute(context)
        return context
