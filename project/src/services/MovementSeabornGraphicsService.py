import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from services.MovementDataPreparationService import MovementDataPreparationService


class MovementSeabornGraphicsService:
    def __init__(self, preparation_service: MovementDataPreparationService):
        self.service = preparation_service
        self.charts_dir = 'charts_seaborn/'

    def _ensure_dir(self):
        os.makedirs(self.charts_dir, exist_ok=True)

    def _get_prepared_df(self) -> pd.DataFrame:
        if self.service.df_prepared is None:
            self.service.prepare_full_pipeline()
        return self.service.df_prepared

    def generate_monto_histogram(self, filename: str = 'seaborn_histograma_monto.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='monto', bins=30, kde=True, color='steelblue', edgecolor='black', alpha=0.7)
        plt.axvline(df['monto'].mean(), color='red', linestyle='--', linewidth=2, label=f"Media: ${df['monto'].mean():,.0f}")
        plt.axvline(df['monto'].median(), color='green', linestyle='--', linewidth=2, label=f"Mediana: ${df['monto'].median():,.0f}")

        plt.xlabel('Monto (COP)', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title('Distribución de Montos - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_monto_log_histogram(self, filename: str = 'seaborn_histograma_monto_log.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='monto_log', bins=30, kde=True, color='purple', edgecolor='black', alpha=0.7)
        plt.axvline(df['monto_log'].mean(), color='red', linestyle='--', linewidth=2, label=f"Media: {df['monto_log'].mean():.2f}")
        plt.axvline(df['monto_log'].median(), color='green', linestyle='--', linewidth=2, label=f"Mediana: {df['monto_log'].median():.2f}")

        plt.xlabel('Log(Monto + 1)', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title('Distribución de Log(Monto) - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_boxplot_category(self, filename: str = 'seaborn_boxplot_categoria.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        plt.figure(figsize=(16, 8))
        order = df.groupby('categoria')['monto'].median().sort_values(ascending=False).index
        sns.boxplot(data=df, x='categoria', y='monto', order=order, hue='categoria', palette='viridis', legend=False)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('Categoría', fontsize=12)
        plt.ylabel('Monto (COP)', fontsize=12)
        plt.title('Distribución de Montos por Categoría - Leo Counter (Seaborn)', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_boxplot_tipo_movimiento(self, filename: str = 'seaborn_boxplot_tipo.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='tipo_movimiento', y='monto', hue='tipo_movimiento', palette={'Ingreso': 'green', 'Gasto': 'red'}, legend=False)
        plt.xlabel('Tipo de Movimiento', fontsize=12)
        plt.ylabel('Monto (COP)', fontsize=12)
        plt.title('Distribución de Montos: Ingresos vs Gastos - Leo Counter (Seaborn)', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_scatter_monto_fecha(self, filename: str = 'seaborn_scatter_monto_fecha.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        plt.figure(figsize=(14, 6))
        sns.scatterplot(data=df, x='fecha', y='monto', hue='tipo_movimiento', 
                           style='categoria', s=100, palette={'Ingreso': 'green', 'Gasto': 'red'})
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Monto (COP)', fontsize=12)
        plt.title('Dispersión: Monto vs Fecha por Tipo y Categoría - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_regplot_monto_log_fecha(self, filename: str = 'seaborn_regplot_monto_log_fecha.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        df_sorted = df.sort_values('fecha').reset_index(drop=True)
        df_sorted['fecha_num'] = (df_sorted['fecha'] - df_sorted['fecha'].min()).dt.days

        plt.figure(figsize=(12, 6))
        sns.regplot(data=df_sorted, x='fecha_num', y='monto_log', 
                    scatter_kws={'alpha': 0.6, 's': 60}, line_kws={'color': 'red', 'linewidth': 2})
        plt.xlabel('Días desde primera transacción', fontsize=12)
        plt.ylabel('Log(Monto + 1)', fontsize=12)
        plt.title('Regresión: Log(Monto) vs Tiempo - Leo Counter (Seaborn)', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_barplot_categoria_tipo(self, filename: str = 'seaborn_barplot_categoria_tipo.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        plt.figure(figsize=(14, 6))
        sns.barplot(data=df, x='categoria', y='monto', hue='tipo_movimiento', 
                    estimator=np.sum, errorbar=None, palette={'Ingreso': 'green', 'Gasto': 'red'})
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('Categoría', fontsize=12)
        plt.ylabel('Total Monto (COP)', fontsize=12)
        plt.title('Total de Montos por Categoría y Tipo - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(title='Tipo', fontsize=10)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_correlation_heatmap(self, filename: str = 'seaborn_correlation_heatmap.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr()

        plt.figure(figsize=(14, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title('Matriz de Correlación (Variables Numéricas) - Leo Counter (Seaborn)', fontsize=14)
        plt.tight_layout()
        filepath = f"{self.charts_dir}{filename}"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generate_pairplot_sample(self, filename: str = 'seaborn_pairplot.png') -> str:
        self._ensure_dir()
        df = self._get_prepared_df()

        sample_cols = ['monto', 'monto_log', 'es_ingreso', 'mes', 'dia_semana', 'es_fin_semana']
        available_cols = [c for c in sample_cols if c in df.columns]
        df_sample = df[available_cols].dropna()

        if len(df_sample) > 0 and len(available_cols) > 1:
            g = sns.pairplot(df_sample, diag_kind='hist', plot_kws={'alpha': 0.6, 's': 30})
            g.fig.suptitle('Pairplot de Variables Numéricas Principales - Leo Counter (Seaborn)', y=1.02, fontsize=14)
            plt.tight_layout()
            filepath = f"{self.charts_dir}{filename}"
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            return filepath
        return None

    def generate_all(self) -> list:
        generated_files = []
        generated_files.append(self.generate_monto_histogram())
        generated_files.append(self.generate_monto_log_histogram())
        generated_files.append(self.generate_boxplot_category())
        generated_files.append(self.generate_boxplot_tipo_movimiento())
        generated_files.append(self.generate_scatter_monto_fecha())
        generated_files.append(self.generate_regplot_monto_log_fecha())
        generated_files.append(self.generate_barplot_categoria_tipo())
        generated_files.append(self.generate_correlation_heatmap())
        pairplot_path = self.generate_pairplot_sample()
        if pairplot_path:
            generated_files.append(pairplot_path)
        return generated_files