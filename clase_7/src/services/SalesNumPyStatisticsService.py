import numpy as np
from app_collections.SalesCollection import SalesCollection
from enums.SaleFilteringKeys import SaleFilteringKeys
from entities.Sale import Sale
from dto.SaleNumPyDTO import SaleNumPyDTO
from typing import List, Dict


class SalesNumPyStatisticsService:
    def __init__(self, sales_collection: SalesCollection):
        self.sales_collection = sales_collection

    def get_total_venta_array(self) -> np.ndarray:
        return np.array([sale.total_venta for sale in self.sales_collection.get_items()])

    def get_edad_array(self) -> np.ndarray:
        return np.array([sale.cliente_edad for sale in self.sales_collection.get_items() if sale.cliente_edad > 0])

    def get_precio_unitario_array(self) -> np.ndarray:
        return np.array([sale.precio_unitario for sale in self.sales_collection.get_items()])

    def get_cantidad_array(self) -> np.ndarray:
        return np.array([sale.cantidad for sale in self.sales_collection.get_items()])

    def get_encoded_categoria_array(self) -> np.ndarray:
        sales = self.sales_collection.get_items()
        categories = [sale.categoria for sale in sales]
        unique_cats = sorted(list(set(categories)))
        cat_to_num = {cat: i for i, cat in enumerate(unique_cats)}
        return np.array([cat_to_num[c] for c in categories]), unique_cats

    def get_encoded_metodo_pago_array(self) -> np.ndarray:
        sales = self.sales_collection.get_items()
        methods = [sale.metodo_pago for sale in sales]
        unique_methods = sorted(list(set(methods)))
        method_to_num = {m: i for i, m in enumerate(unique_methods)}
        return np.array([method_to_num[m] for m in methods]), unique_methods

    def get_encoded_ciudad_array(self) -> np.ndarray:
        sales = self.sales_collection.get_items()
        cities = [sale.ciudad for sale in sales]
        unique_cities = sorted(list(set(cities)))
        city_to_num = {c: i for i, c in enumerate(unique_cities)}
        return np.array([city_to_num[c] for c in cities]), unique_cities

    def get_stats_for_array(self, data: np.ndarray) -> SaleNumPyDTO:
        if len(data) == 0:
            return SaleNumPyDTO(0, 0, 0, 0, 0, 0, 0)
        return SaleNumPyDTO(
            np.median(data),
            np.mean(data),
            np.std(data),
            np.min(data),
            np.max(data),
            len(data),
            np.sum(data)
        )

    def get_total_venta_stats(self) -> SaleNumPyDTO:
        return self.get_stats_for_array(self.get_total_venta_array())

    def get_edad_stats(self) -> SaleNumPyDTO:
        return self.get_stats_for_array(self.get_edad_array())

    def get_stats_by_category(self) -> Dict[str, SaleNumPyDTO]:
        sales = self.sales_collection.get_items()
        categories = list(set(sale.categoria for sale in sales))
        result = {}
        for cat in sorted(categories):
            amounts = np.array([sale.total_venta for sale in sales if sale.categoria == cat])
            result[cat] = self.get_stats_for_array(amounts)
        return result

    def get_stats_by_payment_method(self) -> Dict[str, SaleNumPyDTO]:
        sales = self.sales_collection.get_items()
        methods = list(set(sale.metodo_pago for sale in sales))
        result = {}
        for method in sorted(methods):
            amounts = np.array([sale.total_venta for sale in sales if sale.metodo_pago == method])
            result[method] = self.get_stats_for_array(amounts)
        return result

    def get_correlation_matrix(self) -> np.ndarray:
        total_venta = self.get_total_venta_array()
        edad = self.get_edad_array()
        precio = self.get_precio_unitario_array()
        cantidad = self.get_cantidad_array()
        
        min_len = min(len(total_venta), len(edad), len(precio), len(cantidad))
        data = np.column_stack([
            total_venta[:min_len],
            edad[:min_len],
            precio[:min_len],
            cantidad[:min_len]
        ])
        return np.corrcoef(data, rowvar=False)