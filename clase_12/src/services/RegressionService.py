"""Entrenamiento y evaluación de la regresión lineal."""

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from pipelines.regression.dtos.RegressionReport import RegressionReport


class RegressionService:
    """Encapsula el modelo, las predicciones y las métricas de regresión."""

    @staticmethod
    def build_model() -> Pipeline:
        """Crea el pipeline de escalado más regresión lineal."""
        return Pipeline(
            [
                ("escalado", StandardScaler()),
                ("modelo", LinearRegression()),
            ]
        )

    @staticmethod
    def train(model, X_train: pd.DataFrame, y_train: pd.Series):
        """Entrena el modelo y lo devuelve."""
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def predict(model, X: pd.DataFrame) -> np.ndarray:
        """Predice el rendimiento para cada fila de entrada."""
        return model.predict(X)

    @staticmethod
    def build_report(
        model,
        y_test: pd.Series,
        y_predicted: np.ndarray,
        feature_names: Tuple[str, ...],
        train_count: int,
        test_count: int,
        average_yield: float,
    ) -> RegressionReport:
        """Calcula MAE, RMSE y R², y extrae los coeficientes del modelo."""
        mae = mean_absolute_error(y_test, y_predicted)
        rmse = np.sqrt(mean_squared_error(y_test, y_predicted))
        r2 = r2_score(y_test, y_predicted)

        inner_model = model.named_steps["modelo"]
        coefficients = tuple(float(value) for value in inner_model.coef_)
        intercept = float(inner_model.intercept_)

        return RegressionReport(
            mae=float(mae),
            rmse=float(rmse),
            r2=float(r2),
            coefficients=coefficients,
            intercept=intercept,
            featureNames=feature_names,
            trainCount=train_count,
            testCount=test_count,
            averageYield=float(average_yield),
        )
