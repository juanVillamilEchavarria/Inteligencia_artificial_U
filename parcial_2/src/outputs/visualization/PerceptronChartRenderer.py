"""Gráficos del entrenamiento y de la frontera de decisión del perceptrón."""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from helpers.project_paths import PERCEPTRON_CHARTS_DIR
from pipelines.train.dtos.PerceptronReport import PerceptronReport


class PerceptronChartRenderer:
    """Dibuja las curvas de aprendizaje y la separación de las clases."""

    def __init__(
        self,
        dfPrepared: pd.DataFrame,
        report: PerceptronReport,
        means: np.ndarray,
        stds: np.ndarray,
        chartsDir: str = None,
    ):
        """Recibe los datos, el modelo entrenado y la carpeta de salida."""
        self.dfPrepared = dfPrepared
        self.report = report
        self.means = means
        self.stds = stds
        self.chartsDir = chartsDir or f"{PERCEPTRON_CHARTS_DIR}/"

    def _ensureDir(self):
        """Crea la carpeta de gráficos si todavía no existe."""
        os.makedirs(self.chartsDir, exist_ok=True)

    def _save(self, filepath: str) -> str:
        """Ajusta la figura, la guarda y cierra el gráfico."""
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        return filepath

    def generateLearningCurve(self, filename: str = "curva_aprendizaje.png") -> str:
        """Grafica la pérdida y la exactitud por época."""
        self._ensureDir()

        figure, (lossAxis, accuracyAxis) = plt.subplots(1, 2, figsize=(12, 4.5))
        lossAxis.plot(self.report.losses, color="red")
        lossAxis.set_title("Pérdida por época")
        lossAxis.set_xlabel("Época")
        lossAxis.set_ylabel("Pérdida logarítmica")
        lossAxis.grid(True, alpha=0.3)

        accuracyAxis.plot(self.report.accuracies, color="green")
        accuracyAxis.set_title("Exactitud por época")
        accuracyAxis.set_xlabel("Época")
        accuracyAxis.set_ylabel("Exactitud")
        accuracyAxis.set_ylim(0, 1.05)
        accuracyAxis.grid(True, alpha=0.3)

        return self._save(f"{self.chartsDir}{filename}")

    def generateDecisionBoundary(self, filename: str = "frontera_decision.png") -> str:
        """Grafica los puntos y la recta que separa retrasos de rutas a tiempo."""
        self._ensureDir()

        df = self.dfPrepared
        firstFeature, secondFeature = self.report.featureNames
        firstValues = df[firstFeature].to_numpy(dtype=float)
        secondValues = df[secondFeature].to_numpy(dtype=float)

        x1Original = np.linspace(firstValues.min(), firstValues.max(), 200)
        x1Scaled = (x1Original - self.means[0]) / self.stds[0]
        x2Scaled = (
            -(self.report.weights[0] * x1Scaled + self.report.bias)
            / self.report.weights[1]
        )
        x2Original = x2Scaled * self.stds[1] + self.means[1]

        plt.figure(figsize=(10, 6))
        plt.scatter(
            firstValues[df[self.report.targetName] == 1],
            secondValues[df[self.report.targetName] == 1],
            color="seagreen",
            edgecolors="black",
            label="Retraso (1)",
        )
        plt.scatter(
            firstValues[df[self.report.targetName] == 0],
            secondValues[df[self.report.targetName] == 0],
            color="tomato",
            marker="s",
            edgecolors="black",
            label="A tiempo (0)",
        )
        plt.plot(x1Original, x2Original, color="blue", linewidth=2.5, label="Frontera de decisión")
        plt.xlabel("Toneladas recogidas", fontsize=12)
        plt.ylabel("Distancia recorrida (km)", fontsize=12)
        plt.title("Frontera de decisión del perceptrón - Rutas de recolección", fontsize=14)
        plt.legend()
        plt.grid(alpha=0.3)

        return self._save(f"{self.chartsDir}{filename}")

    def generateAll(self) -> list:
        """Genera ambos gráficos y devuelve sus rutas."""
        return [
            self.generateLearningCurve(),
            self.generateDecisionBoundary(),
        ]
