from app_collections.SalesCollection import SalesCollection
from enums.SaleFilteringKeys import SaleFilteringKeys
from entities.Sale import Sale
from typing import List


class SalesStatisticsService:
    def __init__(self, sales_collection: SalesCollection):
        self.sales_collection = sales_collection

    def get_all_sales(self) -> List[Sale]:
        return self.sales_collection.get_items()

    def get_sales_by_category(self, category: str) -> List[Sale]:
        return self.sales_collection.get_by_key(SaleFilteringKeys.CATEGORIA, category)

    def get_sales_by_payment_method(self, method: str) -> List[Sale]:
        return self.sales_collection.get_by_key(SaleFilteringKeys.METODO_PAGO, method)

    def get_total_sales(self) -> float:
        return sum(sale.total_venta for sale in self.get_all_sales())

    def get_average_sale(self) -> float:
        sales = self.get_all_sales()
        if len(sales) == 0:
            return 0
        return self.get_total_sales() / len(sales)

    def get_min_sale(self) -> float:
        sales = self.get_all_sales()
        if len(sales) == 0:
            return 0
        return min(sale.total_venta for sale in sales)

    def get_max_sale(self) -> float:
        sales = self.get_all_sales()
        if len(sales) == 0:
            return 0
        return max(sale.total_venta for sale in sales)

    def get_total_sales_by_category(self, category: str) -> float:
        sales = self.get_sales_by_category(category)
        return sum(sale.total_venta for sale in sales)

    def get_categories(self) -> List[str]:
        sales = self.get_all_sales()
        return list(set(sale.categoria for sale in sales))

    def get_payment_methods(self) -> List[str]:
        sales = self.get_all_sales()
        return list(set(sale.metodo_pago for sale in sales))

    def get_cities(self) -> List[str]:
        sales = self.get_all_sales()
        return list(set(sale.ciudad for sale in sales))

    def get_null_age_count(self) -> int:
        sales = self.get_all_sales()
        return sum(1 for sale in sales if sale.cliente_edad == 0.0)