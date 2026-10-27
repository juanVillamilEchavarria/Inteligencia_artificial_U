"""Gráficos exploratorios del dataset limpio usando Seaborn."""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from helpers.project_paths import SEABORN_CHARTS_DIR


class SeabornChartRenderer:
    """Genera y guarda los gráficos del análisis exploratorio."""

    TARGET = "ruta_retrasada"

    def __init__(self, dfClean: pd.DataFrame, chartsDir: str = None):
        """Recibe el dataframe limpio y la carpeta de salida."""
        self.dfClean = dfClean
        self.chartsDir = chartsDir or f"{SEABORN_CHARTS_DIR}/"

    def _ensureDir(self):
        """Crea la carpeta de gráficos si todavía no existe."""
        os.makedirs(self.chartsDir, exist_ok=True)

    def _save(self, filepath: str) -> str:
        """Ajusta la figura, la guarda y cierra el gráfico."""
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        return filepath

    def generateScatterFeaturesTarget(
        self, filename: str = "seaborn_scatter_features_target.png"
    ) -> str:
        """Dispersión de toneladas contra distancia coloreada por la clase."""
        self._ensureDir()
        df = self.dfClean

        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df,
            x="toneladas_recogidas",
            y="distancia_km",
            hue=self.TARGET,
            palette={0: "tomato", 1: "seagreen"},
            s=90,
            edgecolor="black",
            alpha=0.85,
        )
        plt.xlabel("Toneladas recogidas", fontsize=12)
        plt.ylabel("Distancia recorrida (km)", fontsize=12)
        plt.title("Toneladas vs distancia por estado de la ruta - Grupo 07", fontsize=14)
        plt.legend(title="ruta_retrasada (0 = a tiempo, 1 = retraso)", fontsize=10)
        plt.grid(alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateBoxplotDistanceByTarget(
        self, filename: str = "seaborn_boxplot_distancia_objetivo.png"
    ) -> str:
        """Boxplot de la distancia recorrida para cada clase."""
        self._ensureDir()
        df = self.dfClean

        plt.figure(figsize=(9, 6))
        sns.boxplot(
            data=df,
            x=self.TARGET,
            y="distancia_km",
            hue=self.TARGET,
            palette={0: "tomato", 1: "seagreen"},
            legend=False,
            width=0.5,
        )
        plt.xticks([0, 1], ["A tiempo (0)", "Retraso (1)"])
        plt.xlabel("Estado de la ruta", fontsize=12)
        plt.ylabel("Distancia recorrida (km)", fontsize=12)
        plt.title("Distancia recorrida por estado de la ruta - Grupo 07", fontsize=14)
        plt.grid(axis="y", alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateAll(self) -> list:
        """Genera ambos gráficos y devuelve sus rutas."""
        return [
            self.generateScatterFeaturesTarget(),
            self.generateBoxplotDistanceByTarget(),
        ]
