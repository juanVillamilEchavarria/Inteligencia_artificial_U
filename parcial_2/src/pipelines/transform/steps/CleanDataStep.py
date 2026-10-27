"""Paso de limpieza y normalización del dataset original."""

from dataclasses import replace

import pandas as pd

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.dtos.CleaningReport import (
    CleaningReport,
    CorrectionRecord,
    ImputationRecord,
)
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class CleanDataStep(DataPreparationStep):
    """Convierte tipos, corrige valores inválidos y completa nulos."""

    TEXT_COLUMNS = ("recorrido_id", "ruta")
    NUMERIC_COLUMNS = ("toneladas_recogidas", "distancia_km", "ruta_retrasada")
    FEATURE_COLUMNS = ("toneladas_recogidas", "distancia_km")

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
        targetCountsBefore = {
            int(key): int(value)
            for key, value in dfClean["ruta_retrasada"].value_counts().sort_index().items()
        }
        meanBefore = float(dfClean["toneladas_recogidas"].mean())
        stdBefore = float(dfClean["toneladas_recogidas"].std())

        normalizedColumns = self._normalizeTextColumns(dfClean)

        for column in self.NUMERIC_COLUMNS:
            dfClean[column] = pd.to_numeric(dfClean[column], errors="coerce")

        corrections = self._correctInvalidValues(dfClean)

        duplicateIds = tuple(
            dfClean.loc[dfClean.duplicated(keep="first"), "recorrido_id"].tolist()
        )
        rowsBeforeDuplicates = len(dfClean)
        dfClean = dfClean.drop_duplicates(keep="first").copy()
        duplicatesRemoved = rowsBeforeDuplicates - len(dfClean)

        imputations = self._imputeNulls(dfClean, self.FEATURE_COLUMNS)

        invalidMask = (
            (dfClean["toneladas_recogidas"] <= 0)
            | (dfClean["distancia_km"] <= 0)
            | (~dfClean["ruta_retrasada"].isin([0, 1]))
        )
        invalidRowsRemoved = int(invalidMask.sum())
        dfClean = dfClean.loc[~invalidMask].copy()
        dfClean["ruta_retrasada"] = dfClean["ruta_retrasada"].astype(int)
        dfClean["toneladas_recogidas"] = dfClean["toneladas_recogidas"].astype(float)
        dfClean["distancia_km"] = dfClean["distancia_km"].astype(float)
        dfClean = dfClean.reset_index(drop=True)

        report = CleaningReport(
            rowsBefore=rowsBefore,
            rowsAfter=len(dfClean),
            columnsBefore=columnsBefore,
            columnsAfter=len(dfClean.columns),
            nullsBefore=nullsBefore,
            nullsAfter=int(dfClean.isnull().sum().sum()),
            duplicatesRemoved=duplicatesRemoved,
            duplicateIds=duplicateIds,
            imputations=tuple(imputations),
            corrections=tuple(corrections),
            invalidRowsRemoved=invalidRowsRemoved,
            normalizedColumns=tuple(normalizedColumns),
            targetCountsBefore=targetCountsBefore,
            targetCountsAfter={
                int(key): int(value)
                for key, value in dfClean["ruta_retrasada"].value_counts().sort_index().items()
            },
            suspiciousColumn="toneladas_recogidas",
            suspiciousValue=float(context.dfRaw["toneladas_recogidas"].max()),
            meanBefore=meanBefore,
            meanAfter=float(dfClean["toneladas_recogidas"].mean()),
            stdBefore=stdBefore,
            stdAfter=float(dfClean["toneladas_recogidas"].std()),
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
                .astype(str)
            )
            normalized.append(column)
        return normalized

    def _correctInvalidValues(self, df: pd.DataFrame) -> list[CorrectionRecord]:
        """Corrige valores imposibles o con unidades equivocadas."""
        corrections = []

        for index in df.index[df["toneladas_recogidas"] > 100]:
            originalValue = float(df.at[index, "toneladas_recogidas"])
            correctedValue = originalValue / 1000.0
            df.at[index, "toneladas_recogidas"] = correctedValue
            corrections.append(
                CorrectionRecord(
                    recorridoId=str(df.at[index, "recorrido_id"]),
                    column="toneladas_recogidas",
                    originalValue=originalValue,
                    correctedValue=correctedValue,
                    reason="Valor en kilogramos exportado como toneladas; se dividió entre 1000.",
                )
            )

        for index in df.index[df["distancia_km"] < 0]:
            originalValue = float(df.at[index, "distancia_km"])
            correctedValue = abs(originalValue)
            df.at[index, "distancia_km"] = correctedValue
            corrections.append(
                CorrectionRecord(
                    recorridoId=str(df.at[index, "recorrido_id"]),
                    column="distancia_km",
                    originalValue=originalValue,
                    correctedValue=correctedValue,
                    reason="La distancia no puede ser negativa; se corrigió el signo.",
                )
            )

        return corrections

    def _imputeNulls(self, df: pd.DataFrame, columns) -> list[ImputationRecord]:
        """Completa nulos numéricos con la mediana de cada columna."""
        imputations = []
        for column in columns:
            nullCount = int(df[column].isnull().sum())
            if nullCount == 0:
                continue
            filledValue = float(df[column].median())
            df[column] = df[column].fillna(filledValue)
            imputations.append(
                ImputationRecord(
                    column=column,
                    strategy="median",
                    filledValue=filledValue,
                    nullsCount=nullCount,
                )
            )
        return imputations
