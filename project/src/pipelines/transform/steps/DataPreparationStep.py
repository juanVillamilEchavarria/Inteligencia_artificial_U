from abc import ABC, abstractmethod

from pipelines.transform.DataPreparationContext import DataPreparationContext


class DataPreparationStep(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, context: DataPreparationContext) -> DataPreparationContext:
        pass