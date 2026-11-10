"""Gráfico de la matriz de confusión con Matplotlib."""

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from helpers.project_paths import CONFUSION_MATRIX_PATH


class ClassificationChartRenderer:
    """Dibuja la matriz de confusión del mejor clasificador."""

    def generateConfusionMatrix(
        self,
        matrix: Sequence[Sequence[int]],
        modelName: str,
        outputPath: Path = CONFUSION_MATRIX_PATH,
    ) -> str:
        """Guarda la matriz como una imagen PNG y devuelve su ruta."""
        outputPath = Path(outputPath)
        outputPath.parent.mkdir(parents=True, exist_ok=True)

        values = np.array(matrix)
        figure, axis = plt.subplots(figsize=(6, 5))
        image = axis.imshow(values, cmap="Blues")

        axis.set_xticks([0, 1])
        axis.set_xticklabels(["Predijo 0", "Predijo 1"])
        axis.set_yticks([0, 1])
        axis.set_yticklabels(["Real 0", "Real 1"])

        for row in range(values.shape[0]):
            for column in range(values.shape[1]):
                axis.text(
                    column,
                    row,
                    str(int(values[row, column])),
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=14,
                )

        axis.set_title(f"Matriz de confusión – {modelName}")
        figure.colorbar(image, ax=axis, shrink=0.8)
        figure.tight_layout()
        figure.savefig(outputPath, dpi=150, bbox_inches="tight")
        plt.close(figure)
        return str(outputPath)
