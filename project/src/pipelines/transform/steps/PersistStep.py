from dataclasses import replace

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class PersistStep(DataPreparationStep):
    def __init__(self, outputPath: str = "data_prepared.csv"):
        self._outputPath = outputPath

    @property
    def name(self) -> str:
        return "Persistencia de dataset"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        if context.dfPrepared is None:
            raise ValueError("PersistStep requiere dfPrepared (falta EncodingStep?)")

        context.dfPrepared.to_csv(self._outputPath, index=False)

        metadata = dict(context.metadata)
        metadata["outputPath"] = self._outputPath
        return replace(context, metadata=metadata)
