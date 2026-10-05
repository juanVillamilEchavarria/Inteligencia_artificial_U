from typing import List

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class DataPreparationPipeline:
    def __init__(self, steps: List[DataPreparationStep]):
        self._steps = steps

    def run(self) -> DataPreparationContext:
        context = DataPreparationContext()
        for step in self._steps:
            print(f"  → {step.name}")
            context = step.execute(context)
        return context
