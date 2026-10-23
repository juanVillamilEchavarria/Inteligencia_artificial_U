"""Paso que separa las variables de entrada y la variable objetivo."""

from dataclasses import replace
from typing import Tuple

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep


class SelectFeaturesStep(TrainingStep):
    """Valida las columnas y construye las matrices X e y."""

    def __init__(
        self,
        targetName: str = "es_ingreso",
        featureNames: Tuple[str, ...] = ("monto_log", "mes"),
    ):
        """Define la variable objetivo y las dos entradas del perceptrón."""
        if len(featureNames) != 2:
            raise ValueError("El perceptrón requiere exactamente dos variables de entrada.")
        self._targetName = targetName
        self._featureNames = featureNames

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Selección de variable objetivo y entradas"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Selecciona las columnas y verifica que la variable objetivo sea binaria."""
        if context.dfPrepared is None:
            raise ValueError("SelectFeaturesStep requiere dfPrepared (falta LoadPreparedDataStep?)")

        df = context.dfPrepared
        requiredColumns = [self._targetName, *self._featureNames]
        missingColumns = [column for column in requiredColumns if column not in df.columns]
        if missingColumns:
            raise ValueError(f"Faltan columnas en el dataset preparado: {missingColumns}")

        if df[self._targetName].isnull().any():
            raise ValueError(f"La variable objetivo '{self._targetName}' contiene valores nulos.")

        targetValues = sorted(df[self._targetName].unique().tolist())
        if targetValues != [0, 1]:
            raise ValueError(
                f"La variable objetivo '{self._targetName}' debe ser binaria 0/1; "
                f"se encontraron: {targetValues}"
            )

        X = df[list(self._featureNames)].to_numpy(dtype=float)
        y = df[self._targetName].to_numpy(dtype=int)

        metadata = dict(context.metadata)
        metadata["rows"] = len(df)

        return replace(
            context,
            featureNames=self._featureNames,
            targetName=self._targetName,
            X=X,
            y=y,
            metadata=metadata,
        )
