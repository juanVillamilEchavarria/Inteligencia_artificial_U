"""Paso que calcula las métricas finales del modelo."""

from dataclasses import replace

import numpy as np

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.dtos.PerceptronReport import PerceptronReport
from pipelines.train.steps.TrainingStep import TrainingStep
from services.PerceptronService import PerceptronService


class EvaluateStep(TrainingStep):
    """Calcula pérdida, exactitud y la referencia de clase mayoritaria."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Evaluación del perceptrón"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Genera el reporte final a partir del modelo entrenado."""
        if (
            context.XScaledTrain is None
            or context.XScaledTest is None
            or context.yTrain is None
            or context.yTest is None
            or context.training is None
        ):
            raise ValueError(
                "EvaluateStep requiere train/test y training (falta TrainPerceptronStep?)"
            )

        weights = np.array(context.training.weights)
        bias = context.training.bias

        trainProbability = PerceptronService.predictProbability(
            context.XScaledTrain, weights, bias
        )
        testProbability = PerceptronService.predictProbability(
            context.XScaledTest, weights, bias
        )

        positiveCount = int(np.sum(context.yTrain == 1))
        negativeCount = int(np.sum(context.yTrain == 0))
        positiveTest = int(np.sum(context.yTest == 1))
        negativeTest = int(np.sum(context.yTest == 0))
        testBaseline = max(positiveTest, negativeTest) / len(context.yTest)

        report = PerceptronReport(
            featureNames=context.featureNames,
            targetName=context.targetName,
            weights=context.training.weights,
            bias=bias,
            initialLoss=context.training.losses[0],
            finalLoss=PerceptronService.computeLoss(context.yTrain, trainProbability),
            initialAccuracy=context.training.accuracies[0],
            finalAccuracy=PerceptronService.computeAccuracy(context.yTrain, trainProbability),
            baselineAccuracy=float(testBaseline),
            positiveCount=positiveCount,
            negativeCount=negativeCount,
            losses=context.training.losses,
            accuracies=context.training.accuracies,
            testLoss=PerceptronService.computeLoss(context.yTest, testProbability),
            testAccuracy=PerceptronService.computeAccuracy(context.yTest, testProbability),
            trainCount=len(context.yTrain),
            testCount=len(context.yTest),
        )
        return replace(context, report=report)
