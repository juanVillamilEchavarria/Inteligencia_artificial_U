"""Configuración y ejecución del entrenamiento del perceptrón."""

from typing import Tuple

from helpers.project_paths import CLEAN_DATASET_PATH
from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.PerceptronTrainingPipeline import PerceptronTrainingPipeline
from pipelines.train.steps.EvaluateStep import EvaluateStep
from pipelines.train.steps.LoadPreparedDataStep import LoadPreparedDataStep
from pipelines.train.steps.SelectFeaturesStep import SelectFeaturesStep
from pipelines.train.steps.StandardizeStep import StandardizeStep
from pipelines.train.steps.TrainPerceptronStep import TrainPerceptronStep


class PerceptronTrainingRunner:
    """Arma el pipeline con la configuración del modelo y lo ejecuta."""

    def __init__(
        self,
        dataPath: str = str(CLEAN_DATASET_PATH),
        targetName: str = "ruta_retrasada",
        featureNames: Tuple[str, ...] = ("toneladas_recogidas", "distancia_km"),
        learningRate: float = 0.1,
        epochs: int = 500,
    ):
        """Define la ruta del dataset, las variables y los hiperparámetros."""
        self._pipeline = PerceptronTrainingPipeline(
            steps=[
                LoadPreparedDataStep(dataPath),
                SelectFeaturesStep(targetName, featureNames),
                StandardizeStep(),
                TrainPerceptronStep(learningRate, epochs),
                EvaluateStep(),
            ]
        )

    def run(self) -> PerceptronTrainingContext:
        """Ejecuta el entrenamiento y entrega el contexto resultante."""
        return self._pipeline.run()
