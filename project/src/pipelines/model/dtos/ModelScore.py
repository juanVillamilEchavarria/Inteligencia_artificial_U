"""Métricas obtenidas por un modelo candidato."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ModelScore:
    """Resultados de entrenar y evaluar un modelo.

    Attributes:
        modelName: Nombre del modelo evaluado.
        accuracy: Proporción total de aciertos en prueba.
        precision: Aciertos de la clase 1 sobre lo que el modelo llamó 1.
        recall: Casos reales de clase 1 que el modelo encontró.
        f1Macro: Media armónica de precisión y recall promediada por clase.
        f1Class1: F1 de la clase minoritaria (Ingreso).
        rocAuc: Área bajo la curva ROC en prueba.
        crossValidationMean: Promedio de F1 macro en validación cruzada.
        crossValidationStd: Desviación estándar de la validación cruzada.
        confusionMatrix: Matriz 2x2 (filas = real, columnas = predicción).
        bestParams: Hiperparámetros elegidos, si aplica.
    """

    modelName: str
    accuracy: float
    precision: float
    recall: float
    f1Macro: float
    f1Class1: float
    rocAuc: float
    crossValidationMean: float
    crossValidationStd: float
    confusionMatrix: Tuple[Tuple[int, int], Tuple[int, int]]
    bestParams: str = ""
