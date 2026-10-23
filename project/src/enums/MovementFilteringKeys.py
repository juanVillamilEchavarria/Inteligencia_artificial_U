"""Claves disponibles para filtrar movimientos financieros."""

from enum import Enum


class MovementFilteringKeys(Enum):
    """Campos por los que se puede filtrar una colección de movimientos."""

    CUENTA = 'cuenta'
    CATEGORIA = 'categoria'
    TIPO_MOVIMIENTO = 'tipo_movimiento'
    FECHA = 'fecha'
