"""Paso que estandariza las variables de entrada."""

from dataclasses import replace

import numpy as np

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep


class StandardizeStep(TrainingStep):
    """Centra cada variable en 0 y la escala por su desviación estándar."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Estandarización de entradas"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Calcula media y desviación, y guarda ambas para predecir casos nuevos."""
        if context.X is None:
            raise ValueError("StandardizeStep requiere X (falta SelectFeaturesStep?)")

        means = context.X.mean(axis=0)
        stds = context.X.std(axis=0)
        if np.any(stds == 0):
            raise ValueError("No se puede estandarizar una variable con desviación estándar cero.")

        XScaled = (context.X - means) / stds
        return replace(context, XScaled=XScaled, means=means, stds=stds)
