"""Paso que estandariza las variables de entrada."""

from dataclasses import replace

import numpy as np

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep


class StandardizeStep(TrainingStep):
    """Centra cada variable en 0 y la escala por su desviación estándar.

    La media y la desviación se calculan **solo con el conjunto de
    entrenamiento** para no filtrar información del conjunto de prueba.
    """

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Estandarización de entradas"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Calcula media y desviación de train y escala train y test."""
        if context.XTrain is None or context.XTest is None:
            raise ValueError(
                "StandardizeStep requiere XTrain y XTest (falta SplitDataStep?)"
            )

        means = context.XTrain.mean(axis=0)
        stds = context.XTrain.std(axis=0)
        if np.any(stds == 0):
            raise ValueError("No se puede estandarizar una variable con desviación estándar cero.")

        XScaledTrain = (context.XTrain - means) / stds
        XScaledTest = (context.XTest - means) / stds

        return replace(
            context,
            XScaled=XScaledTrain,
            XScaledTrain=XScaledTrain,
            XScaledTest=XScaledTest,
            means=means,
            stds=stds,
        )
