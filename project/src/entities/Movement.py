"""Entidad que representa un movimiento financiero dentro del sistema."""

from datetime import datetime


class Movement:
    """Movimiento financiero con los datos que llegan desde la fuente original."""

    id: str
    nombre: str
    cuenta: str
    categoria: str
    tipo_movimiento: str
    monto: float
    fecha: str
    descripcion: str

    def __init__(self, id, nombre, cuenta, categoria, tipo_movimiento, monto, fecha, descripcion):
        """Crea un movimiento con todos sus campos."""
        self.id = id
        self.nombre = nombre
        self.cuenta = cuenta
        self.categoria = categoria
        self.tipo_movimiento = tipo_movimiento
        self.monto = monto
        self.fecha = fecha
        self.descripcion = descripcion

    @staticmethod
    def from_dict(d: dict) -> "Movement":
        """Construye un Movement a partir de un diccionario con las claves del JSON."""
        return Movement(
            id=d['id'],
            nombre=d['nombre'],
            cuenta=d['cuenta'],
            categoria=d['categoria'],
            tipo_movimiento=d['tipo_movimiento'],
            monto=float(d['monto']),
            fecha=datetime.strptime(d['fecha'], '%Y-%m-%d'),
            descripcion=d['descripcion']
        )
