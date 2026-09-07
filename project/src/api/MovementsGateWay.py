import json
from app_collections.MovementsCollection import MovementsCollection
class MovementsGateWay:
    """
    Clase para obtener los movimientos
    por el momento abre un archivo .json manualmente, pero a futuro hara la peticion via API
    """
    @staticmethod
    def __open():
        with open('data/data.json', 'r') as data:
            return json.load(data)
    @staticmethod
    def getData()->MovementsCollection:
        return MovementsCollection.from_dict(MovementsGateWay.__open())
        