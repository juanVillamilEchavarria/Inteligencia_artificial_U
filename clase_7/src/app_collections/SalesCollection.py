from entities.Sale import Sale
from enums.SaleFilteringKeys import SaleFilteringKeys
from typing import List


class SalesCollection:
    def __init__(self, sales: List[Sale]):
        self.sales = sales

    @staticmethod
    def from_dataframe(df) -> 'SalesCollection':
        sales = [Sale.from_dict(row.to_dict()) for _, row in df.iterrows()]
        return SalesCollection(sales=sales)

    def get_by_key(self, key: SaleFilteringKeys, value: str) -> List[Sale]:
        filtered_sales = []
        for sale in self.sales:
            if getattr(sale, key.value) == value:
                filtered_sales.append(sale)
        return filtered_sales

    def count(self) -> int:
        return len(self.sales)

    def get_items(self) -> List[Sale]:
        return self.sales

    def to_dataframe(self):
        import pandas as pd
        data = []
        for sale in self.sales:
            data.append({
                'id_venta': sale.id_venta,
                'fecha': sale.fecha,
                'producto': sale.producto,
                'categoria': sale.categoria,
                'precio_unitario': sale.precio_unitario,
                'cantidad': sale.cantidad,
                'ciudad': sale.ciudad,
                'cliente_edad': sale.cliente_edad,
                'metodo_pago': sale.metodo_pago,
                'total_venta': sale.total_venta
            })
        return pd.DataFrame(data)