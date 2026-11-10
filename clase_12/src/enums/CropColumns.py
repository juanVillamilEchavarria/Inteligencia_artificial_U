"""Nombres de columnas usados por los datasets de la clase 12."""

from enum import Enum


class CropColumns(str, Enum):
    """Columnas del dataset de cultivos de Cartago."""

    LOTE = "lote"
    PRECIPITACION_MM = "precipitacion_mm"
    TEMPERATURA_C = "temperatura_c"
    COSECHA_EXITOSA = "cosecha_exitosa"


class RegressionColumns(str, Enum):
    """Columnas del dataset simulado de rendimiento."""

    PRECIPITACION_MM = "precipitacion_mm"
    TEMPERATURA_C = "temperatura_c"
    FERTILIZANTE_KG_HA = "fertilizante_kg_ha"
    RENDIMIENTO_KG_HA = "rendimiento_kg_ha"
