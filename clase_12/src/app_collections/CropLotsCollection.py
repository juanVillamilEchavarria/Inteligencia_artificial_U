"""Colección de lotes de cultivo con conversión a DataFrame."""

from dataclasses import asdict
from typing import List

import pandas as pd

from entities.CropLot import CropLot


class CropLotsCollection:
    """Agrupa una lista de lotes y facilita su análisis."""

    def __init__(self, lots: List[CropLot]):
        """Crea la colección a partir de una lista de entidades."""
        self._lots = list(lots)

    @staticmethod
    def from_dataframe(dataframe: pd.DataFrame) -> "CropLotsCollection":
        """Construye la colección a partir de las filas de un DataFrame."""
        return CropLotsCollection(
            [CropLot.from_dict(row) for row in dataframe.to_dict("records")]
        )

    def to_dataframe(self) -> pd.DataFrame:
        """Convierte la colección en un DataFrame de Pandas."""
        return pd.DataFrame([asdict(lot) for lot in self._lots])

    def get_items(self) -> List[CropLot]:
        """Devuelve la lista completa de lotes."""
        return list(self._lots)

    def get_by_target(self, value: int) -> List[CropLot]:
        """Filtra los lotes según el valor de ``cosecha_exitosa``."""
        return [lot for lot in self._lots if lot.cosecha_exitosa == value]

    def count(self) -> int:
        """Devuelve la cantidad de lotes de la colección."""
        return len(self._lots)
