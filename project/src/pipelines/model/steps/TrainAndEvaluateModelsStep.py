"""Paso que entrena y evalúa cada modelo candidato."""

from dataclasses import replace

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep
from services.SklearnModelService import SklearnModelService


class TrainAndEvaluateModelsStep(ModelTrainingStep):
    """Entrena cada candidato y calcula sus métricas de prueba y validación."""

    def __init__(self, cv=None):
        """Recibe el esquema de validación cruzada que se usará."""
        self._cv = cv

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento y evaluación de modelos"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Entrena todos los candidatos y guarda sus métricas."""
        if (
            context.XTrain is None
            or context.yTrain is None
            or context.XTest is None
            or context.yTest is None
        ):
            raise ValueError(
                "TrainAndEvaluateModelsStep requiere los conjuntos ya divididos."
            )

        tunedParams = context.metadata.get("randomForestBestParams", {})
        tunedParamsText = (
            ", ".join(f"{key}={value}" for key, value in tunedParams.items())
            if tunedParams
            else ""
        )

        scores = tuple(
            SklearnModelService.evaluateModel(
                candidate=candidate,
                XTrain=context.XTrain,
                yTrain=context.yTrain,
                XTest=context.XTest,
                yTest=context.yTest,
                cv=self._cv,
                bestParams=(
                    tunedParamsText
                    if candidate.name == "Random Forest (GridSearchCV)"
                    else ""
                ),
            )
            for candidate in context.candidates
        )

        return replace(context, scores=scores)
