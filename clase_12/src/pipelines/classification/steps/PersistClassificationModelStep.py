"""Paso que guarda el mejor modelo en disco."""

from dataclasses import replace
from pathlib import Path

from helpers.project_paths import CLASSIFICATION_MODEL_PATH
from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.core.PipelineStep import PipelineStep
from services.ModelPersistenceService import ModelPersistenceService


class PersistClassificationModelStep(PipelineStep[ClassificationContext]):
    """Serializa el mejor modelo con joblib."""

    def __init__(self, modelPath: Path = CLASSIFICATION_MODEL_PATH):
        """Define la ruta del archivo del modelo."""
        self._persistence = ModelPersistenceService(modelPath)

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Guardado del mejor modelo"

    def execute(self, context: ClassificationContext) -> ClassificationContext:
        """Guarda el modelo y deja la ruta en los metadatos."""
        if context.bestModel is None:
            raise ValueError("PersistClassificationModelStep requiere bestModel.")

        modelPath = self._persistence.save(context.bestModel)
        metadata = dict(context.metadata)
        metadata["modelPath"] = modelPath
        return replace(context, metadata=metadata)
