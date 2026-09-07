from entities.Movement import Movement
from enums.MovementFilteringKeys import MovementFilteringKeys
"""Coleccion de movimientos

Methods:
    getByKey(key: MovementFilteringKeys, value: str)
    count()
    getItems()
"""
class MovementsCollection:
    def __init__(self, movements : list[Movement]):
        self.movements = movements
    @staticmethod
    def from_dict( d: dict)->MovementsCollection:
        return MovementsCollection(
            movements= [Movement.from_dict(movement) for movement in d]
        )

    """
    Filtra movimientos por key y value

    Args:
        key: MovementFilteringKeys
        value: str

    Returns:
        list[Movement]
    """
    def getByKey(self, key: MovementFilteringKeys, value: str)-> list[Movement]:
        filtered_movements = []
        for movement in self.movements:
                if getattr(movement, key.value) == value:
                    filtered_movements.append(movement)
        return filtered_movements
    """
    Contar movimientos

    Returns:
        int
    """
    def count(self)-> int:
        return len(self.movements)

    """
    Obtiene todos los items de la coleccion

    Returns:
        list[Movement]
    """
    def getItems(self)-> list[Movement]:
        return self.movements