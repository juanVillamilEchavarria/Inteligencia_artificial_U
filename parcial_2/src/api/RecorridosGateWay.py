"""Punto de acceso a los recorridos de recolección de residuos.

Los datos se leen del CSV original asignado al grupo. Esta clase concentra el
acceso a la fuente para que el resto del sistema no dependa del formato físico.
"""

import pandas as pd

from app_collections.RecorridosCollection import RecorridosCollection
from helpers.project_paths import SOURCE_DATASET_PATH


class RecorridosGateWay:
    """Obtiene los recorridos desde el archivo CSV del grupo."""

    @staticmethod
    def __open() -> pd.DataFrame:
        """Lee el CSV original sin aplicar todavía ninguna transformación."""
        return pd.read_csv(SOURCE_DATASET_PATH)

    @staticmethod
    def getData() -> RecorridosCollection:
        """Carga los recorridos del CSV y los entrega como colección."""
        return RecorridosCollection.from_dataframe(RecorridosGateWay.__open())
