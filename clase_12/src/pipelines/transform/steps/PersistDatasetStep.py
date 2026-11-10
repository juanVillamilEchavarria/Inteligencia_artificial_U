"""Paso que guarda un dataset en disco."""

from dataclasses import replace
from pathlib import Path

from pipelines.core.PipelineStep import PipelineStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class PersistDatasetStep(PipelineStep[DataPreparationContext]):
    """Escribe el dataframe crudo como CSV."""

    def __init__(self, outputPath: str):
        """Define la ruta del archivo de salida."""
        self._outputPath = Path(outputPath)

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Persistencia del dataset"

    def execute(
        self, context: DataPreparationContext
    ) -> DataPreparationContext:
        """Crea la carpeta si hace falta y guarda el CSV."""
        if context.dfRaw is None:
            raise ValueError("PersistDatasetStep requiere dfRaw.")

        self._outputPath.parent.mkdir(parents=True, exist_ok=True)
        context.dfRaw.to_csv(self._outputPath, index=False)

        metadata = dict(context.metadata)
        metadata["outputPath"] = str(self._outputPath)
        return replace(context, metadata=metadata)
