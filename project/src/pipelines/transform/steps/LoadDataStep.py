"""Paso que carga los movimientos originales en un dataframe."""

from dataclasses import replace

from api.MovementsGateWay import MovementsGateWay
from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class LoadDataStep(DataPreparationStep):
    """Obtiene los movimientos y los deja como dataframe crudo."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Carga de datos"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Convierte la colección de movimientos en un dataframe."""
        collection = MovementsGateWay.getData()
        dfRaw = collection.to_dataframe()
        return replace(context, dfRaw=dfRaw)
