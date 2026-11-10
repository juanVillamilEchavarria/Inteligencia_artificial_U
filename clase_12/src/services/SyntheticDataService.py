"""Generación de los datos simulados de rendimiento de cultivos."""

import numpy as np
import pandas as pd

from enums.CropColumns import RegressionColumns


class SyntheticDataService:
    """Crea el dataset de regresión con una semilla reproducible."""

    @staticmethod
    def generate_yield_data(n: int = 150, seed: int = 7) -> pd.DataFrame:
        """Genera 150 registros con la fórmula usada en la clase 12."""
        generator = np.random.default_rng(seed=seed)

        precipitation = RegressionColumns.PRECIPITACION_MM.value
        temperature = RegressionColumns.TEMPERATURA_C.value
        fertilizer = RegressionColumns.FERTILIZANTE_KG_HA.value
        yield_column = RegressionColumns.RENDIMIENTO_KG_HA.value

        dataframe = pd.DataFrame(
            {
                precipitation: generator.uniform(40, 260, n).round(1),
                temperature: generator.uniform(21, 31, n).round(1),
                fertilizer: generator.uniform(50, 300, n).round(0),
            }
        )

        dataframe[yield_column] = (
            2000
            + 6.0 * dataframe[precipitation]
            - 90.0 * (dataframe[temperature] - 26)
            + 3.0 * dataframe[fertilizer]
            + generator.normal(0, 180, n)
        ).round(0)

        return dataframe
