"""Paso que selecciona el modelo con el mejor F1."""

from dataclasses import replace

from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.core.PipelineStep import PipelineStep
from services.ClassificationService import ClassificationService


class SelectBestModelStep(PipelineStep[ClassificationContext]):
    """Elige el candidato con el F1 más alto."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Selección del mejor modelo por F1"

    def execute(self, context: ClassificationContext) -> ClassificationContext:
        """Guarda el nombre y el objeto del mejor modelo."""
        if not context.scores or not context.candidates:
            raise ValueError("SelectBestModelStep requiere modelos evaluados.")

        bestName = ClassificationService.select_best_by_f1(context.scores)
        bestModel = next(
            (
                candidate.model
                for candidate in context.candidates
                if candidate.name == bestName
            ),
            None,
        )
        if bestModel is None:
            raise ValueError(f"No se encontró el modelo seleccionado: {bestName}")

        return replace(
            context,
            bestModelName=bestName,
            bestModel=bestModel,
        )
