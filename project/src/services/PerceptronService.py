"""Operaciones matemáticas del perceptrón implementadas con NumPy."""

from typing import Tuple

import numpy as np

from dto.PerceptronTrainingDTO import PerceptronTrainingDTO


class PerceptronService:
    """Entrena un perceptrón simple y calcula sus predicciones y métricas."""

    EPSILON = 1e-9

    @staticmethod
    def sigmoid(z: np.ndarray) -> np.ndarray:
        """Aplica la función sigmoide para obtener probabilidades entre 0 y 1."""
        return 1.0 / (1.0 + np.exp(-z))

    @staticmethod
    def weightedSum(X: np.ndarray, weights: np.ndarray, bias: float) -> np.ndarray:
        """Calcula la combinación lineal entre las entradas, los pesos y el sesgo."""
        return X @ weights + bias

    @classmethod
    def predictProbability(cls, X: np.ndarray, weights: np.ndarray, bias: float) -> np.ndarray:
        """Devuelve la probabilidad de que cada fila pertenezca a la clase 1."""
        return cls.sigmoid(cls.weightedSum(X, weights, bias))

    @classmethod
    def computeLoss(cls, yTrue: np.ndarray, yProbability: np.ndarray) -> float:
        """Calcula la pérdida logarítmica promedio.

        Las probabilidades se recortan para evitar logaritmos de cero.
        """
        yProbability = np.clip(yProbability, cls.EPSILON, 1.0 - cls.EPSILON)
        return float(-np.mean(yTrue * np.log(yProbability) + (1 - yTrue) * np.log(1 - yProbability)))

    @staticmethod
    def computeAccuracy(yTrue: np.ndarray, yProbability: np.ndarray) -> float:
        """Calcula la proporción de aciertos usando un umbral de 0.5."""
        predictions = (yProbability >= 0.5).astype(int)
        return float(np.mean(predictions == yTrue))

    @staticmethod
    def computeGradients(
        X: np.ndarray,
        yTrue: np.ndarray,
        yProbability: np.ndarray,
    ) -> Tuple[np.ndarray, float]:
        """Calcula los gradientes de los pesos y del sesgo."""
        error = yProbability - yTrue
        gradientWeights = (X.T @ error) / len(yTrue)
        gradientBias = float(np.mean(error))
        return gradientWeights, gradientBias

    @classmethod
    def train(
        cls,
        X: np.ndarray,
        y: np.ndarray,
        learningRate: float = 0.1,
        epochs: int = 500,
    ) -> PerceptronTrainingDTO:
        """Entrena el perceptrón con descenso de gradiente.

        Args:
            X: Matriz de entradas ya estandarizadas.
            y: Etiquetas binarias de cada fila.
            learningRate: Tamaño del paso del descenso de gradiente.
            epochs: Número de iteraciones sobre el conjunto completo.

        Returns:
            Los pesos, el sesgo y el historial de pérdida y exactitud.

        Raises:
            ValueError: Si las dimensiones no coinciden o los parámetros no son válidos.
        """
        if X.ndim != 2:
            raise ValueError("X debe ser una matriz bidimensional.")
        if len(X) == 0 or len(X) != len(y):
            raise ValueError("X y y deben tener la misma cantidad de filas y no estar vacíos.")
        if epochs <= 0:
            raise ValueError("epochs debe ser mayor que cero.")
        if learningRate <= 0:
            raise ValueError("learningRate debe ser mayor que cero.")

        weights = np.zeros(X.shape[1])
        bias = 0.0
        losses = []
        accuracies = []

        for _ in range(epochs):
            yProbability = cls.predictProbability(X, weights, bias)
            losses.append(cls.computeLoss(y, yProbability))
            accuracies.append(cls.computeAccuracy(y, yProbability))

            gradientWeights, gradientBias = cls.computeGradients(X, y, yProbability)
            weights = weights - learningRate * gradientWeights
            bias = bias - learningRate * gradientBias

        return PerceptronTrainingDTO(
            weights=tuple(float(value) for value in weights),
            bias=float(bias),
            losses=tuple(losses),
            accuracies=tuple(accuracies),
        )
