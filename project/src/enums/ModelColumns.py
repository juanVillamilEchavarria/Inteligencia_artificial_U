"""Nombres de las columnas usadas por los modelos supervisados."""

from enum import Enum


class ModelColumns(Enum):
    """Variables de entrada y objetivo del modelo de Scikit-Learn."""

    TARGET = "es_ingreso"
    MONTO_LOG = "monto_log"
    MES = "mes"
    DIA_SEMANA = "dia_semana"
    ES_FIN_SEMANA = "es_fin_semana"
