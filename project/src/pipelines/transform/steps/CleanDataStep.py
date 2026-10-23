"""Paso de limpieza y normalización del dataset original."""

from dataclasses import replace

import pandas as pd

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.dtos.CleaningReport import CleaningReport, ImputationRecord
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class CleanDataStep(DataPreparationStep):
    """Convierte tipos, descarta registros inválidos y completa nulos."""

    TEXT_COLUMNS = (
        "id",
        "nombre",
        "cuenta",
        "categoria",
        "tipo_movimiento",
        "descripcion",
    )

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Limpieza de datos"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Limpia el dataframe y registra cada cambio en el reporte."""
        if context.dfRaw is None:
            raise ValueError("CleanDataStep requiere dfRaw cargado (falta LoadDataStep?)")

        dfClean = context.dfRaw.copy()
        rowsBefore = len(dfClean)
        columnsBefore = len(dfClean.columns)
        nullsBefore = int(dfClean.isnull().sum().sum())

        normalizedColumns = self._normalizeTextColumns(dfClean)

        dfClean["monto"] = pd.to_numeric(dfClean["monto"], errors="coerce")
        invalidAmountMask = dfClean["monto"].isna() | (dfClean["monto"] <= 0)
        invalidAmountsRemoved = int(invalidAmountMask.sum())
        dfClean = dfClean.loc[~invalidAmountMask].copy()

        fechaConverted = False
        invalidDatesRemoved = 0
        if "fecha" in dfClean.columns:
            dfClean["fecha"] = pd.to_datetime(dfClean["fecha"], errors="coerce")
            invalidDateMask = dfClean["fecha"].isna()
            invalidDatesRemoved = int(invalidDateMask.sum())
            dfClean = dfClean.loc[~invalidDateMask].copy()
            fechaConverted = True

        rowsBeforeDuplicates = len(dfClean)
        dfClean = dfClean.drop_duplicates().copy()
        duplicatesRemoved = rowsBeforeDuplicates - len(dfClean)

        imputations = self._imputeNulls(dfClean)
        outliersKept = self._countOutliersIqr(dfClean["monto"])

        report = CleaningReport(
            rowsBefore=rowsBefore,
            rowsAfter=len(dfClean),
            columnsBefore=columnsBefore,
            columnsAfter=len(dfClean.columns),
            nullsBefore=nullsBefore,
            nullsAfter=int(dfClean.isnull().sum().sum()),
            duplicatesRemoved=duplicatesRemoved,
            imputations=tuple(imputations),
            fechaConverted=fechaConverted,
            normalizedColumns=tuple(normalizedColumns),
            outliersKept=outliersKept,
            invalidDatesRemoved=invalidDatesRemoved,
            invalidAmountsRemoved=invalidAmountsRemoved,
        )
        return replace(context, dfClean=dfClean, cleaningReport=report)

    def _normalizeTextColumns(self, df: pd.DataFrame) -> list[str]:
        """Quita espacios repetidos y extremos en las columnas de texto."""
        normalized = []
        for column in self.TEXT_COLUMNS:
            if column not in df.columns:
                continue
            df[column] = (
                df[column]
                .astype("string")
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
            )
            normalized.append(column)
        return normalized

    def _imputeNulls(self, df: pd.DataFrame) -> list[ImputationRecord]:
        """Completa nulos con la mediana o la moda según el tipo de columna."""
        imputations = []
        for column in df.columns:
            nullCount = int(df[column].isnull().sum())
            if nullCount == 0:
                continue

            if pd.api.types.is_numeric_dtype(df[column]):
                filledValue = float(df[column].median())
                df[column] = df[column].fillna(filledValue)
                strategy = "median"
            else:
                modeSeries = df[column].mode()
                filledValue = modeSeries[0] if not modeSeries.empty else "Unknown"
                df[column] = df[column].fillna(filledValue)
                strategy = "mode"

            imputations.append(
                ImputationRecord(
                    column=column,
                    strategy=strategy,
                    filledValue=filledValue,
                    nullsCount=nullCount,
                )
            )
        return imputations

    def _countOutliersIqr(self, series: pd.Series) -> int:
        """Cuenta los montos fuera de los límites de 1.5 veces el IQR."""
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return int(((series < lower) | (series > upper)).sum())
