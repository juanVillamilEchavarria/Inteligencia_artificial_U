"""Gráficos de evaluación del mejor modelo de Scikit-Learn."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import roc_auc_score, roc_curve

from helpers.project_paths import MODEL_CHARTS_DIR
from pipelines.model.ModelTrainingContext import ModelTrainingContext


class EvaluationChartRenderer:
    """Genera la matriz de confusión y los gráficos comparativos."""

    def __init__(
        self,
        context: ModelTrainingContext,
        chartsDir: str = None,
    ):
        """Recibe el contexto entrenado y la carpeta de salida."""
        self.context = context
        self.chartsDir = chartsDir or f"{MODEL_CHARTS_DIR}/"

    def _ensureDir(self):
        """Crea la carpeta de gráficos si todavía no existe."""
        os.makedirs(self.chartsDir, exist_ok=True)

    def _save(self, filepath: str) -> str:
        """Ajusta la figura, la guarda y cierra el gráfico."""
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close()
        return filepath

    def _requireReport(self):
        if self.context.report is None:
            raise ValueError("El contexto no tiene reporte de modelos.")

    def generateConfusionMatrix(self, filename: str = "matriz_confusion.png") -> str:
        """Dibuja la matriz de confusión del mejor modelo."""
        self._requireReport()
        self._ensureDir()

        matrix = np.array(self.context.report.bestConfusionMatrix)
        plt.figure(figsize=(7, 5.5))
        sns.heatmap(
            matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            xticklabels=["Gasto (0)", "Ingreso (1)"],
            yticklabels=["Gasto (0)", "Ingreso (1)"],
        )
        plt.xlabel("Predicción del modelo", fontsize=12)
        plt.ylabel("Valor real", fontsize=12)
        plt.title(
            f"Matriz de confusión - {self.context.report.bestModelName}",
            fontsize=13,
        )
        return self._save(f"{self.chartsDir}{filename}")

    def generateRealVsPredicted(self, filename: str = "real_vs_predicho.png") -> str:
        """Compara la cantidad de gastos e ingresos reales y predichos."""
        if (
            self.context.bestModel is None
            or self.context.XTest is None
            or self.context.yTest is None
        ):
            raise ValueError("Faltan el modelo o los datos de prueba.")
        self._ensureDir()

        predictions = self.context.bestModel.predict(self.context.XTest)
        real = self.context.yTest.to_numpy()
        counts = pd.DataFrame(
            {
                "Clase": ["Gasto", "Ingreso", "Gasto", "Ingreso"],
                "Serie": ["Real", "Real", "Predicho", "Predicho"],
                "Cantidad": [
                    int((real == 0).sum()),
                    int((real == 1).sum()),
                    int((predictions == 0).sum()),
                    int((predictions == 1).sum()),
                ],
            }
        )

        plt.figure(figsize=(9, 5.5))
        sns.barplot(
            data=counts,
            x="Clase",
            y="Cantidad",
            hue="Serie",
            palette={"Real": "steelblue", "Predicho": "seagreen"},
        )
        plt.xlabel("Clase", fontsize=12)
        plt.ylabel("Cantidad de transacciones", fontsize=12)
        plt.title("Real vs predicho en el conjunto de prueba", fontsize=13)
        plt.grid(axis="y", alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateModelComparison(self, filename: str = "comparacion_modelos.png") -> str:
        """Grafica el F1 macro de prueba y de validación cruzada por modelo."""
        self._requireReport()
        self._ensureDir()

        table = pd.DataFrame(
            [
                {
                    "Modelo": score.modelName,
                    "F1 macro (prueba)": score.f1Macro,
                    "F1 macro (validación cruzada)": score.crossValidationMean,
                }
                for score in self.context.report.scores
            ]
        )
        melted = table.melt(
            id_vars="Modelo",
            var_name="Métrica",
            value_name="Valor",
        )

        plt.figure(figsize=(11, 5.5))
        sns.barplot(data=melted, x="Valor", y="Modelo", hue="Métrica")
        plt.xlim(0, 1.05)
        plt.xlabel("F1 macro", fontsize=12)
        plt.ylabel("Modelo", fontsize=12)
        plt.title("Comparación de modelos de Scikit-Learn", fontsize=13)
        plt.legend(loc="lower right")
        plt.grid(axis="x", alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateRocCurve(self, filename: str = "curva_roc.png") -> str:
        """Dibuja la curva ROC del mejor modelo sobre el conjunto de prueba."""
        if (
            self.context.bestModel is None
            or self.context.XTest is None
            or self.context.yTest is None
        ):
            raise ValueError("Faltan el modelo o los datos de prueba.")
        self._ensureDir()

        probabilities = self.context.bestModel.predict_proba(self.context.XTest)[:, 1]
        fpr, tpr, _ = roc_curve(self.context.yTest, probabilities)
        auc = roc_auc_score(self.context.yTest, probabilities)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color="darkorange", linewidth=2.5, label=f"AUC = {auc:.3f}")
        plt.plot([0, 1], [0, 1], color="gray", linestyle="--", linewidth=1)
        plt.xlabel("Tasa de falsos positivos", fontsize=12)
        plt.ylabel("Tasa de verdaderos positivos", fontsize=12)
        plt.title(
            f"Curva ROC - {self.context.report.bestModelName if self.context.report else 'modelo'}",
            fontsize=13,
        )
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateAll(self) -> list:
        """Genera todos los gráficos de evaluación y devuelve sus rutas."""
        return [
            self.generateConfusionMatrix(),
            self.generateRealVsPredicted(),
            self.generateModelComparison(),
            self.generateRocCurve(),
        ]
