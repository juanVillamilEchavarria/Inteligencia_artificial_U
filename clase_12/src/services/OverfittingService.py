"""Entrenamiento de árboles con distintas profundidades."""

from typing import Tuple

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from pipelines.overfitting.dtos.OverfittingReport import DepthScore


class OverfittingService:
    """Mide cómo cambia la exactitud al aumentar la profundidad del árbol."""

    @staticmethod
    def train_depths(
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        max_depth: int = 12,
    ) -> Tuple[DepthScore, ...]:
        """Entrena un árbol por cada profundidad entre 1 y ``max_depth``."""
        scores = []
        for depth in range(1, max_depth + 1):
            tree = DecisionTreeClassifier(max_depth=depth, random_state=42)
            tree.fit(X_train, y_train)
            scores.append(
                DepthScore(
                    depth=depth,
                    trainAccuracy=float(tree.score(X_train, y_train)),
                    testAccuracy=float(tree.score(X_test, y_test)),
                )
            )
        return tuple(scores)
