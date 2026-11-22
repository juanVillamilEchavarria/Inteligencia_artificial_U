"""Paso que construye los modelos candidatos."""

from dataclasses import replace

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep
from services.SklearnModelService import SklearnModelService


class BuildCandidateModelsStep(ModelTrainingStep):
    """Crea los pipelines de regresión logística, Random Forest y MLP."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Construcción de modelos candidatos"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Agrega los candidatos al contexto."""
        candidates = SklearnModelService.buildCandidateModels()
        return replace(context, candidates=candidates)
