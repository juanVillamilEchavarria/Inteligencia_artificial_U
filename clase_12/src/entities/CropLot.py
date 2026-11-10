"""Entidad que representa un lote de cultivo."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class CropLot:
    """Datos originales de un lote de cultivo.

    Attributes:
        lote: Identificador del lote.
        precipitacion_mm: Lluvia mensual en milímetros.
        temperatura_c: Temperatura promedio en grados Celsius.
        cosecha_exitosa: 1 si la cosecha fue exitosa, 0 si no.
    """

    lote: str
    precipitacion_mm: float
    temperatura_c: float
    cosecha_exitosa: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CropLot":
        """Construye un lote a partir de una fila del CSV."""
        return CropLot(
            lote=str(data["lote"]),
            precipitacion_mm=float(data["precipitacion_mm"]),
            temperatura_c=float(data["temperatura_c"]),
            cosecha_exitosa=int(data["cosecha_exitosa"]),
        )
