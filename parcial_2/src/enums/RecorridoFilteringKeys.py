"""Claves disponibles para filtrar recorridos de recolección."""

from enum import Enum


class RecorridoFilteringKeys(Enum):
    """Campos por los que se puede filtrar una colección de recorridos."""

    RECORRIDO_ID = "recorrido_id"
    RUTA = "ruta"
    RUTA_RETRASADA = "ruta_retrasada"
