from dataclasses import replace

import pandas as pd

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class EncodingStep(DataPreparationStep):
    def __init__(self, categoricalColumns=None):
        self._categoricalColumns = categoricalColumns or [
            "categoria",
            "tipo_movimiento",
            "cuenta",
        ]

    @property
    def name(self) -> str:
        return "Encoding de variables categoricas"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
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
