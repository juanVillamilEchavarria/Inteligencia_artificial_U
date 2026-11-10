"""Paso que entrena árboles con profundidades crecientes."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.overfitting.OverfittingContext import OverfittingContext
from services.OverfittingService import OverfittingService


class TrainTreeDepthsStep(PipelineStep[OverfittingContext]):
    """Entrena un árbol por cada profundidad y recoge exactitudes."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento de árboles por profundidad"

    def execute(self, context: OverfittingContext) -> OverfittingContext:
        """Calcula las exactitudes de entrenamiento y prueba."""
        data = context.data
        if (
            data is None
            or data.X_train is None
            or data.y_train is None
            or data.X_test is None
            or data.y_test is None
        ):
            raise ValueError(
                "TrainTreeDepthsStep requiere datos ya divididos."
            )

        scores = OverfittingService.train_depths(
            data.X_train,
            data.y_train,
            data.X_test,
            data.y_test,
        )
        return replace(context, scores=scores)
