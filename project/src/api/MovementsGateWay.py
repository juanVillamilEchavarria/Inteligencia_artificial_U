"""Punto de acceso a los movimientos financieros.

Los datos crudos viven en ``data/datos_originales.json``. Esta clase está pensada
para que, más adelante, la fuente sea una API sin cambiar el resto del sistema.
"""

import json

from app_collections.MovementsCollection import MovementsCollection
from helpers.project_paths import RAW_DATASET_PATH


class MovementsGateWay:
    """Obtiene los movimientos desde el archivo JSON canónico del proyecto."""

    @staticmethod
    def __open():
        """Lee el archivo de datos originales y devuelve la lista de diccionarios."""
        with open(RAW_DATASET_PATH, "r", encoding="utf-8") as data:
            return json.load(data)

    @staticmethod
    def getData() -> MovementsCollection:
        """Carga los movimientos del archivo JSON y los entrega como colección."""
        return MovementsCollection.from_dict(MovementsGateWay.__open())
