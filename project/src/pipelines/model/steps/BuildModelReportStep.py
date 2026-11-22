"""Paso que construye el reporte final de la comparación."""

from dataclasses import replace

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.dtos.ModelReport import ModelReport
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep
from services.SklearnModelService import SklearnModelService


class BuildModelReportStep(ModelTrainingStep):
    """Reúne las métricas y las rutas de los artefactos en un DTO."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Construcción del reporte de modelos"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Genera el reporte a partir del contexto ya completado."""
        if not context.scores or context.bestModel is None:
            raise ValueError(
                "BuildModelReportStep requiere modelos entrenados y seleccionados."
            )

        bestScore = SklearnModelService.selectBestScore(context.scores)

        report = ModelReport(
            scores=context.scores,
            bestModelName=context.bestModelName,
            featureNames=context.featureNames,
            targetName=context.targetName,
            trainCount=len(context.yTrain) if context.yTrain is not None else 0,
            testCount=len(context.yTest) if context.yTest is not None else 0,
            modelPath=context.metadata.get("modelPath", ""),
            metricsPath=context.metadata.get("metricsPath", ""),
            bestParams=bestScore.bestParams,
            bestConfusionMatrix=bestScore.confusionMatrix,
        )

        return replace(context, report=report)
