from entities.Movement import Movement
from enums.MovementFilteringKeys import MovementFilteringKeys
from typing import List
"""Coleccion de movimientos

Methods:
    getByKey(key: MovementFilteringKeys, value: str)
    count()
    getItems()
    to_dataframe()
"""
class MovementsCollection:
    def __init__(self, movements : List[Movement]):
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
    def getByKey(self, key: MovementFilteringKeys, value: str)-> List[Movement]:
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
    def getItems(self)-> List[Movement]:
        return self.movements

    """
    Convierte la colección a pandas DataFrame

    Returns:
        pd.DataFrame
    """
    def to_dataframe(self):
        import pandas as pd
        data = []
        for movement in self.movements:
            data.append({
                'id': movement.id,
                'nombre': movement.nombre,
                'cuenta': movement.cuenta,
                'categoria': movement.categoria,
                'tipo_movimiento': movement.tipo_movimiento,
                'monto': movement.monto,
                'fecha': movement.fecha,
                'descripcion': movement.descripcion
            })
        return pd.DataFrame(data)