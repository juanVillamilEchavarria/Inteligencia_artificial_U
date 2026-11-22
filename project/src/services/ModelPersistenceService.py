"""Guardado y carga del modelo entrenado y de sus métricas."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import joblib

from helpers.project_paths import MODEL_METRICS_PATH, MODEL_PATH


class ModelPersistenceService:
    """Serializa el modelo en disco y lo recupera sin volver a entrenarlo."""

    def __init__(
        self,
        modelPath: Path = MODEL_PATH,
        metricsPath: Path = MODEL_METRICS_PATH,
    ):
        """Guarda las rutas del modelo y de las métricas legibles."""
        self._modelPath = Path(modelPath)
        self._metricsPath = Path(metricsPath)

    @property
    def modelPath(self) -> Path:
        """Ruta configurada para el archivo joblib."""
        return self._modelPath

    @property
    def metricsPath(self) -> Path:
        """Ruta configurada para el archivo JSON de métricas."""
        return self._metricsPath

    def save(self, payload: Dict[str, Any]) -> str:
        """Guarda el modelo y su metadata, y devuelve la ruta creada."""
        self._modelPath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(payload, self._modelPath)
        return str(self._modelPath)

    def saveMetrics(self, metrics: Dict[str, Any]) -> str:
        """Escribe un JSON legible con las métricas para el README y el informe."""
        self._metricsPath.parent.mkdir(parents=True, exist_ok=True)
        document = dict(metrics)
        document.setdefault("generatedAt", datetime.now().isoformat(timespec="seconds"))
        with open(self._metricsPath, "w", encoding="utf-8") as file:
            json.dump(document, file, ensure_ascii=False, indent=2)
        return str(self._metricsPath)

    def load(self) -> Dict[str, Any]:
        """Carga el modelo guardado.

        Raises:
            FileNotFoundError: Si todavía no existe el archivo del modelo.
        """
        if not self._modelPath.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en {self._modelPath}. "
                "Ejecute primero: python src/modelo_proyecto.py"
            )
        return joblib.load(self._modelPath)

    def loadMetrics(self) -> Dict[str, Any]:
        """Carga las métricas guardadas en JSON.

        Raises:
            FileNotFoundError: Si todavía no existe el archivo de métricas.
        """
        if not self._metricsPath.exists():
            raise FileNotFoundError(
                f"No se encontraron las métricas en {self._metricsPath}. "
                "Ejecute primero: python src/modelo_proyecto.py"
            )
        with open(self._metricsPath, "r", encoding="utf-8") as file:
            return json.load(file)
