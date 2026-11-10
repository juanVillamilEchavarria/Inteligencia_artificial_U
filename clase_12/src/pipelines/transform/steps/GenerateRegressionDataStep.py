"""Paso que genera los datos simulados de rendimiento."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.transform.DataPreparationContext import DataPreparationContext
from services.SyntheticDataService import SyntheticDataService


class GenerateRegressionDataStep(PipelineStep[DataPreparationContext]):
    """Crea el dataset sintético de rendimiento de cultivos."""

    def __init__(self, n: int = 150, seed: int = 7):
        """Define el tamaño del dataset y la semilla reproducible."""
        self._n = n
        self._seed = seed

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Generación de datos de rendimiento"

    def execute(
        self, context: DataPreparationContext
    ) -> DataPreparationContext:
        """Genera el dataframe y lo deja como dato crudo."""
        dataframe = SyntheticDataService.generate_yield_data(
            n=self._n,
            seed=self._seed,
        )
        metadata = dict(context.metadata)
        metadata["rows"] = len(dataframe)
        metadata["source"] = "SyntheticDataService"
        return replace(context, dfRaw=dataframe, metadata=metadata)
