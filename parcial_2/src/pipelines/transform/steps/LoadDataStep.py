"""Paso que carga los recorridos originales en un dataframe."""

from dataclasses import replace

from api.RecorridosGateWay import RecorridosGateWay
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class LoadDataStep(DataPreparationStep):
    """Obtiene los recorridos y los deja como dataframe crudo."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Carga de datos"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Convierte la colección de recorridos en un dataframe."""
        collection = RecorridosGateWay.getData()
        dfRaw = collection.to_dataframe()
        return replace(context, dfRaw=dfRaw)
