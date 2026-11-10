"""Orquestador genérico de pasos con estado inmutable."""

from typing import Generic, Sequence, TypeVar

from pipelines.core.PipelineStep import PipelineStep

ContextType = TypeVar("ContextType")


class Pipeline(Generic[ContextType]):
    """Ejecuta una secuencia de pasos sobre un contexto."""

    def __init__(self, steps: Sequence[PipelineStep[ContextType]]):
        """Recibe los pasos en el orden en que deben ejecutarse."""
        self._steps = tuple(steps)

    def run(self, context: ContextType) -> ContextType:
        """Ejecuta todos los pasos y devuelve el contexto final."""
        for step in self._steps:
            print(f"  → {step.name}")
            context = step.execute(context)
        return context
