"""Paso que guarda el mejor modelo y sus métricas."""

from dataclasses import asdict, replace
from pathlib import Path

from helpers.project_paths import MODEL_METRICS_PATH, MODEL_PATH
from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep
from services.ModelPersistenceService import ModelPersistenceService


class PersistModelStep(ModelTrainingStep):
    """Serializa el mejor modelo con joblib y escribe un JSON de métricas."""

    def __init__(
        self,
        modelPath: Path = MODEL_PATH,
        metricsPath: Path = MODEL_METRICS_PATH,
    ):
        """Define las rutas de salida del modelo y de las métricas."""
        self._storage = ModelPersistenceService(modelPath, metricsPath)

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Persistencia del mejor modelo"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Guarda el modelo y devuelve las rutas en la metadata."""
        if context.bestModel is None:
            raise ValueError(
                "PersistModelStep requiere bestModel (falta SelectBestModelStep?)"
            )

        bestParams = context.metadata.get("randomForestBestParams", {})
        bestParamsText = (
            ", ".join(f"{key}={value}" for key, value in bestParams.items())
            if bestParams
            else ""
        )

        scores = [asdict(score) for score in context.scores]
        payload = {
            "modelName": context.bestModelName,
            "model": context.bestModel,
            "featureNames": list(context.featureNames),
            "targetName": context.targetName,
            "bestParams": bestParamsText,
            "trainCount": len(context.yTrain) if context.yTrain is not None else 0,
            "testCount": len(context.yTest) if context.yTest is not None else 0,
            "scores": scores,
        }

        modelPath = self._storage.save(payload)
        metricsPath = self._storage.saveMetrics(
            {
                "modelName": context.bestModelName,
                "featureNames": list(context.featureNames),
                "targetName": context.targetName,
                "bestParams": bestParamsText,
                "trainCount": payload["trainCount"],
                "testCount": payload["testCount"],
                "models": scores,
            }
        )

        metadata = dict(context.metadata)
        metadata["modelPath"] = modelPath
        metadata["metricsPath"] = metricsPath

        return replace(context, metadata=metadata)
