"""Fachada para entrenar y usar el modelo de clasificación."""

from typing import Iterable, List, Tuple

import pandas as pd

from dto.PredictionResult import PredictionResult
from enums.CropColumns import CropColumns
from pipelines.classification.ClassificationContext import ClassificationContext
from pipelines.classification.ClassificationRunner import ClassificationRunner
from pipelines.transform.DataPreparationContext import DataPreparationContext
from services.ClassificationService import ClassificationService
from services.ModelPersistenceService import ModelPersistenceService


class ClassificationController:
    """Coordina el entrenamiento y las predicciones del clasificador."""

    def __init__(
        self,
        runner: ClassificationRunner,
        storage: ModelPersistenceService,
        featureNames: Tuple[str, ...] = (
            CropColumns.PRECIPITACION_MM.value,
            CropColumns.TEMPERATURA_C.value,
        ),
    ):
        """Recibe el runner del pipeline, el almacenamiento y las entradas."""
        self._runner = runner
        self._storage = storage
        self._featureNames = tuple(featureNames)

    def train(
        self, preparedData: DataPreparationContext
    ) -> ClassificationContext:
        """Ejecuta la comparación de modelos y devuelve el contexto."""
        return self._runner.run(preparedData)

    def loadModel(self):
        """Carga el modelo guardado desde disco."""
        return self._storage.load()

    def predictNewCases(
        self,
        cases: Iterable[Tuple[float, float]],
    ) -> List[PredictionResult]:
        """Clasifica casos nuevos usando el modelo guardado.

        Args:
            cases: Pares ``(precipitacion_mm, temperatura_c)``.

        Returns:
            Una predicción por cada caso, con su probabilidad de éxito.
        """
        rows = list(cases)
        if not rows:
            return []

        model = self.loadModel()
        X = pd.DataFrame(rows, columns=list(self._featureNames))
        probabilities = ClassificationService.predict_probabilities(model, X)
        labels = model.predict(X)

        return [
            PredictionResult(
                precipitacion_mm=float(row[0]),
                temperatura_c=float(row[1]),
                probability=float(probability),
                label=int(label),
            )
            for row, probability, label in zip(rows, probabilities, labels)
        ]
