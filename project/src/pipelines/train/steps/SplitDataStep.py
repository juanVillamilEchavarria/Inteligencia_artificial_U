"""Paso que divide el dataset en entrenamiento y prueba."""

from dataclasses import replace

from sklearn.model_selection import train_test_split

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep


class SplitDataStep(TrainingStep):
    """Separa las filas antes de estandarizar y entrenar."""

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

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Divide X e y manteniendo la proporción de clases."""
        if context.X is None or context.y is None:
            raise ValueError("SplitDataStep requiere X e y (falta SelectFeaturesStep?)")
        if len(set(context.y.tolist())) < 2:
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

        return replace(
            context,
            XTrain=XTrain,
            XTest=XTest,
            yTrain=yTrain,
            yTest=yTest,
            metadata=metadata,
        )
