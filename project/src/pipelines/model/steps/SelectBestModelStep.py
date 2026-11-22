"""Paso que selecciona el mejor modelo por validación cruzada."""

from dataclasses import replace

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep
from services.SklearnModelService import SklearnModelService


class SelectBestModelStep(ModelTrainingStep):
    """Elige el candidato con mejor F1 macro promedio en validación cruzada."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Selección del mejor modelo"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Guarda el nombre y el objeto del mejor modelo."""
        bestScore = SklearnModelService.selectBestScore(context.scores)
        bestCandidate = next(
            (
                candidate
                for candidate in context.candidates
                if candidate.name == bestScore.modelName
            ),
            None,
        )
        if bestCandidate is None:
            raise ValueError(f"No se encontró el modelo '{bestScore.modelName}'.")

        return replace(
            context,
            bestModelName=bestScore.modelName,
            bestModel=bestCandidate.model,
        )
