"""Paso que divide el dataset en entrenamiento y prueba."""

from dataclasses import replace

from sklearn.model_selection import train_test_split

from pipelines.model.ModelTrainingContext import ModelTrainingContext
from pipelines.model.steps.ModelTrainingStep import ModelTrainingStep


class SplitDataStep(ModelTrainingStep):
    """Separa las filas antes de entrenar para evaluar con datos no vistos."""

    def __init__(self, testSize: float = 0.25, randomState: int = 42):
        """Define el tamaño del conjunto de prueba y la semilla."""
        if not 0 < testSize < 1:
            raise ValueError("testSize debe estar entre 0 y 1.")
        self._testSize = testSize
        self._randomState = randomState

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "División entrenamiento / prueba"

    def execute(self, context: ModelTrainingContext) -> ModelTrainingContext:
        """Divide X e y manteniendo la proporción de clases."""
        if context.X is None or context.y is None:
            raise ValueError(
                "SplitDataStep requiere X e y (falta SelectFeaturesStep?)"
            )
        if context.y.nunique() < 2:
            raise ValueError("La variable objetivo necesita al menos dos clases.")

        XTrain, XTest, yTrain, yTest = train_test_split(
            context.X,
            context.y,
            test_size=self._testSize,
            stratify=context.y,
            random_state=self._randomState,
        )

        metadata = dict(context.metadata)
        metadata["trainCount"] = len(XTrain)
        metadata["testCount"] = len(XTest)
        metadata["testSize"] = self._testSize
        metadata["randomState"] = self._randomState

        return replace(
            context,
            XTrain=XTrain,
            XTest=XTest,
            yTrain=yTrain,
            yTest=yTest,
            metadata=metadata,
        )
