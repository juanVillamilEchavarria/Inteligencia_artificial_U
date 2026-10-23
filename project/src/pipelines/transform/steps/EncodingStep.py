"""Paso que convierte las variables categóricas en columnas binarias."""

from dataclasses import replace

import pandas as pd

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class EncodingStep(DataPreparationStep):
    """Aplica one-hot encoding a las columnas categóricas indicadas."""

    def __init__(self, categoricalColumns=None):
        """Define las columnas que se van a codificar."""
        self._categoricalColumns = categoricalColumns or [
            "categoria",
            "tipo_movimiento",
            "cuenta",
        ]

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Encoding de variables categoricas"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Agrega las columnas codificadas y registra cuáles se crearon."""
        if context.dfPrepared is None:
            raise ValueError("EncodingStep requiere dfPrepared (falta FeatureEngineeringStep?)")

        dfEncoded = context.dfPrepared.copy()
        encodedMetadata = {}

        for col in self._categoricalColumns:
            if col in dfEncoded.columns:
                dummies = pd.get_dummies(dfEncoded[col], prefix=col, dtype=int)
                dfEncoded = pd.concat([dfEncoded, dummies], axis=1)
                encodedMetadata[col] = list(dummies.columns)

        metadata = dict(context.metadata)
        metadata["encodedColumns"] = encodedMetadata
        return replace(context, dfPrepared=dfEncoded, metadata=metadata)
