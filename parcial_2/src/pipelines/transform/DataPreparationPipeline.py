"""Pipeline que ejecuta en orden la preparación y limpieza del dataset."""

from typing import List

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class DataPreparationPipeline:
    """Encadena pasos de transformación sobre un contexto inmutable."""

    def __init__(self, steps: List[DataPreparationStep]):
        """Recibe los pasos en el orden en que deben ejecutarse."""
        self._steps = steps

    def run(self) -> DataPreparationContext:
        """Ejecuta todos los pasos y devuelve el contexto final."""
        context = DataPreparationContext()
        for step in self._steps:
            print(f"  → {step.name}")
            context = step.execute(context)
        return context
