from services.SalesStatisticsService import SalesStatisticsService


class SalesController:
    def __init__(self, sales_service: SalesStatisticsService):
        self.service = sales_service

    def get_total_sales(self):
        return self.service.get_total_sales()

    def get_average_sale(self):
        return self.service.get_average_sale()

    def get_min_sale(self):
        return self.service.get_min_sale()

    def get_max_sale(self):
        return self.service.get_max_sale()

    def get_total_sales_by_category(self, category: str):
        return self.service.get_total_sales_by_category(category)

    def get_categories(self):
        return self.service.get_categories()

    def get_payment_methods(self):
        return self.service.get_payment_methods()

    def get_cities(self):
        return self.service.get_cities()

    def get_null_age_count(self):
        return self.service.get_null_age_count()