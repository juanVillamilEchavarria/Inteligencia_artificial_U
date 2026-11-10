"""Composición del pipeline del experimento XOR."""

from pipelines.core.Pipeline import Pipeline
from pipelines.xor.XorContext import XorContext
from pipelines.xor.steps.BuildXorReportStep import BuildXorReportStep
from pipelines.xor.steps.LoadXorDataStep import LoadXorDataStep
from pipelines.xor.steps.TrainNetworkStep import TrainNetworkStep
from pipelines.xor.steps.TrainSingleNeuronStep import TrainSingleNeuronStep


class XorRunner:
    """Arma y ejecuta el experimento de la compuerta XOR."""

    def __init__(self):
        """Configura los pasos del experimento."""
        self._pipeline = Pipeline(
            [
                LoadXorDataStep(),
                TrainSingleNeuronStep(),
                TrainNetworkStep(),
                BuildXorReportStep(),
            ]
        )

    def run(self) -> XorContext:
        """Ejecuta el experimento y entrega el contexto resultante."""
        return self._pipeline.run(XorContext())
