from services.SalesGraphicsService import SalesGraphicsService


class SalesGraphicsController:
    def __init__(self, graphics_service: SalesGraphicsService):
        self.service = graphics_service

    def generate_all(self):
        self.service.generate_all()

    def generate_histograma_ventas(self):
        self.service.generate_histograma_ventas()

    def generate_barplot_categoria(self):
        self.service.generate_barplot_categoria()

    def generate_scatter_edad_venta(self):
        self.service.generate_scatter_edad_venta()

    def generate_boxplot_categoria(self):
        self.service.generate_boxplot_categoria()

    def generate_correlation_heatmap(self):
        self.service.generate_correlation_heatmap()