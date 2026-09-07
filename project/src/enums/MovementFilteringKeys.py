from enum import Enum

"""
Clase que representa las claves de filtrado de movimientos financieros."""
class MovementFilteringKeys(Enum):
    CUENTA = 'cuenta'
    CATEGORIA = 'categoria'
    TIPO_MOVIMIENTO = 'tipo_movimiento'
    FECHA = 'fecha'