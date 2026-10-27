"""Paso que guarda el dataset preparado en disco."""

from dataclasses import replace
from pathlib import Path

from helpers.project_paths import CLEAN_DATASET_PATH
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class PersistStep(DataPreparationStep):
    """Escribe el dataframe preparado como CSV."""

    def __init__(self, outputPath: str = str(CLEAN_DATASET_PATH)):
        """Define la ruta del archivo de salida."""
        self._outputPath = outputPath

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Persistencia de dataset"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Crea la carpeta si hace falta y guarda el CSV."""
        if context.dfPrepared is None:
            raise ValueError("PersistStep requiere dfPrepared (falta FeatureEngineeringStep?)")

        outputPath = Path(self._outputPath)
        outputPath.parent.mkdir(parents=True, exist_ok=True)
        context.dfPrepared.to_csv(outputPath, index=False)

        metadata = dict(context.metadata)
        metadata["outputPath"] = self._outputPath
        return replace(context, metadata=metadata)
