"""Paso que carga el dataset generado por la preparación de datos."""

from dataclasses import replace
from pathlib import Path

import pandas as pd

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep


class LoadPreparedDataStep(ModelTrainingStep):
    """Lee el CSV limpio y lo deja disponible en el contexto."""

    def __init__(self, dataPath: str):
        """Guarda la ruta del dataset que se va a cargar."""
        self._dataPath = Path(dataPath)

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Carga del dataset preparado"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Carga el CSV y falla con un mensaje claro si aún no existe."""
        if not self._dataPath.exists():
            raise FileNotFoundError(
                f"No se encontró el dataset preparado en {self._dataPath}. "
                "Ejecute primero: python src/data_preparation.py"
            )
        dfPrepared = pd.read_csv(self._dataPath)
        if dfPrepared.empty:
            raise ValueError("El dataset preparado está vacío.")
        return replace(context, dfPrepared=dfPrepared)
