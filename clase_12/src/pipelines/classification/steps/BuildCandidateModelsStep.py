"""Paso que construye los tres modelos candidatos."""

from dataclasses import replace

from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.core.PipelineStep import PipelineStep
from services.ClassificationService import ClassificationService


class BuildCandidateModelsStep(PipelineStep[ClassificationContext]):
    """Crea los pipelines de regresión logística, KNN y árbol."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Construcción de modelos candidatos"

    def execute(self, context: ClassificationContext) -> ClassificationContext:
        """Agrega los candidatos al contexto."""
        if context.data is None:
            raise ValueError("BuildCandidateModelsStep requiere datos preparados.")
        candidates = ClassificationService.build_candidate_models()
        return replace(context, candidates=candidates)
