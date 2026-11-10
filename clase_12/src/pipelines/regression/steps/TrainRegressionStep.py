"""Paso que entrena la regresión lineal."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.regression.RegressionContext import RegressionContext
from services.RegressionService import RegressionService


class TrainRegressionStep(PipelineStep[RegressionContext]):
    """Construye y entrena el pipeline de regresión lineal."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento de la regresión lineal"

    def execute(self, context: RegressionContext) -> RegressionContext:
        """Entrena el modelo con los datos de entrenamiento."""
        data = context.data
        if data is None or data.X_train is None or data.y_train is None:
            raise ValueError("TrainRegressionStep requiere datos de entrenamiento.")

        model = RegressionService.build_model()
        model = RegressionService.train(model, data.X_train, data.y_train)
        return replace(context, model=model)
