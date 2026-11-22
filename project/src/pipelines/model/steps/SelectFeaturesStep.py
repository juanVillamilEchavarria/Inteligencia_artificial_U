"""Paso que separa las variables de entrada y la variable objetivo."""

from dataclasses import replace
from typing import Tuple

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep


class SelectFeaturesStep(ModelTrainingStep):
    """Valida las columnas y construye las matrices X e y."""

    def __init__(
        self,
        targetName: str = "es_ingreso",
        featureNames: Tuple[str, ...] = (
            "monto_log",
            "mes",
            "dia_semana",
            "es_fin_semana",
        ),
    ):
        """Define la variable objetivo y las entradas del modelo.

        No se incluyen ``tipo_movimiento`` ni ``categoria`` porque determinan
        directamente la variable objetivo y producirían fuga de información.
        """
        self._targetName = targetName
        self._featureNames = tuple(featureNames)

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Selección de variable objetivo y entradas"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Selecciona las columnas y verifica que la variable objetivo sea binaria."""
        if context.dfPrepared is None:
            raise ValueError(
                "SelectFeaturesStep requiere dfPrepared (falta LoadPreparedDataStep?)"
            )

        df = context.dfPrepared
        requiredColumns = [self._targetName, *self._featureNames]
        missingColumns = [column for column in requiredColumns if column not in df.columns]
        if missingColumns:
            raise ValueError(f"Faltan columnas en el dataset preparado: {missingColumns}")

        if df[requiredColumns].isnull().any().any():
            raise ValueError("Las variables del modelo contienen valores nulos.")

        targetValues = sorted(df[self._targetName].unique().tolist())
        if targetValues != [0, 1]:
            raise ValueError(
                f"La variable objetivo '{self._targetName}' debe ser binaria 0/1; "
                f"se encontraron: {targetValues}"
            )

        X = df[list(self._featureNames)].copy()
        y = df[self._targetName].astype(int).copy()

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
