"""Paso de análisis exploratorio sobre los datos sin limpiar."""

from dataclasses import replace

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.dtos.EdaReport import EdaReport
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class EdaStep(DataPreparationStep):
    """Calcula distribuciones, nulos, duplicados y correlaciones del dataset original."""

    NUMERIC_COLUMNS = ("toneladas_recogidas", "distancia_km", "ruta_retrasada")

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "EDA"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Genera el reporte EDA y lo agrega al contexto."""
        df = context.dfRaw
        if df is None:
            raise ValueError("EdaStep requiere dfRaw cargado (falta LoadDataStep?)")

        numericSummary = {}
        for column in self.NUMERIC_COLUMNS:
            series = df[column]
            numericSummary[column] = {
                "mean": float(series.mean()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
                "median": float(series.median()),
            }

        correlations = df[list(self.NUMERIC_COLUMNS)].corr()
        report = EdaReport(
            shape=df.shape,
            nullCounts={key: int(value) for key, value in df.isnull().sum().items()},
            totalNulls=int(df.isnull().sum().sum()),
            dtypes=df.dtypes.astype(str).to_dict(),
            duplicatesExact=int(df.duplicated().sum()),
            duplicatesById=int(df["recorrido_id"].duplicated().sum()),
            uniqueRoutes=int(df["ruta"].nunique()),
            routeDist={
                str(key): int(value)
                for key, value in df["ruta"].value_counts().items()
            },
            targetDist={
                int(key): int(value)
                for key, value in df["ruta_retrasada"].value_counts().sort_index().items()
            },
            numericSummary=numericSummary,
            correlations={
                "toneladasVsRetraso": float(correlations.loc["toneladas_recogidas", "ruta_retrasada"]),
                "distanciaVsRetraso": float(correlations.loc["distancia_km", "ruta_retrasada"]),
                "toneladasVsDistancia": float(correlations.loc["toneladas_recogidas", "distancia_km"]),
            },
            head=df.head().to_dict(),
            describe=df.describe(include="all").to_dict(),
        )
        return replace(context, edaReport=report)
