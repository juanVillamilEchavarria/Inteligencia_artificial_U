"""Paso que divide los datos en entrenamiento y prueba."""

from dataclasses import replace

from sklearn.model_selection import train_test_split

from pipelines.core.PipelineStep import PipelineStep
from pipelines.transform.DataPreparationContext import DataPreparationContext


class SplitDataStep(PipelineStep[DataPreparationContext]):
    """Separa X e y dejando un porcentaje aparte para evaluar."""

    def __init__(
        self,
        testSize: float = 0.2,
        randomState: int = 42,
        stratify: bool = True,
    ):
        """Configura el tamaño de prueba, la semilla y la estratificación."""
        self._testSize = testSize
        self._randomState = randomState
        self._stratify = stratify

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "División entrenamiento / prueba"

    def execute(
        self, context: DataPreparationContext
    ) -> DataPreparationContext:
        """Divide los datos y guarda los cuatro conjuntos en el contexto."""
        if context.X is None or context.y is None:
            raise ValueError(
                "SplitDataStep requiere X e y (falta SelectFeaturesStep?)"
            )

        stratifyValues = context.y if self._stratify else None
        X_train, X_test, y_train, y_test = train_test_split(
            context.X,
            context.y,
            test_size=self._testSize,
            random_state=self._randomState,
            stratify=stratifyValues,
        )

        metadata = dict(context.metadata)
        metadata["trainCount"] = len(X_train)
        metadata["testCount"] = len(X_test)

        return replace(
            context,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            metadata=metadata,
        )
