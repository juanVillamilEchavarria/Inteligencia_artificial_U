from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class OutlierAnalysis:
    q1: float
    q3: float
    iqr: float
    lowerBound: float
    upperBound: float
    count: int
    percentage: float


@dataclass(frozen=True)
class IncomeExpenseComparison:
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