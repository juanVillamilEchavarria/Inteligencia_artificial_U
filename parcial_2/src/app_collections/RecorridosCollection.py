"""Colección de recorridos con operaciones de consulta y conversión."""

from typing import List

from entities.Recorrido import Recorrido
from enums.RecorridoFilteringKeys import RecorridoFilteringKeys


class RecorridosCollection:
    """Agrupa una lista de recorridos y facilita su filtrado y análisis."""

    def __init__(self, recorridos: List[Recorrido]):
        """Crea la colección a partir de una lista de objetos Recorrido."""
        self.recorridos = recorridos

    @staticmethod
    def from_dataframe(df) -> "RecorridosCollection":
        """Construye una colección a partir de un DataFrame con las columnas del CSV."""
        return RecorridosCollection(
            recorridos=[Recorrido.from_record(record) for record in df.to_dict("records")]
        )

    def getByKey(self, key: RecorridoFilteringKeys, value) -> List[Recorrido]:
        """Filtra los recorridos por un campo y un valor."""
        return [
            recorrido
            for recorrido in self.recorridos
            if getattr(recorrido, key.value) == value
        ]

    def count(self) -> int:
        """Devuelve la cantidad de recorridos de la colección."""
        return len(self.recorridos)

    def getItems(self) -> List[Recorrido]:
        """Devuelve la lista completa de recorridos."""
        return self.recorridos

    def to_dataframe(self):
        """Convierte la colección en un DataFrame de Pandas."""
        import pandas as pd

        return pd.DataFrame([recorrido.to_dict() for recorrido in self.recorridos])
