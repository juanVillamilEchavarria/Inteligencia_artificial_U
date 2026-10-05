from dataclasses import replace

from pipelines.transform.DataPreparationContext import DataPreparationContext
from pipelines.transform.dtos.EdaReport import (
    EdaReport,
    OutlierAnalysis,
    IncomeExpenseComparison,
)
from pipelines.transform.steps.DataPreparationStep import DataPreparationStep


class EdaStep(DataPreparationStep):
    @property
    def name(self) -> str:
        return "EDA"

    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        df = context.dfRaw
        if df is None:
            raise ValueError("EdaStep requiere dfRaw cargado (falta LoadDataStep?)")

        report = EdaReport(
            shape=df.shape,
            nullCounts=df.isnull().sum().to_dict(),
            totalNulls=int(df.isnull().sum().sum()),
            dtypes=df.dtypes.astype(str).to_dict(),
            uniqueCategories=int(df["categoria"].nunique()),
            uniqueAccounts=int(df["cuenta"].nunique()),
            tipoMovimientoDist=df["tipo_movimiento"].value_counts().to_dict(),
            categoriaDist=df["categoria"].value_counts().to_dict(),
            cuentaDist=df["cuenta"].value_counts().to_dict(),
            montoSkew=float(df["monto"].skew()),
            montoKurtosis=float(df["monto"].kurtosis()),
            outlierAnalysis=self._detectOutliersIqr(df["monto"]),
            incomeVsExpense=self._splitByTipo(df),
            head=df.head().to_dict(),
            describe=df.describe(include="all").to_dict(),
        )
        return replace(context, edaReport=report)

    def _detectOutliersIqr(self, series) -> OutlierAnalysis:
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]
        return OutlierAnalysis(
            q1=float(q1),
            q3=float(q3),
            iqr=float(iqr),
            lowerBound=float(lower),
            upperBound=float(upper),
            count=int(len(outliers)),
            percentage=float(len(outliers) / len(series) * 100),
        )

    def _splitByTipo(self, df) -> IncomeExpenseComparison:
        ing = df[df["tipo_movimiento"] == "Ingreso"]["monto"]
        gas = df[df["tipo_movimiento"] == "Gasto"]["monto"]
        return IncomeExpenseComparison(
            incomeCount=len(ing),
            expenseCount=len(gas),
            incomeMean=float(ing.mean()),
            expenseMean=float(gas.mean()),
            incomeMedian=float(ing.median()),
            expenseMedian=float(gas.median()),
            incomeMax=float(ing.max()),
            expenseMax=float(gas.max()),
        )
