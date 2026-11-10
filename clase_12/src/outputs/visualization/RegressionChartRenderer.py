"""Gráfico de valores reales contra valores predichos."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from helpers.project_paths import REGRESSION_PLOT_PATH


class RegressionChartRenderer:
    """Dibuja la comparación entre rendimiento real y predicho."""

    def generateRealVsPredicted(
        self,
        yTrue,
        yPredicted,
        r2: float,
        outputPath: Path = REGRESSION_PLOT_PATH,
    ) -> str:
        """Guarda el gráfico real vs. predicho y devuelve su ruta."""
        outputPath = Path(outputPath)
        outputPath.parent.mkdir(parents=True, exist_ok=True)

        trueValues = np.asarray(yTrue, dtype=float)
        predictedValues = np.asarray(yPredicted, dtype=float)

        figure, axis = plt.subplots(figsize=(7, 6))
        axis.scatter(
            trueValues,
            predictedValues,
            color="teal",
            edgecolors="black",
            alpha=0.8,
            label="Lotes de prueba",
        )

        minimum = min(trueValues.min(), predictedValues.min())
        maximum = max(trueValues.max(), predictedValues.max())
        axis.plot(
            [minimum, maximum],
            [minimum, maximum],
            color="red",
            linestyle="--",
            label="Predicción perfecta",
        )

        axis.set_title(f"Regresión lineal: real vs. predicho (R² = {r2:.2f})")
        axis.set_xlabel("Rendimiento real (kg/ha)")
        axis.set_ylabel("Rendimiento predicho (kg/ha)")
        axis.legend()
        axis.grid(True, alpha=0.3)
        figure.tight_layout()
        figure.savefig(outputPath, dpi=150, bbox_inches="tight")
        plt.close(figure)
        return str(outputPath)
