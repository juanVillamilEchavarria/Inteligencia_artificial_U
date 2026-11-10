"""Gráfico del sobreajuste de árboles de decisión."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from helpers.project_paths import OVERFITTING_PLOT_PATH
from pipelines.overfitting.dtos.OverfittingReport import OverfittingReport


class OverfittingChartRenderer:
    """Dibuja exactitud de entrenamiento y prueba por profundidad."""

    def generateOverfittingPlot(
        self,
        report: OverfittingReport,
        outputPath: Path = OVERFITTING_PLOT_PATH,
    ) -> str:
        """Guarda el gráfico de sobreajuste y devuelve su ruta."""
        outputPath = Path(outputPath)
        outputPath.parent.mkdir(parents=True, exist_ok=True)

        depths = [score.depth for score in report.scores]
        trainAccuracies = [score.trainAccuracy for score in report.scores]
        testAccuracies = [score.testAccuracy for score in report.scores]

        figure, axis = plt.subplots(figsize=(8, 5))
        axis.plot(
            depths,
            trainAccuracies,
            marker="o",
            label="Entrenamiento",
        )
        axis.plot(
            depths,
            testAccuracies,
            marker="s",
            label="Prueba",
        )
        axis.set_title("Sobreajuste: exactitud según la profundidad del árbol")
        axis.set_xlabel("Profundidad del árbol (max_depth)")
        axis.set_ylabel("Exactitud")
        axis.legend()
        axis.grid(True, alpha=0.3)
        figure.tight_layout()
        figure.savefig(outputPath, dpi=150, bbox_inches="tight")
        plt.close(figure)
        return str(outputPath)
