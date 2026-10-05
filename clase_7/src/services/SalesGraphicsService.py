import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from services.SalesNumPyStatisticsService import SalesNumPyStatisticsService


class SalesGraphicsService:
    def __init__(self, numpy_service: SalesNumPyStatisticsService):
        self.service = numpy_service
        self.charts_dir = 'charts/'

    def _ensure_dir(self):
        os.makedirs(self.charts_dir, exist_ok=True)

    def generate_histograma_ventas(self, filename: str = 'histograma_ventas.png'):
        self._ensure_dir()
        amounts = self.service.get_total_venta_array()
        stats = self.service.get_total_venta_stats()

        plt.figure(figsize=(10, 6))
        sns.histplot(data=amounts, bins=10, kde=True, color='skyblue')
        plt.axvline(stats.average, color='red', linestyle='dashed', linewidth=2,
                    label=f"Media: ${stats.average:,.2f}")
        plt.axvline(stats.median, color='green', linestyle='dashed', linewidth=2,
                    label=f"Mediana: ${stats.median:,.2f}")

        plt.xlabel('Total de Venta ($)', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title('Distribución del Total de Ventas', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Histograma guardado: {self.charts_dir}{filename}")

    def generate_barplot_categoria(self, filename: str = 'ventas_por_categoria.png'):
        self._ensure_dir()
        stats_by_cat = self.service.get_stats_by_category()
        
        categories = list(stats_by_cat.keys())
        totals = [stats_by_cat[cat].sum for cat in categories]

        plt.figure(figsize=(10, 6))
        sns.barplot(x=categories, y=totals, palette='viridis')
        plt.title('Total de Ventas por Categoría', fontsize=14)
        plt.xlabel('Categoría', fontsize=12)
        plt.ylabel('Total de Ventas ($)', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Barplot guardado: {self.charts_dir}{filename}")

    def generate_scatter_edad_venta(self, filename: str = 'edad_vs_venta.png'):
        self._ensure_dir()
        df = self.service.sales_collection.to_dataframe()
        df_clean = df.copy()
        median_age = df_clean['cliente_edad'].median()
        df_clean['cliente_edad'] = df_clean['cliente_edad'].fillna(median_age)
        df_clean['total_venta'] = df_clean['precio_unitario'] * df_clean['cantidad']

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df_clean, x='cliente_edad', y='total_venta', 
                        hue='categoria', style='metodo_pago', s=100)
        plt.title('Relación: Edad del Cliente vs Total de Venta', fontsize=14)
        plt.xlabel('Edad del Cliente', fontsize=12)
        plt.ylabel('Total de Venta ($)', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Scatter plot guardado: {self.charts_dir}{filename}")

    def generate_boxplot_categoria(self, filename: str = 'boxplot_ventas_categoria.png'):
        self._ensure_dir()
        stats_by_cat = self.service.get_stats_by_category()
        
        categories = list(stats_by_cat.keys())
        data_by_cat = []
        for cat in categories:
            sales = self.service.sales_collection.get_by_key(
                __import__('enums.SaleFilteringKeys', fromlist=['SaleFilteringKeys']).SaleFilteringKeys.CATEGORIA, cat
            )
            amounts = [sale.total_venta for sale in sales]
            data_by_cat.append(amounts)

        plt.figure(figsize=(12, 6))
        sns.boxplot(data=data_by_cat)
        plt.xticks(range(len(categories)), categories, rotation=45, ha='right')
        plt.title('Distribución de Ventas por Categoría', fontsize=14)
        plt.ylabel('Total de Venta ($)', fontsize=12)
        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Boxplot guardado: {self.charts_dir}{filename}")

    def generate_correlation_heatmap(self, filename: str = 'correlation_heatmap.png'):
        self._ensure_dir()
        corr_matrix = self.service.get_correlation_matrix()
        features = ['Total Venta', 'Edad', 'Precio Unitario', 'Cantidad']

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    xticklabels=features, yticklabels=features, center=0)
        plt.title('Matriz de Correlación', fontsize=14)
        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Heatmap guardado: {self.charts_dir}{filename}")

    def generate_all(self):
        print("\nGenerando gráficos del EDA...\n")
        self.generate_histograma_ventas()
        self.generate_barplot_categoria()
        self.generate_scatter_edad_venta()
        self.generate_boxplot_categoria()
        self.generate_correlation_heatmap()
        print("\nTodos los gráficos generados correctamente.\n")