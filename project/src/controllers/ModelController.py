"""Fachada para entrenar y usar el modelo de Scikit-Learn."""

from typing import Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from helpers.project_paths import MODEL_METRICS_PATH, MODEL_PATH
from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.ModelTrainingRunner import ModelTrainingRunner
from pipelines.model.dtos.ModelPredictionResult import ModelPredictionResult
from services.ModelPersistenceService import ModelPersistenceService
from services.SklearnModelService import SklearnModelService


class ModelController:
    """Coordina el entrenamiento, la carga y las predicciones del modelo."""

    def __init__(
        self,
        runner: Optional[ModelTrainingRunner] = None,
        storage: Optional[ModelPersistenceService] = None,
    ):
        """Recibe el runner del pipeline y el almacenamiento del modelo."""
        self._runner = runner
        self._storage = storage or ModelPersistenceService(MODEL_PATH, MODEL_METRICS_PATH)

    def train(self) -> ModelTrainingContext:
        """Ejecuta la comparación de modelos y devuelve el contexto."""
        if self._runner is None:
            raise ValueError("Este controlador no tiene un runner de entrenamiento.")
        return self._runner.run()

    def loadModel(self) -> dict:
        """Carga el payload guardado con el modelo y su metadata."""
        return self._storage.load()

    def loadMetrics(self) -> dict:
        """Carga las métricas legibles guardadas en JSON."""
        return self._storage.loadMetrics()

    def predictNewCases(
        self,
        cases: Iterable[Tuple[float, int, int]],
    ) -> List[ModelPredictionResult]:
        """Clasifica casos nuevos usando el modelo guardado.

        Args:
            cases: Tuplas ``(monto, mes, dia_semana)`` en unidades originales.
                ``dia_semana`` usa 0 = lunes y 6 = domingo.

        Returns:
            Una predicción por caso, con la probabilidad de ser ingreso.
        """
        rows = list(cases)
        if not rows:
            return []

        payload = self.loadModel()
        model = payload["model"]
        featureNames = list(payload["featureNames"])

        preparedRows = []
        for monto, mes, diaSemana in rows:
            if monto <= 0:
                raise ValueError("El monto debe ser mayor que cero.")
            if not 1 <= int(mes) <= 12:
                raise ValueError("El mes debe estar entre 1 y 12.")
            if not 0 <= int(diaSemana) <= 6:
                raise ValueError("El día de la semana debe estar entre 0 y 6.")
            preparedRows.append(
                {
                    "monto_log": float(np.log1p(monto)),
                    "mes": int(mes),
                    "dia_semana": int(diaSemana),
                    "es_fin_semana": int(int(diaSemana) >= 5),
                }
            )

        X = pd.DataFrame(preparedRows, columns=featureNames)
        probabilities = SklearnModelService.predictProbabilities(model, X)
        labels = model.predict(X)

        return [
            ModelPredictionResult(
                monto=float(row[0]),
                mes=int(row[1]),
                diaSemana=int(row[2]),
                probability=float(probability),
                label=int(label),
            )
            for row, probability, label in zip(rows, probabilities, labels)
        ]
