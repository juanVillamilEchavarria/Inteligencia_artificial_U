"""Fachada para entrenar el modelo de regresión."""

from pipelines.regression.RegressionContext import RegressionContext
from pipelines.regression.RegressionRunner import RegressionRunner
from pipelines.transform.DataPreparationContext import DataPreparationContext


class RegressionController:
    """Coordina la ejecución del pipeline de regresión."""

    def __init__(self, runner: RegressionRunner):
        """Recibe el runner que ejecuta el pipeline."""
        self._runner = runner

    def train(
        self, preparedData: DataPreparationContext
    ) -> RegressionContext:
        """Ejecuta la regresión y devuelve el contexto resultante."""
        return self._runner.run(preparedData)
