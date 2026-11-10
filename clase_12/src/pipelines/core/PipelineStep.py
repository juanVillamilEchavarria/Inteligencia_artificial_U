"""Contrato común para los pasos de un pipeline."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ContextType = TypeVar("ContextType")


class PipelineStep(ABC, Generic[ContextType]):
    """Define el nombre y la operación que debe implementar cada paso."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre que se muestra al ejecutar el pipeline."""
        pass

    @abstractmethod
    def execute(self, context: ContextType) -> ContextType:
        """Recibe el contexto, realiza su tarea y devuelve el contexto actualizado."""
        pass
