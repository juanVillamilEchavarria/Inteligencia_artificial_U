"""Paso que optimiza los hiperparámetros del Random Forest."""

from dataclasses import replace

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep
from services.SklearnModelService import SklearnModelService


class TuneRandomForestStep(ModelTrainingStep):
    """Ejecuta GridSearchCV sobre el candidato Random Forest."""

    def __init__(self, cv=None):
        """Recibe el esquema de validación cruzada que se usará."""
        self._cv = cv

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Optimización de hiperparámetros (GridSearchCV)"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Reemplaza el Random Forest base por la mejor versión encontrada."""
        if context.XTrain is None or context.yTrain is None:
            raise ValueError(
                "TuneRandomForestStep requiere XTrain e yTrain (falta SplitDataStep?)"
            )

        baseCandidate = next(
            (
                candidate
                for candidate in context.candidates
                if candidate.name == "Random Forest"
            ),
            None,
        )
        if baseCandidate is None:
            return context

        tunedCandidate, bestParams, bestScore = SklearnModelService.tuneRandomForest(
            baseCandidate,
            context.XTrain,
            context.yTrain,
            self._cv,
        )

        candidates = tuple(
            tunedCandidate if candidate.name == "Random Forest" else candidate
            for candidate in context.candidates
        )

        metadata = dict(context.metadata)
        metadata["randomForestBestParams"] = bestParams
        metadata["randomForestBestCvScore"] = bestScore

        return replace(context, candidates=candidates, metadata=metadata)
