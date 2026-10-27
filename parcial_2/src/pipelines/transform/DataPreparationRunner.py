"""Configuración y ejecución del pipeline de preparación de datos."""

from helpers.project_paths import CLEAN_DATASET_PATH
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.DataPreparationPipeline import DataPreparationPipeline
from pipelines.transform.steps.CleanDataStep import CleanDataStep
from pipelines.transform.steps.EdaStep import EdaStep
from pipelines.transform.steps.FeatureEngineeringStep import FeatureEngineeringStep
from pipelines.transform.steps.LoadDataStep import LoadDataStep
from pipelines.transform.steps.PersistStep import PersistStep


class DataPreparationRunner:
    """Arma el pipeline de preparación con la ruta de salida indicada."""

    def __init__(self, outputPath: str = str(CLEAN_DATASET_PATH)):
        """Define dónde se guardará el dataset preparado."""
        self._pipeline = DataPreparationPipeline(
            steps=[
                LoadDataStep(),
                EdaStep(),
                CleanDataStep(),
                FeatureEngineeringStep(),
                PersistStep(outputPath),
            ]
        )

    def run(self) -> DataPreparationContext:
        """Ejecuta la preparación y entrega el contexto resultante."""
        return self._pipeline.run()
