import pandas as pd
import numpy as np
from api.MovementsGateWay import MovementsGateWay
from app_collections.MovementsCollection import MovementsCollection
from typing import Dict, Any, Tuple


class MovementDataPreparationService:
    """
    Servicio para la preparación de datos de movimientos financieros.
    Este servicio realiza la carga de datos, análisis exploratorio (EDA), limpieza,
    creación de columnas derivadas y codificación de variables categóricas.
    Atributos:
        gateway (MovementsGateWay): Instancia del gateway para acceder a los datos.
        movements_collection (MovementsCollection): Colección de movimientos cargados.
        df_raw (pd.DataFrame): DataFrame con los datos crudos cargados.
        df_clean (pd.DataFrame): DataFrame con los datos limpios.
        df_prepared (pd.DataFrame): DataFrame con los datos preparados para análisis.
        eda_findings (Dict[str, Any]): Diccionario con los hallazgos del análisis exploratorio de datos (EDA).
    """
    def __init__(self):
        self.gateway = MovementsGateWay()
        self.movements_collection: MovementsCollection = None
        self.df_raw: pd.DataFrame = None
        self.df_clean: pd.DataFrame = None
        self.df_prepared: pd.DataFrame = None
        self.eda_findings: Dict[str, Any] = {}

    def load_data(self) -> pd.DataFrame:
        self.movements_collection = self.gateway.getData()
        self.df_raw = self.movements_collection.to_dataframe()
        return self.df_raw

    def perform_eda(self) -> Dict[str, Any]:
        if self.df_raw is None:
            self.load_data()

        findings = {}
        findings['shape'] = self.df_raw.shape
        findings['head'] = self.df_raw.head().to_dict()
        findings['info'] = self._get_info_string()
        findings['describe'] = self.df_raw.describe(include='all').to_dict()
        findings['null_counts'] = self.df_raw.isnull().sum().to_dict()
        findings['dtypes'] = self.df_raw.dtypes.astype(str).to_dict()
        findings['unique_categories'] = self.df_raw['categoria'].nunique()
        findings['unique_accounts'] = self.df_raw['cuenta'].nunique()
        findings['tipo_movimiento_dist'] = self.df_raw['tipo_movimiento'].value_counts().to_dict()
        findings['categoria_dist'] = self.df_raw['categoria'].value_counts().to_dict()
        findings['cuenta_dist'] = self.df_raw['cuenta'].value_counts().to_dict()

        self._analyze_findings(findings)
        self.eda_findings = findings
        return findings

    def _get_info_string(self) -> str:
        import io
        buffer = io.StringIO()
        self.df_raw.info(buf=buffer)
        return buffer.getvalue()

    def _analyze_findings(self, findings: Dict[str, Any]):
        null_counts = findings['null_counts']
        total_nulls = sum(null_counts.values())
        findings['total_nulls'] = total_nulls
        findings['columns_with_nulls'] = {k: v for k, v in null_counts.items() if v > 0}

        amounts = self.df_raw['monto']
        findings['monto_skew'] = float(amounts.skew())
        findings['monto_kurtosis'] = float(amounts.kurtosis())
        findings['monto_outliers_iqr'] = self._detect_outliers_iqr(amounts)

        income_amounts = self.df_raw[self.df_raw['tipo_movimiento'] == 'Ingreso']['monto']
        expense_amounts = self.df_raw[self.df_raw['tipo_movimiento'] == 'Gasto']['monto']
        findings['income_vs_expense'] = {
            'income_count': len(income_amounts),
            'expense_count': len(expense_amounts),
            'income_mean': float(income_amounts.mean()),
            'expense_mean': float(expense_amounts.mean()),
            'income_median': float(income_amounts.median()),
            'expense_median': float(expense_amounts.median()),
            'income_max': float(income_amounts.max()),
            'expense_max': float(expense_amounts.max()),
        }

    def _detect_outliers_iqr(self, series: pd.Series) -> Dict[str, Any]:
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = series[(series < lower) | (series > upper)]
        return {
            'Q1': float(Q1),
            'Q3': float(Q3),
            'IQR': float(IQR),
            'lower_bound': float(lower),
            'upper_bound': float(upper),
            'outlier_count': int(len(outliers)),
            'outlier_percentage': float(len(outliers) / len(series) * 100),
            'outlier_values': outliers.tolist()
        }

    def clean_data(self) -> pd.DataFrame:
        if self.df_raw is None:
            self.load_data()

        self.df_clean = self.df_raw.copy()

        for col in self.df_clean.columns:
            if self.df_clean[col].isnull().any():
                if self.df_clean[col].dtype in ['float64', 'int64']:
                    median_val = self.df_clean[col].median()
                    self.df_clean[col] = self.df_clean[col].fillna(median_val)
                else:
                    mode_val = self.df_clean[col].mode()[0] if not self.df_clean[col].mode().empty else 'Unknown'
                    self.df_clean[col] = self.df_clean[col].fillna(mode_val)

        self.df_clean['fecha'] = pd.to_datetime(self.df_clean['fecha'], errors='coerce')
        return self.df_clean

    def create_derived_columns(self) -> pd.DataFrame:
        if self.df_clean is None:
            self.clean_data()

        self.df_prepared = self.df_clean.copy()

        self.df_prepared['monto_log'] = np.log1p(self.df_prepared['monto'])
        self.df_prepared['es_ingreso'] = (self.df_prepared['tipo_movimiento'] == 'Ingreso').astype(int)

        self.df_prepared['mes'] = self.df_prepared['fecha'].dt.month
        self.df_prepared['dia_semana'] = self.df_prepared['fecha'].dt.dayofweek
        self.df_prepared['es_fin_semana'] = (self.df_prepared['dia_semana'] >= 5).astype(int)

        return self.df_prepared

    def encode_categorical_variables(self) -> pd.DataFrame:
        if self.df_prepared is None:
            self.create_derived_columns()

        df_encoded = self.df_prepared.copy()

        categorical_cols = ['categoria', 'tipo_movimiento', 'cuenta']
        for col in categorical_cols:
            if col in df_encoded.columns:
                dummies = pd.get_dummies(df_encoded[col], prefix=col, dtype=int)
                df_encoded = pd.concat([df_encoded, dummies], axis=1)

        self.df_prepared = df_encoded
        return self.df_prepared

    def prepare_full_pipeline(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        self.load_data()
        self.perform_eda()
        self.clean_data()
        self.create_derived_columns()
        self.encode_categorical_variables()

        return self.df_prepared, self.eda_findings

    def save_prepared_data(self, output_path: str = 'data_prepared.csv'):
        if self.df_prepared is not None:
            self.df_prepared.to_csv(output_path, index=False)
        else:
            raise ValueError("No hay datos preparados para guardar. Ejecute prepare_full_pipeline() primero.")
