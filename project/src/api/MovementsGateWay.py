"""Punto de acceso a los movimientos financieros.

Por ahora los datos se leen de un archivo JSON local. Esta clase está pensada
para que, más adelante, la fuente sea una API sin cambiar el resto del sistema.
"""

import json
import os
from app_collections.MovementsCollection import MovementsCollection


class MovementsGateWay:
    """
    Clase para obtener los movimientos
    por el momento abre un archivo .json manualmente, pero a futuro hara la peticion via API
    """
    @staticmethod
    def __open():
        """Lee el archivo data.json y devuelve su contenido como lista de diccionarios."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'data.json')
        with open(data_path, 'r') as data:
            return json.load(data)

    @staticmethod
    def getData() -> MovementsCollection:
        """Carga los movimientos del archivo JSON y los entrega como colección."""
        return MovementsCollection.from_dict(MovementsGateWay.__open())
        