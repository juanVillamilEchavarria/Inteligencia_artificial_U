"""Configuración y ejecución del pipeline de comparación de modelos."""

from pathlib import Path
from typing import Tuple

from sklearn.model_selection import StratifiedKFold

from helpers.project_paths import MODEL_METRICS_PATH, MODEL_PATH, PREPARED_DATASET_PATH
from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.ModelTrainingPipeline import ModelTrainingPipeline
from pipelines.model.steps.BuildCandidateModelsStep import BuildCandidateModelsStep
from pipelines.model.steps.BuildModelReportStep import BuildModelReportStep
from pipelines.model.steps.LoadPreparedDataStep import LoadPreparedDataStep
from pipelines.model.steps.PersistModelStep import PersistModelStep
from pipelines.model.steps.SelectBestModelStep import SelectBestModelStep
from pipelines.model.steps.SelectFeaturesStep import SelectFeaturesStep
from pipelines.model.steps.SplitDataStep import SplitDataStep
from pipelines.model.steps.TrainAndEvaluateModelsStep import (
    TrainAndEvaluateModelsStep,
)
from pipelines.model.steps.TuneRandomForestStep import TuneRandomForestStep


class ModelTrainingRunner:
    """Arma el pipeline con la configuración del modelo y lo ejecuta."""

    def __init__(
        self,
        dataPath: str = str(PREPARED_DATASET_PATH),
        targetName: str = "es_ingreso",
        featureNames: Tuple[str, ...] = (
            "monto_log",
            "mes",
            "dia_semana",
            "es_fin_semana",
        ),
        testSize: float = 0.25,
        randomState: int = 42,
        cvFolds: int = 5,
        modelPath: Path = MODEL_PATH,
        metricsPath: Path = MODEL_METRICS_PATH,
    ):
        """Define la ruta del dataset, las variables y los hiperparámetros."""
        cv = StratifiedKFold(
            n_splits=cvFolds,
            shuffle=True,
            random_state=randomState,
        )
        self._pipeline = ModelTrainingPipeline(
            steps=[
                LoadPreparedDataStep(dataPath),
                SelectFeaturesStep(targetName, featureNames),
                SplitDataStep(testSize, randomState),
                BuildCandidateModelsStep(),
                TuneRandomForestStep(cv),
                TrainAndEvaluateModelsStep(cv),
                SelectBestModelStep(),
                PersistModelStep(modelPath, metricsPath),
                BuildModelReportStep(),
            ]
        )

    def run(self) -> ModelTrainingContext:
        """Ejecuta la comparación y entrega el contexto resultante."""
        return self._pipeline.run()
