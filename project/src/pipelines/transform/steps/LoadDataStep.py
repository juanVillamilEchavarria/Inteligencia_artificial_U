from dataclasses import replace

from api.MovementsGateWay import MovementsGateWay
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class LoadDataStep(DataPreparationStep):
    @property
    def name(self) -> str:
        return "Carga de datos"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        collection = MovementsGateWay.getData()
        dfRaw = collection.to_dataframe()
        return replace(context, dfRaw=dfRaw)
