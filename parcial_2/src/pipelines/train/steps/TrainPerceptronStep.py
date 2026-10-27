"""Paso que entrena el perceptrón con las entradas ya estandarizadas."""

from dataclasses import replace

from pipelines.train.PerceptronTrainingContext import PerceptronTrainingContext
from pipelines.train.steps.TrainingStep import TrainingStep
from services.PerceptronService import PerceptronService


class TrainPerceptronStep(TrainingStep):
    """Ejecuta el descenso de gradiente y guarda el modelo entrenado."""

    def __init__(self, learningRate: float = 0.1, epochs: int = 500):
        """Configura la tasa de aprendizaje y el número de épocas."""
        self._learningRate = learningRate
        self._epochs = epochs

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Entrenamiento del perceptrón"

    def execute(self, context: PerceptronTrainingContext) -> PerceptronTrainingContext:
        """Entrena el modelo y agrega el resultado al contexto."""
        if context.XScaled is None or context.y is None:
            raise ValueError("TrainPerceptronStep requiere XScaled e y (falta StandardizeStep?)")

        training = PerceptronService.train(
            context.XScaled,
            context.y,
            learningRate=self._learningRate,
            epochs=self._epochs,
        )
        return replace(context, training=training)
