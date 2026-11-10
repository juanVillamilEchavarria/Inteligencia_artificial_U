"""Punto único de acceso al dataset de cultivos."""

from pathlib import Path

import pandas as pd

from app_collections.CropLotsCollection import CropLotsCollection
from helpers.project_paths import CROP_DATASET_PATH


class CropDataGateway:
    """Lee el CSV de cultivos y lo entrega como colección de dominio."""

    def __init__(self, data_path: Path = CROP_DATASET_PATH):
        """Guarda la ruta del archivo que se va a leer."""
        self._data_path = Path(data_path)

    def get_data(self) -> CropLotsCollection:
        """Carga el CSV y devuelve una colección de lotes.

        Raises:
            FileNotFoundError: Si el archivo no existe en la ruta indicada.
        """
        if not self._data_path.exists():
            raise FileNotFoundError(
                f"No se encontró el dataset de cultivos en {self._data_path}. "
                "Verifique la carpeta data/ de clase_12."
            )
        dataframe = pd.read_csv(self._data_path)
        return CropLotsCollection.from_dataframe(dataframe)
