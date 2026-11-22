"""Modelo candidato que se va a comparar durante el entrenamiento."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CandidateModel:
    """Nombre y pipeline de Scikit-Learn de un modelo candidato.

    Attributes:
        name: Nombre legible que se muestra en las tablas.
        model: Pipeline ya configurado, listo para recibir ``fit``.
    """

    name: str
    model: Any
