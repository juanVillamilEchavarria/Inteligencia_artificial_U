"""Paso que entrena y evalúa cada modelo candidato."""

from dataclasses import replace

from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.core.PipelineStep import PipelineStep
from services.ClassificationService import ClassificationService


class TrainAndEvaluateModelsStep(PipelineStep[ClassificationContext]):
    """Entrena cada candidato y calcula sus métricas de prueba."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento y evaluación de modelos"

    def execute(self, context: ClassificationContext) -> ClassificationContext:
        """Entrena todos los candidatos y guarda sus métricas."""
        data = context.data
        if (
            data is None
            or data.X_train is None
            or data.y_train is None
            or data.X_test is None
            or data.y_test is None
            or data.X is None
            or data.y is None
        ):
            raise ValueError(
                "TrainAndEvaluateModelsStep requiere datos ya divididos."
            )

        scores = tuple(
            ClassificationService.evaluate_model(
                candidate=candidate,
                X_train=data.X_train,
                y_train=data.y_train,
                X_test=data.X_test,
                y_test=data.y_test,
                X_full=data.X,
                y_full=data.y,
                cv=5,
            )
            for candidate in context.candidates
        )
        return replace(context, scores=scores)
