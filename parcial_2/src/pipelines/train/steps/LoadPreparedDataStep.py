"""Paso que carga el dataset generado por la preparación de datos."""

from dataclasses import replace
from pathlib import Path

import pandas as pd

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep


class LoadPreparedDataStep(TrainingStep):
    """Lee el CSV limpio y lo deja disponible en el contexto."""

    def __init__(self, dataPath: str):
        """Guarda la ruta del dataset que se va a cargar."""
        self._dataPath = Path(dataPath)

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Carga del dataset preparado"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Carga el CSV y falla con un mensaje claro si aún no existe."""
        if not self._dataPath.exists():
            raise FileNotFoundError(
                f"No se encontró el dataset limpio en {self._dataPath}. "
                "Ejecute primero el pipeline de preparación."
            )
        dfPrepared = pd.read_csv(self._dataPath)
        return replace(context, dfPrepared=dfPrepared)
