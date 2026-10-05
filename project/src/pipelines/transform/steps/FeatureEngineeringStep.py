from dataclasses import replace

import numpy as np

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class FeatureEngineeringStep(DataPreparationStep):
    @property
    def name(self) -> str:
        return "Feature engineering"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        if context.dfClean is None:
            raise ValueError("FeatureEngineeringStep requiere dfClean (falta CleanDataStep?)")

        dfPrepared = context.dfClean.copy()

        dfPrepared["monto_log"] = np.log1p(dfPrepared["monto"])
        dfPrepared["es_ingreso"] = (dfPrepared["tipo_movimiento"] == "Ingreso").astype(int)
        dfPrepared["mes"] = dfPrepared["fecha"].dt.month
        dfPrepared["dia_semana"] = dfPrepared["fecha"].dt.dayofweek
        dfPrepared["es_fin_semana"] = (dfPrepared["dia_semana"] >= 5).astype(int)

        metadata = dict(context.metadata)
        metadata["derivedColumns"] = [
            "monto_log",
            "es_ingreso",
            "mes",
            "dia_semana",
            "es_fin_semana",
        ]
        return replace(context, dfPrepared=dfPrepared, metadata=metadata)
