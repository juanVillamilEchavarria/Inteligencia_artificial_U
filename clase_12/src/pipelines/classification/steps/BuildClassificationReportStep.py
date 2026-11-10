"""Paso que construye el reporte final de clasificación."""

from dataclasses import replace

from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.classification.dtos.ClassificationReport import ClassificationReport
from pipelines.core.PipelineStep import PipelineStep
from services.ClassificationService import ClassificationService


class BuildClassificationReportStep(PipelineStep[ClassificationContext]):
    """Calcula matriz de confusión y coeficientes del mejor modelo."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Construcción del reporte de clasificación"

    def execute(self, context: ClassificationContext) -> ClassificationContext:
        """Crea el DTO final con todas las métricas."""
        data = context.data
        if (
            data is None
            or data.X_test is None
            or data.y_test is None
            or data.X_train is None
            or context.bestModel is None
        ):
            raise ValueError(
                "BuildClassificationReportStep requiere datos y modelo entrenado."
            )

        matrix = ClassificationService.confusion_matrix(
            context.bestModel,
            data.X_test,
            data.y_test,
        )
        weights, bias = ClassificationService.logistic_coefficients(
            context.bestModel
        )

        report = ClassificationReport(
            scores=context.scores,
            bestModelName=context.bestModelName,
            confusionMatrix=matrix,
            weights=weights,
            bias=bias,
            featureNames=data.featureNames,
            targetName=data.targetName,
            trainCount=len(data.X_train),
            testCount=len(data.X_test),
            modelPath=str(context.metadata.get("modelPath", "")),
        )
        return replace(context, report=report)
