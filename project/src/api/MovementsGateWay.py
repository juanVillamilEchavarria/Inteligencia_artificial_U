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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'data.json')
        with open(data_path, 'r') as data:
            return json.load(data)
    @staticmethod
    def getData()->MovementsCollection:
        return MovementsCollection.from_dict(MovementsGateWay.__open())
        