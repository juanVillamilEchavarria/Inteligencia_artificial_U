"""Paso que separa las variables de entrada y la variable objetivo."""

from dataclasses import replace
from typing import Tuple

from pipelines.core.PipelineStep import PipelineStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class SelectFeaturesStep(PipelineStep[DataPreparationContext]):
    """Construye las matrices X e y a partir del dataset validado."""

    def __init__(
        self,
        featureNames: Tuple[str, ...],
        targetName: str,
        requireBinaryTarget: bool = False,
    ):
        """Define las entradas, la salida y si la salida debe ser 0/1."""
        self._featureNames = tuple(featureNames)
        self._targetName = targetName
        self._requireBinaryTarget = requireBinaryTarget

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Selección de entradas y variable objetivo"

    def execute(
        self, context: DataPreparationContext
    ) -> DataPreparationContext:
        """Selecciona las columnas y verifica que no haya nulos."""
        if context.dfPrepared is None:
            raise ValueError(
                "SelectFeaturesStep requiere dfPrepared (falta ValidateDataStep?)"
            )

        dataframe = context.dfPrepared
        requiredColumns = [*self._featureNames, self._targetName]
        missingColumns = [
            column for column in requiredColumns if column not in dataframe.columns
        ]
        if missingColumns:
            raise ValueError(f"Faltan columnas para el modelo: {missingColumns}")

        if self._requireBinaryTarget:
            values = sorted(dataframe[self._targetName].unique().tolist())
            if values != [0, 1]:
                raise ValueError(
                    f"La variable objetivo '{self._targetName}' debe ser binaria 0/1; "
                    f"se encontraron: {values}"
                )

        X = dataframe[list(self._featureNames)].astype(float)
        y = dataframe[self._targetName].astype(int)

        metadata = dict(context.metadata)
        metadata["rows"] = len(dataframe)

        return replace(
            context,
            featureNames=self._featureNames,
            targetName=self._targetName,
            X=X,
            y=y,
            metadata=metadata,
        )
