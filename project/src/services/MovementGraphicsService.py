import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para guardar sin mostrar ventana
from enums.MovementFilteringKeys import MovementFilteringKeys

from services.MovementNumPyStatisticsService import MovementNumPyStatisticsService


class MovementGraphicsService:
    """
    Service encargado de generar los gráficos del EDA.
    Guarda los archivos PNG en la carpeta /charts/
    """

    def __init__(self, numpyService: MovementNumPyStatisticsService):
        self.service = numpyService
        self.charts_dir = 'charts/'

    def _ensure_dir(self):
        import os
        os.makedirs(self.charts_dir, exist_ok=True)


    def generateAmountHistogram(self, filename: str = 'histograma_montos.png'):
        """
        Histograma de todos los montos.
        Muestra la distribución de valores en las transacciones.
        """
        self._ensure_dir()
        amounts = self.service.getAmountsArray()
        stats = self.service.getAllAmountsStats()

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.hist(amounts, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
        ax.axvline(stats.average, color='red', linestyle='dashed', linewidth=2,
                   label=f"Media: ${stats.average:,.0f}")
        ax.axvline(stats.median, color='green', linestyle='dashed', linewidth=2,
                   label=f"Mediana: ${stats.median:,.0f}")

        ax.set_xlabel('Monto (COP)', fontsize=12)
        ax.set_ylabel('Frecuencia', fontsize=12)
        ax.set_title('Distribución de Montos - Leo Counter', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Histograma guardado: {self.charts_dir}{filename}")


    def generateScatterPlot(self, filename: str = 'dispersion_monto_tipo.png'):
        """
        Gráfico de dispersión: Monto vs Tipo de movimiento codificado.
        Ingreso = 1, Gasto = 0
        """
        self._ensure_dir()
        amounts = self.service.getAmountsArray()
        types = self.service.getEncodedTypesArray()


        expenses_mask = types == 0
        incomes_mask = types == 1

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.scatter(
            np.zeros(np.sum(expenses_mask)), amounts[expenses_mask],
            color='red', alpha=0.6, s=80, label='Gastos'
        )
        ax.scatter(
            np.ones(np.sum(incomes_mask)), amounts[incomes_mask],
            color='green', alpha=0.6, s=80, label='Ingresos'
        )

        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Gastos', 'Ingresos'], fontsize=12)
        ax.set_ylabel('Monto (COP)', fontsize=12)
        ax.set_title('Dispersión de Montos por Tipo de Movimiento - Leo Counter', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f" Dispersión guardada: {self.charts_dir}{filename}")


    def generateCategoryBoxplot(self, filename: str = 'boxplot_gastos_categoria.png'):
        """
        Boxplot de gastos agrupados por categoría.
        Sirve para detectar categorías con mayor variabilidad.
        """
        self._ensure_dir()
        expenses_stats = self.service.getStatsByCategory()

        categories = list(expenses_stats.keys())
        data_by_cat = []
        for cat in categories:
            expenses = self.service.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Gasto')
            amounts = [mov.monto for mov in expenses if mov.categoria == cat]
            data_by_cat.append(amounts)

        fig, ax = plt.subplots(figsize=(14, 6))

        ax.boxplot(data_by_cat, label=categories, patch_artist=True)

        ax.set_ylabel('Monto (COP)', fontsize=12)
        ax.set_title('Distribución de Gastos por Categoría - Leo Counter', fontsize=14)
        ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=9)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{self.charts_dir}{filename}", dpi=150, bbox_inches='tight')
        plt.close()
        print(f" Boxplot guardado: {self.charts_dir}{filename}")

    def generateAll(self):
        """Genera todos los gráficos del EDA."""
        print("\n Generando gráficos del EDA...\n")
        self.generateAmountHistogram()
        self.generateScatterPlot()
        self.generateCategoryBoxplot()
        print("\n Todos los gráficos generados correctamente.\n")