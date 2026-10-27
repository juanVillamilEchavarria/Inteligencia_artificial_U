"""Entidad que representa un recorrido de recolección de residuos."""


class Recorrido:
    """Recorrido con los datos que llegan desde el archivo original."""

    recorrido_id: str
    ruta: str
    toneladas_recogidas: float
    distancia_km: float
    ruta_retrasada: int

    def __init__(
        self,
        recorrido_id: str,
        ruta: str,
        toneladas_recogidas: float,
        distancia_km: float,
        ruta_retrasada: int,
    ):
        """Crea un recorrido con todos sus campos."""
        self.recorrido_id = recorrido_id
        self.ruta = ruta
        self.toneladas_recogidas = toneladas_recogidas
        self.distancia_km = distancia_km
        self.ruta_retrasada = ruta_retrasada

    @staticmethod
    def from_record(record: dict) -> "Recorrido":
        """Construye un Recorrido a partir de un registro del CSV."""
        return Recorrido(
            recorrido_id=str(record["recorrido_id"]),
            ruta=str(record["ruta"]),
            toneladas_recogidas=float(record["toneladas_recogidas"]),
            distancia_km=float(record["distancia_km"]),
            ruta_retrasada=int(record["ruta_retrasada"]),
        )

    def to_dict(self) -> dict:
        """Devuelve la entidad como diccionario con los nombres originales."""
        return {
            "recorrido_id": self.recorrido_id,
            "ruta": self.ruta,
            "toneladas_recogidas": self.toneladas_recogidas,
            "distancia_km": self.distancia_km,
            "ruta_retrasada": self.ruta_retrasada,
        }
