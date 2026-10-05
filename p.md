has violado horriblemente SOLID en el MovementDataPreparationService, esa clase quedo un mounstro que nisiquiera se lee facilmente, es una violacion tremenda a SOLID y clean code, debes de refactorizarlo y colocarlo todo correctamente, primero, el service (MovementDataPreparationService) VIOLA SRP horriblemente, hace muchas cosas, limpiar datos, eda, columnas nuevas, etc, es imposible de extender limpiamente, conforme el proyecto crezca, la deuda tecnica terminara ahogandolo, ahora bien, este es un pipeline de preparacion de datos, cada paso, debe tener una clase dedicada para ello, ademas, guardas estadisticas (findings) en arrays de manera insegura, para eso, se deben crear DTOs, debes de refactorizar todo esto, pues esto es un pipeline, esta es la estructura de carpetas que debes de seguir: 
DataPreparationPipeline.py     # Orquestador
DataPreparationRunner.py     # Orquestador
│       ├── DataPreparationContext.py              # Estado compartido explícito
│       ├── steps/
│       │   ├── DataPreparationStep.py             # ABC
│       │   ├── LoadDataStep.py
│       │   ├── EdaStep.py
│       │   ├── CleanDataStep.py
│       │   ├── FeatureEngineeringStep.py
│       │   ├── EncodingStep.py
│       │   └── PersistStep.py
│       └── dtos/
│           ├── EdaReport.py
│           └── CleaningReport.py


todo esto dentro de la carpeta src/pipelines/transform


es decir, para cada funcion de esto:

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


debe representarse en un step del pipeline.

el runner tendria esto:
class DataPreparationRunner:
    """Ensambla y ejecuta el pipeline de preparación de datos.

    Esta clase es el composition root del pipeline: conoce las dependencias
    concretas (gateway, pasos, orden) y expone una interfaz simple al exterior.
    """

    def __init__(self, output_path: str = "data_prepared.csv"):
        gateway = MovementsGateWay()
        self._pipeline = DataPreparationPipeline(steps=[
            LoadDataStep(gateway),
            EdaStep(),
            CleanDataStep(),
            FeatureEngineeringStep(),
            EncodingStep(),
            PersistStep(output_path),
        ])

    def run(self) -> PipelineContext:
        return self._pipeline.run()


el pipe line haria esto:
class DataPreparationPipeline:
    def __init__(self, steps: List[PipelineStep]):
        self._steps = steps

    def run(self) -> PipelineContext:
        context = PipelineContext()
        for step in self._steps:
            print(f"  → {step.name}")
            context = step.execute(context)
        return context



el PipeLine context seria asi:
@dataclass
class DataPreparationContext:
    """Único estado compartido durante la ejecución del pipeline."""
    df_raw: Optional[pd.DataFrame] = None
    df_clean: Optional[pd.DataFrame] = None
    df_prepared: Optional[pd.DataFrame] = None
    eda_report: Optional[EdaReport] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


un ejemplo de lo que haria cada step (ejemplo con EdaStep):
class EdaStep(PipelineStep):
    @property
    def name(self) -> str:
        return "EDA"

    def execute(self, context: PipelineContext) -> PipelineContext:
        df = context.df_raw
        if df is None:
            raise ValueError("EdaStep requiere df_raw cargado (¿falta LoadDataStep?)")

        report = EdaReport(
            shape=df.shape,
            null_counts=df.isnull().sum().to_dict(),
            total_nulls=int(df.isnull().sum().sum()),
            dtypes=df.dtypes.astype(str).to_dict(),
            unique_categories=df["categoria"].nunique(),
            unique_accounts=df["cuenta"].nunique(),
            monto_skew=float(df["monto"].skew()),
            monto_kurtosis=float(df["monto"].kurtosis()),
            outlier_analysis=self._detect_outliers_iqr(df["monto"]),
            income_vs_expense=self._split_by_tipo(df),
        )
        context.eda_report = report
        return context

    def _detect_outliers_iqr(self, series) -> dict:
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]
        return {
            "q1": float(q1), "q3": float(q3), "iqr": float(iqr),
            "lower_bound": float(lower), "upper_bound": float(upper),
            "count": int(len(outliers)),
            "percentage": float(len(outliers) / len(series) * 100),
        }

    def _split_by_tipo(self, df) -> dict:
        ing = df[df["tipo_movimiento"] == "Ingreso"]["monto"]
        gas = df[df["tipo_movimiento"] == "Gasto"]["monto"]
        return {
            "income_count": len(ing), "expense_count": len(gas),
            "income_mean": float(ing.mean()), "expense_mean": float(gas.mean()),
            "income_median": float(ing.median()), "expense_median": float(gas.median()),
            "income_max": float(ing.max()), "expense_max": float(gas.max()),
        }




Entonces elimina el MovementDataPreparationController, y simplemente llama al DataPreparationRunner en el data_preparation.py 


ademas quiero refactorizar algo, actualmente los services que son de generacion de algo (imagenes, .md, etc) no son SERVICES, LOS SERVICES SON PARA LOGICA DE NEGOCIO, asi que muevelos a una carpeta llamda outputs/ , para los generadores de graficos, estaran dentro de outputs/visualization, y el ReportGenerator estara en outputs/reporting, el resto de servicios que generan estadisticas, simplemente mantenlos en services/ porque realmente SON SERVICES


tambien debes renombrar los archivos :
MovementGraphicsService-> MatploitChartRenderer
MovementNumpyStatisticsService-> NumpyStatisticsService.
MovementSeabornGraphicsService-> SeabornChartRenderer.
MovementStatisticsService-> StatisticsService