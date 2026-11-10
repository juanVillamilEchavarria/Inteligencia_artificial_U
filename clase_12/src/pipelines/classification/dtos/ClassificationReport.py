"""Reportes del pipeline de clasificación."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ModelScore:
    """Métricas obtenidas por un modelo candidato.

    Attributes:
        modelName: Nombre del modelo evaluado.
        accuracy: Proporción total de aciertos.
        precision: Aciertos de la clase 1 sobre lo que el modelo llamó 1.
        recall: Casos reales de clase 1 que el modelo encontró.
        f1: Media armónica entre precisión y recall.
        crossValidation: Promedio de la validación cruzada de 5 pliegues.
    """

    modelName: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    crossValidation: float


@dataclass(frozen=True)
class ClassificationReport:
    """Resultado final de comparar y seleccionar modelos.

    Attributes:
        scores: Métricas de cada modelo candidato.
        bestModelName: Nombre del modelo con el F1 más alto.
        confusionMatrix: Matriz 2x2 del mejor modelo sobre los datos de prueba.
        weights: Pesos aprendidos si el mejor modelo es regresión logística.
        bias: Sesgo aprendido si el mejor modelo es regresión logística.
        featureNames: Variables usadas como entrada.
        targetName: Variable que se intenta predecir.
        trainCount: Cantidad de lotes de entrenamiento.
        testCount: Cantidad de lotes de prueba.
        modelPath: Ruta donde quedó guardado el modelo.
    """

    scores: Tuple[ModelScore, ...]
    bestModelName: str
    confusionMatrix: Tuple[Tuple[int, int], Tuple[int, int]]
    weights: Tuple[float, ...] = ()
    bias: float = 0.0
    featureNames: Tuple[str, ...] = ()
    targetName: str = ""
    trainCount: int = 0
    testCount: int = 0
    modelPath: str = ""
