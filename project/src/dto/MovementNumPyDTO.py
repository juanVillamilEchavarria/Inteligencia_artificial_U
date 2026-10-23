"""DTO con las estadísticas principales de un conjunto de montos."""


class MovementNumPyDTO:
    """Resume las medidas descriptivas calculadas sobre un arreglo de montos."""

    def __init__(self, median, average, std, min, max, count, sum):
        """Guarda los valores calculados para consultarlos desde otras capas."""
        self.median = median
        self.average = average
        self.std = std
        self.min = min
        self.max = max
        self.count = count
        self.sum = sum
