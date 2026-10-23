"""Gráficos exploratorios del dataset preparado usando Seaborn."""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from helpers.project_paths import SEABORN_CHARTS_DIR


class SeabornChartRenderer:
    """Genera y guarda los gráficos del análisis exploratorio."""

    def __init__(self, dfPrepared: pd.DataFrame, chartsDir: str = None):
        """Recibe el dataframe preparado y la carpeta de salida."""
        self.dfPrepared = dfPrepared
        self.chartsDir = chartsDir or f"{SEABORN_CHARTS_DIR}/"

    def _ensureDir(self):
        """Crea la carpeta de gráficos si todavía no existe."""
        os.makedirs(self.chartsDir, exist_ok=True)

    def _save(self, filepath: str) -> str:
        """Ajusta la figura, la guarda y cierra el gráfico."""
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        return filepath

    def generateMontoHistogram(self, filename: str = 'seaborn_histograma_monto.png') -> str:
        """Genera el histograma de montos con media y mediana."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='monto', bins=30, kde=True, color='steelblue', edgecolor='black', alpha=0.7)
        plt.axvline(df['monto'].mean(), color='red', linestyle='--', linewidth=2, label=f"Media: ${df['monto'].mean():,.0f}")
        plt.axvline(df['monto'].median(), color='green', linestyle='--', linewidth=2, label=f"Mediana: ${df['monto'].median():,.0f}")
        plt.xlabel('Monto (COP)', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title('Distribución de Montos - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateMontoLogHistogram(self, filename: str = 'seaborn_histograma_monto_log.png') -> str:
        """Genera el histograma del monto transformado con logaritmo."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='monto_log', bins=30, kde=True, color='purple', edgecolor='black', alpha=0.7)
        plt.axvline(df['monto_log'].mean(), color='red', linestyle='--', linewidth=2, label=f"Media: {df['monto_log'].mean():.2f}")
        plt.axvline(df['monto_log'].median(), color='green', linestyle='--', linewidth=2, label=f"Mediana: {df['monto_log'].median():.2f}")
        plt.xlabel('Log(Monto + 1)', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title('Distribución de Log(Monto) - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateBoxplotCategory(self, filename: str = 'seaborn_boxplot_categoria.png') -> str:
        """Genera el boxplot de montos por categoría."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(16, 8))
        order = df.groupby('categoria')['monto'].median().sort_values(ascending=False).index
        sns.boxplot(data=df, x='categoria', y='monto', order=order, hue='categoria', palette='viridis', legend=False)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('Categoría', fontsize=12)
        plt.ylabel('Monto (COP)', fontsize=12)
        plt.title('Distribución de Montos por Categoría - Leo Counter (Seaborn)', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateBoxplotTipoMovimiento(self, filename: str = 'seaborn_boxplot_tipo.png') -> str:
        """Genera el boxplot que compara ingresos y gastos."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='tipo_movimiento', y='monto', hue='tipo_movimiento', palette={'Ingreso': 'green', 'Gasto': 'red'}, legend=False)
        plt.xlabel('Tipo de Movimiento', fontsize=12)
        plt.ylabel('Monto (COP)', fontsize=12)
        plt.title('Distribución de Montos: Ingresos vs Gastos - Leo Counter (Seaborn)', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateScatterMontoFecha(self, filename: str = 'seaborn_scatter_monto_fecha.png') -> str:
        """Genera la dispersión de monto contra fecha, separada por tipo."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(14, 6))
        topCategories = df['categoria'].value_counts().nlargest(5).index
        sns.scatterplot(
            data=df, x='fecha', y='monto', hue='tipo_movimiento',
            style=df['categoria'].where(df['categoria'].isin(topCategories), 'Otros'),
            s=100, palette={'Ingreso': 'green', 'Gasto': 'red'}
        )
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Monto (COP)', fontsize=12)
        plt.title('Dispersión: Monto vs Fecha por Tipo y Categoría - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateRegplotMontoLogFecha(self, filename: str = 'seaborn_regplot_monto_log_fecha.png') -> str:
        """Genera la regresión del monto logarítmico a lo largo del tiempo."""
        self._ensureDir()
        df = self.dfPrepared

        dfSorted = df.sort_values('fecha').reset_index(drop=True)
        dfSorted['fecha_num'] = (dfSorted['fecha'] - dfSorted['fecha'].min()).dt.days

        plt.figure(figsize=(12, 6))
        sns.regplot(data=dfSorted, x='fecha_num', y='monto_log',
                    scatter_kws={'alpha': 0.6, 's': 60}, line_kws={'color': 'red', 'linewidth': 2})
        plt.xlabel('Días desde primera transacción', fontsize=12)
        plt.ylabel('Log(Monto + 1)', fontsize=12)
        plt.title('Regresión: Log(Monto) vs Tiempo - Leo Counter (Seaborn)', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateBarplotCategoriaTipo(self, filename: str = 'seaborn_barplot_categoria_tipo.png') -> str:
        """Genera el total de montos por categoría y tipo de movimiento."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(14, 6))
        order = df.groupby('categoria')['monto'].sum().sort_values(ascending=False).index
        sns.barplot(data=df, x='categoria', y='monto', hue='tipo_movimiento', order=order,
                    estimator=np.sum, errorbar=None, palette={'Ingreso': 'green', 'Gasto': 'red'})
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.xlabel('Categoría', fontsize=12)
        plt.ylabel('Total Monto (COP)', fontsize=12)
        plt.title('Total de Montos por Categoría y Tipo - Leo Counter (Seaborn)', fontsize=14)
        plt.legend(title='Tipo', fontsize=10)
        plt.grid(axis='y', alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generateCorrelationHeatmap(self, filename: str = 'seaborn_correlation_heatmap.png') -> str:
        """Genera la matriz de correlación de las variables numéricas."""
        self._ensureDir()
        df = self.dfPrepared

        numericCols = df.select_dtypes(include=[np.number]).columns
        corrMatrix = df[numericCols].corr()

        plt.figure(figsize=(14, 10))
        mask = np.triu(np.ones_like(corrMatrix, dtype=bool))
        sns.heatmap(corrMatrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                    center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, annot_kws={'size': 6})
        plt.title('Matriz de Correlación (Variables Numéricas) - Leo Counter (Seaborn)', fontsize=14)
        return self._save(f"{self.chartsDir}{filename}")

    def generateScatterFeaturesTarget(self, filename: str = 'seaborn_scatter_features_target.png') -> str:
        """Grafica las dos entradas del modelo coloreadas por la clase."""
        self._ensureDir()
        df = self.dfPrepared

        plt.figure(figsize=(12, 6))
        sns.scatterplot(
            data=df,
            x='monto_log',
            y='mes',
            hue='es_ingreso',
            palette={0: 'tomato', 1: 'seagreen'},
            s=90,
            edgecolor='black',
            alpha=0.8,
        )
        plt.xlabel('Log(Monto + 1)', fontsize=12)
        plt.ylabel('Mes del movimiento', fontsize=12)
        plt.title('Variables de entrada vs variable objetivo (es_ingreso) - Leo Counter', fontsize=14)
        plt.legend(title='es_ingreso (0=Gasto, 1=Ingreso)', fontsize=10)
        plt.grid(alpha=0.3)
        return self._save(f"{self.chartsDir}{filename}")

    def generatePairplot(self, filename: str = 'seaborn_pairplot.png') -> str:
        """Genera el pairplot de las variables numéricas principales."""
        self._ensureDir()
        df = self.dfPrepared
        columns = ['monto_log', 'mes', 'dia_semana', 'es_fin_semana', 'es_ingreso']
        pairplot = sns.pairplot(df[columns], hue='es_ingreso', palette={0: 'tomato', 1: 'seagreen'})
        pairplot.figure.suptitle('Pairplot de variables numéricas - Leo Counter', y=1.02, fontsize=14)
        pairplot.savefig(f"{self.chartsDir}{filename}", dpi=150, bbox_inches='tight')
        plt.close(pairplot.figure)
        return f"{self.chartsDir}{filename}"

    def generateAll(self) -> list:
        """Genera todos los gráficos y devuelve sus rutas."""
        return [
            self.generateMontoHistogram(),
            self.generateMontoLogHistogram(),
            self.generateBoxplotCategory(),
            self.generateBoxplotTipoMovimiento(),
            self.generateScatterMontoFecha(),
            self.generateRegplotMontoLogFecha(),
            self.generateBarplotCategoriaTipo(),
            self.generateCorrelationHeatmap(),
            self.generateScatterFeaturesTarget(),
            self.generatePairplot(),
        ]
