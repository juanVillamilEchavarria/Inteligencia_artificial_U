"""Entrenamiento y evaluación de modelos de clasificación con Scikit-Learn."""

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from dto.CandidateModel import CandidateModel
from pipelines.classification.dtos.ClassificationReport import ModelScore


class ClassificationService:
    """Construye, entrena y evalúa los tres modelos de la clase 12."""

    @staticmethod
    def build_candidate_models() -> Tuple[CandidateModel, ...]:
        """Crea los tres pipelines que se van a comparar.

        Cada pipeline escala las entradas antes de entregarlas al modelo.
        """
        return (
            CandidateModel(
                "Regresión logística",
                Pipeline(
                    [
                        ("escalado", StandardScaler()),
                        ("modelo", LogisticRegression()),
                    ]
                ),
            ),
            CandidateModel(
                "KNN (5 vecinos)",
                Pipeline(
                    [
                        ("escalado", StandardScaler()),
                        ("modelo", KNeighborsClassifier(n_neighbors=5)),
                    ]
                ),
            ),
            CandidateModel(
                "Árbol de decisión",
                Pipeline(
                    [
                        ("escalado", StandardScaler()),
                        (
                            "modelo",
                            DecisionTreeClassifier(max_depth=3, random_state=42),
                        ),
                    ]
                ),
            ),
        )

    @classmethod
    def evaluate_model(
        cls,
        candidate: CandidateModel,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        X_full: pd.DataFrame,
        y_full: pd.Series,
        cv: int = 5,
    ) -> ModelScore:
        """Entrena un candidato y calcula sus métricas sobre datos de prueba."""
        candidate.model.fit(X_train, y_train)
        predictions = candidate.model.predict(X_test)
        cross_validation = cross_val_score(
            candidate.model, X_full, y_full, cv=cv
        ).mean()

        return ModelScore(
            modelName=candidate.name,
            accuracy=float(accuracy_score(y_test, predictions)),
            precision=float(
                precision_score(y_test, predictions, zero_division=0)
            ),
            recall=float(recall_score(y_test, predictions, zero_division=0)),
            f1=float(f1_score(y_test, predictions, zero_division=0)),
            crossValidation=float(cross_validation),
        )

    @staticmethod
    def select_best_by_f1(scores: Tuple[ModelScore, ...]) -> str:
        """Devuelve el nombre del modelo con el F1 más alto."""
        if not scores:
            raise ValueError("No hay modelos evaluados para seleccionar.")
        best = max(scores, key=lambda score: score.f1)
        return best.modelName

    @staticmethod
    def confusion_matrix(
        model, X_test: pd.DataFrame, y_test: pd.Series
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Calcula la matriz de confusión del modelo ya entrenado."""
        matrix = confusion_matrix(y_test, model.predict(X_test))
        return tuple(tuple(int(value) for value in row) for row in matrix)

    @staticmethod
    def logistic_coefficients(model) -> Tuple[Tuple[float, ...], float]:
        """Extrae pesos y sesgo si el modelo interno es regresión logística."""
        inner_model = model.named_steps["modelo"]
        if not isinstance(inner_model, LogisticRegression):
            return (), 0.0
        weights = tuple(float(value) for value in inner_model.coef_[0])
        bias = float(inner_model.intercept_[0])
        return weights, bias

    @staticmethod
    def predict_probabilities(model, X: pd.DataFrame) -> np.ndarray:
        """Devuelve la probabilidad de que cada fila sea de la clase 1."""
        return model.predict_proba(X)[:, 1]
