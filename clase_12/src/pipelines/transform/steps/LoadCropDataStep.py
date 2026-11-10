"""Paso que carga el dataset de cultivos desde el gateway."""

from dataclasses import replace

from api.CropDataGateway import CropDataGateway
from pipelines.core.PipelineStep import PipelineStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class LoadCropDataStep(PipelineStep[DataPreparationContext]):
    """Lee el CSV de cultivos y lo deja como dataframe crudo."""

    def __init__(self, gateway: CropDataGateway):
        """Recibe el gateway que conoce la ruta del archivo."""
        self._gateway = gateway

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Carga de datos de cultivos"

    def execute(
        self, context: DataPreparationContext
    ) -> DataPreparationContext:
        """Convierte la colección de lotes en un dataframe."""
        collection = self._gateway.get_data()
        metadata = dict(context.metadata)
        metadata["rows"] = collection.count()
        metadata["source"] = "CropDataGateway"
        return replace(
            context,
            dfRaw=collection.to_dataframe(),
            metadata=metadata,
        )
