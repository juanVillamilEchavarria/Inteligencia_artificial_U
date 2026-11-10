"""Fachada para ejecutar el estudio de sobreajuste."""

from pipelines.overfitting.OverfittingContext import OverfittingContext
from pipelines.overfitting.OverfittingRunner import OverfittingRunner
from pipelines.transform.DataPreparationContext import DataPreparationContext


class OverfittingController:
    """Coordina el entrenamiento de árboles con distintas profundidades."""

    def __init__(self, runner: OverfittingRunner):
        """Recibe el runner del estudio."""
        self._runner = runner

    def train(
        self, preparedData: DataPreparationContext
    ) -> OverfittingContext:
        """Ejecuta el estudio y devuelve el contexto resultante."""
        return self._runner.run(preparedData)
