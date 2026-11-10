"""Composición del pipeline de comparación de modelos."""

from pathlib import Path

from helpers.project_paths import CLASSIFICATION_MODEL_PATH
from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.classification.steps.BuildCandidateModelsStep import (
    BuildCandidateModelsStep,
)
from pipelines.classification.steps.BuildClassificationReportStep import (
    BuildClassificationReportStep,
)
from pipelines.classification.steps.PersistClassificationModelStep import (
    PersistClassificationModelStep,
)
from pipelines.classification.steps.SelectBestModelStep import SelectBestModelStep
from pipelines.classification.steps.TrainAndEvaluateModelsStep import (
    TrainAndEvaluateModelsStep,
)
from pipelines.core.Pipeline import Pipeline
from pipelines.transform.DataPreparationContext import DataPreparationContext


class ClassificationRunner:
    """Arma el pipeline de clasificación y lo ejecuta."""

    def __init__(self, modelPath: Path = CLASSIFICATION_MODEL_PATH):
        """Define dónde se guardará el mejor modelo."""
        self._pipeline = Pipeline(
            [
                BuildCandidateModelsStep(),
                TrainAndEvaluateModelsStep(),
                SelectBestModelStep(),
                PersistClassificationModelStep(modelPath),
                BuildClassificationReportStep(),
            ]
        )

    def run(
        self, preparedData: DataPreparationContext
    ) -> ClassificationContext:
        """Ejecuta la comparación y entrega el contexto resultante."""
        return self._pipeline.run(ClassificationContext(data=preparedData))
