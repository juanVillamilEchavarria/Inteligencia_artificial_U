"""Contrato común para los pasos del entrenamiento."""

from abc import ABC, abstractmethod

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext


class TrainingStep(ABC):
    """Define el nombre y la operación que debe implementar cada paso."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre que se muestra al ejecutar el pipeline."""
        pass

    @abstractmethod
    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Recibe el contexto, realiza su tarea y devuelve el contexto actualizado."""
        pass
