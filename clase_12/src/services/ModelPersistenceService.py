"""Guardado y carga de modelos entrenados con joblib."""

from pathlib import Path
from typing import Any

import joblib


class ModelPersistenceService:
    """Serializa un modelo en disco y lo recupera sin volver a entrenarlo."""

    def __init__(self, model_path: Path):
        """Guarda la ruta del archivo del modelo."""
        self._model_path = Path(model_path)

    @property
    def model_path(self) -> Path:
        """Ruta configurada para el archivo del modelo."""
        return self._model_path

    def save(self, model: Any) -> str:
        """Guarda el modelo y devuelve la ruta del archivo creado."""
        self._model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, self._model_path)
        return str(self._model_path)

    def load(self) -> Any:
        """Carga el modelo guardado.

        Raises:
            FileNotFoundError: Si todavía no existe el archivo del modelo.
        """
        if not self._model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en {self._model_path}. "
                "Ejecute primero: python clasificar_cultivos.py"
            )
        return joblib.load(self._model_path)
