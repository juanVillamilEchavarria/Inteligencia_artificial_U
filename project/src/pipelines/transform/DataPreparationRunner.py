from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.DataPreparationPipeline import DataPreparationPipeline
from pipelines.transform.steps.LoadDataStep import LoadDataStep
from pipelines.transform.steps.EdaStep import EdaStep
from pipelines.transform.steps.CleanDataStep import CleanDataStep
from pipelines.transform.steps.FeatureEngineeringStep import FeatureEngineeringStep
from pipelines.transform.steps.EncodingStep import EncodingStep
from pipelines.transform.steps.PersistStep import PersistStep


class DataPreparationRunner:
    def __init__(self, outputPath: str = "data_prepared.csv"):
        self._pipeline = DataPreparationPipeline(steps=[
            LoadDataStep(),
            EdaStep(),
            CleanDataStep(),
            FeatureEngineeringStep(),
            EncodingStep(),
            PersistStep(outputPath),
        ])

    def run(self) -> DataPreparationContext:
        return self._pipeline.run()
