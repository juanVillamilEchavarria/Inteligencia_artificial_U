"""Composición del pipeline de regresión."""

from pipelines.core.Pipeline import Pipeline
from pipelines.regression.RegressionContext import RegressionContext
from pipelines.regression.steps.EvaluateRegressionStep import EvaluateRegressionStep
from pipelines.regression.steps.TrainRegressionStep import TrainRegressionStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class RegressionRunner:
    """Arma el pipeline de regresión y lo ejecuta."""

    def __init__(self):
        """Configura los pasos de entrenamiento y evaluación."""
        self._pipeline = Pipeline(
            [
                TrainRegressionStep(),
                EvaluateRegressionStep(),
            ]
        )

    def run(self, preparedData: DataPreparationContext) -> RegressionContext:
        """Ejecuta la regresión y entrega el contexto resultante."""
        return self._pipeline.run(RegressionContext(data=preparedData))
