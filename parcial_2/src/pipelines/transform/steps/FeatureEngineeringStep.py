"""Paso que valida y deja listas las variables usadas por el modelo."""

from dataclasses import replace

import pandas as pd

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class FeatureEngineeringStep(DataPreparationStep):
    """Verifica los tipos y registra las columnas de entrada y objetivo."""

    FEATURE_COLUMNS = ("toneladas_recogidas", "distancia_km")
    TARGET_COLUMN = "ruta_retrasada"

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Feature engineering"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Asegura los tipos numéricos y agrega metadatos de features."""
        if context.dfClean is None:
            raise ValueError("FeatureEngineeringStep requiere dfClean (falta CleanDataStep?)")

        dfPrepared = context.dfClean.copy()
        for column in self.FEATURE_COLUMNS:
            dfPrepared[column] = pd.to_numeric(dfPrepared[column], errors="raise")
        dfPrepared[self.TARGET_COLUMN] = dfPrepared[self.TARGET_COLUMN].astype(int)

        metadata = dict(context.metadata)
        metadata["featureColumns"] = list(self.FEATURE_COLUMNS)
        metadata["targetColumn"] = self.TARGET_COLUMN
        metadata["rows"] = len(dfPrepared)
        return replace(context, dfPrepared=dfPrepared, metadata=metadata)
