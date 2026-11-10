"""Composición del pipeline de sobreajuste."""

from pipelines.core.Pipeline import Pipeline
from pipelines.overfitting.OverfittingContext import OverfittingContext
from pipelines.overfitting.steps.BuildOverfittingReportStep import (
    BuildOverfittingReportStep,
)
from pipelines.overfitting.steps.TrainTreeDepthsStep import TrainTreeDepthsStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class OverfittingRunner:
    """Arma el estudio de profundidad y lo ejecuta."""

    def __init__(self):
        """Configura los pasos del estudio."""
        self._pipeline = Pipeline(
            [
                TrainTreeDepthsStep(),
                BuildOverfittingReportStep(),
            ]
        )

    def run(self, preparedData: DataPreparationContext) -> OverfittingContext:
        """Ejecuta el estudio y entrega el contexto resultante."""
        return self._pipeline.run(OverfittingContext(data=preparedData))
