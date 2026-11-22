"""Entrenamiento, optimización y evaluación de modelos con Scikit-Learn."""

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from dto.CandidateModel import CandidateModel
from pipelines.model.dtos.ModelScore import ModelScore

RANDOM_STATE = 42


class SklearnModelService:
    """Construye, optimiza, entrena y evalúa los modelos candidatos."""

    @staticmethod
    def buildCandidateModels() -> Tuple[CandidateModel, ...]:
        """Crea los tres pipelines que se van a comparar.

        Cada pipeline incluye su propio escalado para que la validación cruzada
        y la predicción de casos nuevos usen exactamente la misma transformación.
        """
        return (
            CandidateModel(
                "Regresión logística",
                Pipeline(
                    [
                        ("escalado", StandardScaler()),
                        (
                            "modelo",
                            LogisticRegression(
                                class_weight="balanced",
                                max_iter=1000,
                                random_state=RANDOM_STATE,
                            ),
                        ),
                    ]
                ),
            ),
            CandidateModel(
                "Random Forest",
                Pipeline(
                    [
                        (
                            "modelo",
                            RandomForestClassifier(
                                n_estimators=200,
                                class_weight="balanced",
                                random_state=RANDOM_STATE,
                            ),
                        ),
                    ]
                ),
            ),
            CandidateModel(
                "Red neuronal (MLP)",
                Pipeline(
                    [
                        ("escalado", StandardScaler()),
                        (
                            "modelo",
                            MLPClassifier(
                                hidden_layer_sizes=(16, 8),
                                activation="relu",
                                solver="lbfgs",
                                alpha=1e-3,
                                max_iter=3000,
                                random_state=RANDOM_STATE,
                            ),
                        ),
                    ]
                ),
            ),
        )

    @staticmethod
    def tuneRandomForest(
        candidate: CandidateModel,
        XTrain: pd.DataFrame,
        yTrain: pd.Series,
        cv: Any,
    ) -> Tuple[CandidateModel, Dict[str, Any], float]:
        """Optimiza los hiperparámetros del Random Forest con GridSearchCV.

        Returns:
            El candidato ya optimizado, los mejores hiperparámetros y el mejor
            F1 macro promedio de la búsqueda.
        """
        search = GridSearchCV(
            estimator=candidate.model,
            param_grid={
                "modelo__n_estimators": [100, 200],
                "modelo__max_depth": [None, 3, 5],
                "modelo__min_samples_leaf": [1, 2],
            },
            scoring="f1_macro",
            cv=cv,
            n_jobs=-1,
            refit=True,
        )
        search.fit(XTrain, yTrain)

        tuned = CandidateModel(
            "Random Forest (GridSearchCV)",
            search.best_estimator_,
        )
        return tuned, dict(search.best_params_), float(search.best_score_)

    @classmethod
    def evaluateModel(
        cls,
        candidate: CandidateModel,
        XTrain: pd.DataFrame,
        yTrain: pd.Series,
        XTest: pd.DataFrame,
        yTest: pd.Series,
        cv: Any,
        bestParams: str = "",
    ) -> ModelScore:
        """Entrena un candidato y calcula sus métricas de prueba y validación."""
        candidate.model.fit(XTrain, yTrain)
        predictions = candidate.model.predict(XTest)
        probabilities = cls.predictProbabilities(candidate.model, XTest)

        try:
            rocAuc = float(roc_auc_score(yTest, probabilities))
        except ValueError:
            rocAuc = 0.0

        cvScores = cross_val_score(
            candidate.model,
            XTrain,
            yTrain,
            cv=cv,
            scoring="f1_macro",
        )

        matrix = confusion_matrix(yTest, predictions, labels=[0, 1])

        return ModelScore(
            modelName=candidate.name,
            accuracy=float(accuracy_score(yTest, predictions)),
            precision=float(
                precision_score(yTest, predictions, pos_label=1, zero_division=0)
            ),
            recall=float(
                recall_score(yTest, predictions, pos_label=1, zero_division=0)
            ),
            f1Macro=float(
                f1_score(yTest, predictions, average="macro", zero_division=0)
            ),
            f1Class1=float(
                f1_score(yTest, predictions, pos_label=1, zero_division=0)
            ),
            rocAuc=rocAuc,
            crossValidationMean=float(np.mean(cvScores)),
            crossValidationStd=float(np.std(cvScores)),
            confusionMatrix=tuple(
                tuple(int(value) for value in row) for row in matrix
            ),
            bestParams=bestParams,
        )

    @staticmethod
    def selectBestScore(scores: Tuple[ModelScore, ...]) -> ModelScore:
        """Selecciona el modelo con mejor F1 macro de validación cruzada.

        Se usa la validación cruzada y no el conjunto de prueba para evitar
        elegir el modelo con base en los datos que después se reportan.
        """
        if not scores:
            raise ValueError("No hay modelos evaluados para seleccionar.")
        return max(
            scores,
            key=lambda score: (score.crossValidationMean, score.f1Macro),
        )

    @staticmethod
    def predictProbabilities(model: Any, X: pd.DataFrame) -> np.ndarray:
        """Devuelve la probabilidad de que cada fila sea de la clase 1."""
        return model.predict_proba(X)[:, 1]

    @staticmethod
    def describeModel(model: Any, featureNames: Tuple[str, ...]) -> Dict[str, float]:
        """Resume el peso de cada variable para explicar el modelo por dentro.

        Devuelve importancias si el modelo es un árbol y coeficientes si es
        lineal. Para el MLP no hay una lectura directa, así que devuelve vacío.
        """
        inner = model.named_steps.get("modelo", model)
        if hasattr(inner, "feature_importances_"):
            values = inner.feature_importances_
        elif hasattr(inner, "coef_"):
            values = np.ravel(inner.coef_)
        else:
            return {}
        return {
            name: float(value)
            for name, value in zip(featureNames, values)
        }
