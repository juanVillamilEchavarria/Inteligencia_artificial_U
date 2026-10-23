"""Contrato común para los pasos de preparación de datos."""

from abc import ABC, abstractmethod

from pipelines.transform.DataPreparationContext import DataPreparationContext


class DataPreparationStep(ABC):
    """Define el nombre y la operación que debe implementar cada paso."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre que se muestra al ejecutar el pipeline."""
        pass

    @abstractmethod
    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        """Recibe el contexto, realiza su tarea y devuelve el contexto actualizado."""
        pass
