"""DTOs con los resultados del análisis exploratorio de datos."""

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class OutlierAnalysis:
    """Resultado de detectar valores atípicos con el rango intercuartílico."""

    q1: float
    q3: float
    iqr: float
    lowerBound: float
    upperBound: float
    count: int
    percentage: float


@dataclass(frozen=True)
class IncomeExpenseComparison:
    """Comparación de cantidad y montos entre ingresos y gastos."""

    incomeCount: int
    expenseCount: int
    incomeMean: float
    expenseMean: float
    incomeMedian: float
    expenseMedian: float
    incomeMax: float
    expenseMax: float


@dataclass(frozen=True)
class EdaReport:
    """Resumen completo del dataset antes de aplicar la limpieza."""

    shape: Tuple[int, int]
    nullCounts: Dict[str, int]
    totalNulls: int
    dtypes: Dict[str, str]
    uniqueCategories: int
    uniqueAccounts: int
    tipoMovimientoDist: Dict[str, int]
    categoriaDist: Dict[str, int]
    cuentaDist: Dict[str, int]
    montoSkew: float
    montoKurtosis: float
    outlierAnalysis: OutlierAnalysis
    incomeVsExpense: IncomeExpenseComparison
    head: Dict = field(default_factory=dict)
    describe: Dict = field(default_factory=dict)
