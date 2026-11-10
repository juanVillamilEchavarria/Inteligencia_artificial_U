"""Paso que valida columnas, nulos y la variable objetivo."""

from dataclasses import replace
from typing import Optional, Tuple

from pipelines.core.PipelineStep import PipelineStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class ValidateDataStep(PipelineStep[DataPreparationContext]):
    """Comprueba que el dataset tenga las columnas y valores esperados."""

    def __init__(
        self,
        requiredColumns: Tuple[str, ...],
        binaryTarget: Optional[str] = None,
    ):
        """Define las columnas obligatorias y la posible variable binaria."""
        self._requiredColumns = tuple(requiredColumns)
        self._binaryTarget = binaryTarget

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Validación del dataset"

    def execute(
        self, context: DataPreparationContext
    ) -> DataPreparationContext:
        """Valida el dataframe y lo deja disponible como ``dfPrepared``."""
        if context.dfRaw is None:
            raise ValueError("ValidateDataStep requiere dfRaw (falta un paso de carga?)")

        dataframe = context.dfRaw
        missingColumns = [
            column
            for column in self._requiredColumns
            if column not in dataframe.columns
        ]
        if missingColumns:
            raise ValueError(f"Faltan columnas en el dataset: {missingColumns}")

        nullColumns = {
            column: int(dataframe[column].isnull().sum())
            for column in self._requiredColumns
            if dataframe[column].isnull().any()
        }
        if nullColumns:
            raise ValueError(f"Hay valores nulos en columnas requeridas: {nullColumns}")

        if self._binaryTarget is not None:
            values = sorted(dataframe[self._binaryTarget].unique().tolist())
            if values != [0, 1]:
                raise ValueError(
                    f"La variable objetivo '{self._binaryTarget}' debe ser binaria 0/1; "
                    f"se encontraron: {values}"
                )

        metadata = dict(context.metadata)
        metadata["rows"] = len(dataframe)
        metadata["duplicates"] = int(dataframe.duplicated().sum())
        metadata["validatedColumns"] = list(self._requiredColumns)

        return replace(
            context,
            dfPrepared=dataframe.copy(),
            metadata=metadata,
        )
