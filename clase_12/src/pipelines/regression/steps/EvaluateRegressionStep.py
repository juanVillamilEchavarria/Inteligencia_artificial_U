"""Paso que evalúa la regresión con los datos de prueba."""

from dataclasses import replace

from pipelines.core.PipelineStep import PipelineStep
from pipelines.regression.RegressionContext import RegressionContext
from services.RegressionService import RegressionService


class EvaluateRegressionStep(PipelineStep[RegressionContext]):
    """Predice y calcula MAE, RMSE, R² y coeficientes."""

    @property
    def name(self) -> str:
        """Nombre del paso dentro del pipeline."""
        return "Evaluación de la regresión"

    def execute(self, context: RegressionContext) -> RegressionContext:
        """Genera las predicciones y el reporte de regresión."""
        data = context.data
        if (
            data is None
            or data.X_train is None
            or data.X_test is None
            or data.y_train is None
            or data.y_test is None
            or data.y is None
            or context.model is None
        ):
            raise ValueError(
                "EvaluateRegressionStep requiere datos, divisiones y modelo."
            )

        yPredicted = RegressionService.predict(context.model, data.X_test)
        report = RegressionService.build_report(
            model=context.model,
            y_test=data.y_test,
            y_predicted=yPredicted,
            feature_names=data.featureNames,
            train_count=len(data.X_train),
            test_count=len(data.X_test),
            average_yield=float(data.y.mean()),
        )
        return replace(
            context,
            yPredicted=yPredicted,
            report=report,
        )
