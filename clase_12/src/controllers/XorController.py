"""Fachada para ejecutar el experimento XOR."""

from pipelines.xor.XorContext import XorContext
from pipelines.xor.XorRunner import XorRunner


class XorController:
    """Coordina la ejecución del experimento de la compuerta XOR."""

    def __init__(self, runner: XorRunner):
        """Recibe el runner del experimento."""
        self._runner = runner

    def run(self) -> XorContext:
        """Ejecuta el experimento y devuelve el contexto resultante."""
        return self._runner.run()
