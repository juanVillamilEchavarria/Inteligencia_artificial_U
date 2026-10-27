"""Fachada para entrenar el perceptrón y clasificar recorridos nuevos."""

from typing import Iterable, List, Tuple

import numpy as np

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.PerceptronTrainingRunner import PerceptronTrainingRunner
from pipelines.train.dtos.PredictionResult import PredictionResult
from services.PerceptronService import PerceptronService


class PerceptronController:
    """Coordina el entrenamiento y las predicciones del perceptrón."""

    def __init__(self, runner: PerceptronTrainingRunner):
        """Recibe el runner que ejecuta el pipeline de entrenamiento."""
        self._runner = runner

    def train(self) -> PerceptronTrainingContext:
        """Ejecuta el pipeline y devuelve el contexto con el modelo entrenado."""
        return self._runner.run()

    def predictNewCases(
        self,
        context: PerceptronTrainingContext,
        cases: Iterable[Tuple[float, float]],
    ) -> List[PredictionResult]:
        """Clasifica casos nuevos usando la media y desviación del entrenamiento."""
        if context.report is None or context.means is None or context.stds is None:
            raise ValueError("El perceptrón debe entrenarse antes de predecir.")

        rawCases = np.array(list(cases), dtype=float)
        if rawCases.ndim != 2 or rawCases.shape[1] != 2:
            raise ValueError("Cada caso nuevo debe tener (toneladas, distancia).")

        XScaled = (rawCases - context.means) / context.stds
        weights = np.array(context.report.weights)
        probabilities = PerceptronService.predictProbability(
            XScaled, weights, context.report.bias
        )

        return [
            PredictionResult(
                toneladas=float(rawCase[0]),
                distancia=float(rawCase[1]),
                probability=float(probability),
                label=int(probability >= 0.5),
            )
            for rawCase, probability in zip(rawCases, probabilities)
        ]
