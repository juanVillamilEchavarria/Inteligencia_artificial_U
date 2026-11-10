"""Composición del pipeline de datos para la regresión."""

from pathlib import Path
from typing import Tuple

from enums.CropColumns import RegressionColumns
from helpers.project_paths import REGRESSION_DATASET_PATH
from pipelines.core.Pipeline import Pipeline
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.GenerateRegressionDataStep import (
    GenerateRegressionDataStep,
)
from pipelines.transform.steps.PersistDatasetStep import PersistDatasetStep
from pipelines.transform.steps.SelectFeaturesStep import SelectFeaturesStep
from pipelines.transform.steps.SplitDataStep import SplitDataStep
from pipelines.transform.steps.ValidateDataStep import ValidateDataStep


class RegressionDataPreparationRunner:
    """Genera, guarda y prepara el dataset sintético de rendimiento."""

    def __init__(
        self,
        outputPath: Path = REGRESSION_DATASET_PATH,
        featureNames: Tuple[str, ...] = (
            RegressionColumns.PRECIPITACION_MM.value,
            RegressionColumns.TEMPERATURA_C.value,
            RegressionColumns.FERTILIZANTE_KG_HA.value,
        ),
        targetName: str = RegressionColumns.RENDIMIENTO_KG_HA.value,
        testSize: float = 0.2,
        randomState: int = 42,
    ):
        """Configura la salida, las variables y la división de los datos."""
        requiredColumns = (*featureNames, targetName)

        self._pipeline = Pipeline(
            [
                GenerateRegressionDataStep(),
                PersistDatasetStep(str(outputPath)),
                ValidateDataStep(requiredColumns),
                SelectFeaturesStep(
                    featureNames,
                    targetName,
                    requireBinaryTarget=False,
                ),
                SplitDataStep(
                    testSize=testSize,
                    randomState=randomState,
                    stratify=False,
                ),
            ]
        )

    def run(self) -> DataPreparationContext:
        """Ejecuta la preparación y entrega el contexto resultante."""
        return self._pipeline.run(DataPreparationContext())
