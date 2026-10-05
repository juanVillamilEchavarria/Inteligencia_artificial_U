from dataclasses import replace

import pandas as pd

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.dtos.CleaningReport import CleaningReport, ImputationRecord
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class CleanDataStep(DataPreparationStep):
    @property
    def name(self) -> str:
        return "Limpieza de datos"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        if context.dfRaw is None:
            raise ValueError("CleanDataStep requiere dfRaw cargado (falta LoadDataStep?)")

        dfClean = context.dfRaw.copy()
        imputations = []

        for col in dfClean.columns:
            nullCount = int(dfClean[col].isnull().sum())
            if nullCount == 0:
                continue
            if dfClean[col].dtype in ["float64", "int64"]:
                filledValue = float(dfClean[col].median())
                dfClean[col] = dfClean[col].fillna(filledValue)
                imputations.append(
                    ImputationRecord(
                        column=col,
                        strategy="median",
                        filledValue=filledValue,
                        nullsCount=nullCount,
                    )
                )
            else:
                modeSeries = dfClean[col].mode()
                filledValue = modeSeries[0] if not modeSeries.empty else "Unknown"
                dfClean[col] = dfClean[col].fillna(filledValue)
                imputations.append(
                    ImputationRecord(
                        column=col,
                        strategy="mode",
                        filledValue=str(filledValue),
                        nullsCount=nullCount,
                    )
                )

        fechaConverted = False
        if "fecha" in dfClean.columns:
            dfClean["fecha"] = pd.to_datetime(dfClean["fecha"], errors="coerce")
            fechaConverted = True

        report = CleaningReport(
            rowsBefore=len(context.dfRaw),
            rowsAfter=len(dfClean),
            imputations=tuple(imputations),
            fechaConverted=fechaConverted,
        )
        return replace(context, dfClean=dfClean, cleaningReport=report)
