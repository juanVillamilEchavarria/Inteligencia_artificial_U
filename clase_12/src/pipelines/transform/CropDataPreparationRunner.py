"""Composición del pipeline de preparación del dataset de cultivos."""

from pathlib import Path
from typing import Tuple

from api.CropDataGateway import CropDataGateway
from enums.CropColumns import CropColumns
from helpers.project_paths import CROP_DATASET_PATH
from pipelines.core.Pipeline import Pipeline
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.LoadCropDataStep import LoadCropDataStep
from pipelines.transform.steps.SelectFeaturesStep import SelectFeaturesStep
from pipelines.transform.steps.SplitDataStep import SplitDataStep
from pipelines.transform.steps.ValidateDataStep import ValidateDataStep


class CropDataPreparationRunner:
    """Arma y ejecuta el pipeline de datos del problema de cultivos."""

    def __init__(
        self,
        dataPath: Path = CROP_DATASET_PATH,
        featureNames: Tuple[str, ...] = (
            CropColumns.PRECIPITACION_MM.value,
            CropColumns.TEMPERATURA_C.value,
        ),
        targetName: str = CropColumns.COSECHA_EXITOSA.value,
        testSize: float = 0.2,
        randomState: int = 42,
    ):
        """Configura rutas, variables, división y semilla."""
        requiredColumns = (*featureNames, targetName)
        gateway = CropDataGateway(dataPath)

        self._pipeline = Pipeline(
            [
                LoadCropDataStep(gateway),
                ValidateDataStep(requiredColumns, binaryTarget=targetName),
                SelectFeaturesStep(
                    featureNames,
                    targetName,
                    requireBinaryTarget=True,
                ),
                SplitDataStep(
                    testSize=testSize,
                    randomState=randomState,
                    stratify=True,
                ),
            ]
        )

    def run(self) -> DataPreparationContext:
        """Ejecuta la preparación y entrega el contexto resultante."""
        return self._pipeline.run(DataPreparationContext())
