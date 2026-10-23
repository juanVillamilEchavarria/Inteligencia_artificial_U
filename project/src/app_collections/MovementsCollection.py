"""Colección de movimientos financieros con operaciones de consulta y conversión."""

from entities.Movement import Movement
from enums.MovementFilteringKeys import MovementFilteringKeys
from typing import List


class MovementsCollection:
    """Agrupa una lista de movimientos y facilita su filtrado y análisis."""

    def __init__(self, movements: List[Movement]):
        """Crea la colección a partir de una lista de objetos Movement."""
        self.movements = movements

    @staticmethod
    def from_dict(d: dict) -> MovementsCollection:
        """Construye una colección a partir de una lista de diccionarios."""
        return MovementsCollection(
            movements=[Movement.from_dict(movement) for movement in d]
        )

    def getByKey(self, key: MovementFilteringKeys, value: str) -> List[Movement]:
        """Filtra los movimientos por un campo y un valor.

        Args:
            key: Campo por el que se quiere filtrar.
            value: Valor que debe tener el campo.

        Returns:
            Los movimientos que cumplen la condición.
        """
        filtered_movements = []
        for movement in self.movements:
            if getattr(movement, key.value) == value:
                filtered_movements.append(movement)
        return filtered_movements

    def count(self) -> int:
        """Devuelve la cantidad de movimientos de la colección."""
        return len(self.movements)

    def getItems(self) -> List[Movement]:
        """Devuelve la lista completa de movimientos."""
        return self.movements

    def to_dataframe(self):
        """Convierte la colección en un DataFrame de Pandas."""
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
