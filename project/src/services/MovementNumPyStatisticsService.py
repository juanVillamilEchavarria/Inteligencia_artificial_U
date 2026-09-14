import numpy as np
from api.MovementsGateWay import MovementsGateWay
from app_collections.MovementsCollection import MovementsCollection
from enums.MovementFilteringKeys import MovementFilteringKeys
from entities.Movement import Movement
from dto.MovementNumPyDTO import MovementNumPyDTO


class MovementNumPyStatisticsService:
    """
    Servicio de estadísticas usando NumPy.
    para el análisis exploratorio de datos (EDA).
    """

    def __init__(self):
        self.movements: MovementsCollection = MovementsGateWay.getData()


    def getAmountsArray(self) -> np.ndarray:
        """Retorna todos los montos como array NumPy."""
        return np.array([mov.monto for mov in self.movements.getItems()])

    def getExpensesAmountsArray(self) -> np.ndarray:
        """Retorna solo los montos de gastos como array NumPy."""
        expenses = self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Gasto')
        return np.array([mov.monto for mov in expenses])

    def getIncomesAmountsArray(self) -> np.ndarray:
        """Retorna solo los montos de ingresos como array NumPy."""
        incomes = self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Ingreso')
        return np.array([mov.monto for mov in incomes])

    def getEncodedTypesArray(self) -> np.ndarray:
        """
        Codifica tipo_movimiento como array numérico.
        Ingreso = 1, Gasto = 0
        """
        return np.array([
            1 if mov.tipo_movimiento == 'Ingreso' else 0
            for mov in self.movements.getItems()
        ])

    def getEncodedCategoriesArray(self) -> np.ndarray:
        """
        Codifica categorías como array numérico usando np.unique.
        Retorna el array codificado y las etiquetas originales.
        """
        categories = [mov.categoria for mov in self.movements.getItems()]
        unique_cats = sorted(list(set(categories)))
        cat_to_num = {cat: i for i, cat in enumerate(unique_cats)}
        return np.array([cat_to_num[c] for c in categories]), unique_cats


    def getStatsForArray(self, data: np.ndarray) -> MovementNumPyDTO:
        """Calcula todas las estadísticas requeridas para un array."""
        if len(data) == 0:
            return MovementNumPyDTO(0, 0, 0, 0, 0, 0, 0)
        return MovementNumPyDTO(
            np.median(data),
            np.mean(data),
            np.std(data),
            np.min(data),
            np.max(data),
            len(data),
            np.sum(data)
        )

    def getAllExpensesStats(self) -> MovementNumPyDTO:
        """Estadísticas completas de gastos."""
        return self.getStatsForArray(self.getExpensesAmountsArray())

    def getAllIncomesStats(self) -> MovementNumPyDTO:
        """Estadísticas completas de ingresos."""
        return self.getStatsForArray(self.getIncomesAmountsArray())

    def getAllAmountsStats(self) -> MovementNumPyDTO:
        """Estadísticas completas de todos los montos."""
        return self.getStatsForArray(self.getAmountsArray())

    def getStatsByCategory(self) -> dict[str,MovementNumPyDTO]:
        """Estadísticas de gastos agrupadas por categoría."""
        expenses = self.movements.getByKey(MovementFilteringKeys.TIPO_MOVIMIENTO, 'Gasto')
        categories = list(set(mov.categoria for mov in expenses))
        result = {}
        for cat in sorted(categories):
            amounts = np.array([mov.monto for mov in expenses if mov.categoria == cat])
            result[cat] = self.getStatsForArray(amounts)
        return result