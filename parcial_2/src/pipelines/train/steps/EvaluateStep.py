"""Paso que calcula las métricas finales del modelo."""

from dataclasses import replace

import numpy as np

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.dtos.PerceptronReport import PerceptronReport
from pipelines.train.steps.TrainingStep import TrainingStep
from services.PerceptronService import PerceptronService


class EvaluateStep(TrainingStep):
    """Calcula pérdida, exactitud, clase mayoritaria y errores."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Evaluación del perceptrón"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Genera el reporte final a partir del modelo entrenado."""
        if context.XScaled is None or context.y is None or context.training is None:
            raise ValueError("EvaluateStep requiere XScaled, y y training (falta TrainPerceptronStep?)")

        weights = np.array(context.training.weights)
        bias = context.training.bias
        yProbability = PerceptronService.predictProbability(context.XScaled, weights, bias)
        predictions = (yProbability >= 0.5).astype(int)

        positiveCount = int(np.sum(context.y == 1))
        negativeCount = int(np.sum(context.y == 0))
        baselineAccuracy = max(positiveCount, negativeCount) / len(context.y)

        report = PerceptronReport(
            featureNames=context.featureNames,
            targetName=context.targetName,
            weights=context.training.weights,
            bias=bias,
            initialLoss=context.training.losses[0],
            finalLoss=PerceptronService.computeLoss(context.y, yProbability),
            initialAccuracy=context.training.accuracies[0],
            finalAccuracy=PerceptronService.computeAccuracy(context.y, yProbability),
            baselineAccuracy=float(baselineAccuracy),
            positiveCount=positiveCount,
            negativeCount=negativeCount,
            misclassifiedCount=int(np.sum(predictions != context.y)),
            losses=context.training.losses,
            accuracies=context.training.accuracies,
        )
        return replace(context, report=report)
