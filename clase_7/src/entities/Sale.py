from datetime import datetime
from dataclasses import dataclass


@dataclass
class Sale:
    id_venta: str
    fecha: datetime
    producto: str
    categoria: str
    precio_unitario: float
    cantidad: int
    ciudad: str
    cliente_edad: float
    metodo_pago: str

    @property
    def total_venta(self) -> float:
        return self.precio_unitario * self.cantidad

    @staticmethod
    def from_dict(d: dict) -> 'Sale':
        edad = d.get('cliente_edad')
        if edad == '' or edad is None:
            edad = 0.0
        else:
            edad = float(edad)
        return Sale(
            id_venta=str(d['id_venta']),
            fecha=datetime.strptime(d['fecha'], '%Y-%m-%d'),
            producto=str(d['producto']),
            categoria=str(d['categoria']),
            precio_unitario=float(d['precio_unitario']),
            cantidad=int(d['cantidad']),
            ciudad=str(d['ciudad']),
            cliente_edad=edad,
            metodo_pago=str(d['metodo_pago'])
        )