"""Experimento de la compuerta XOR con una neurona y una red neuronal."""

from typing import Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from pipelines.xor.dtos.XorReport import XorReport, XorRow


class XorService:
    """Entrena y compara los dos modelos que resuelven XOR."""

    @staticmethod
    def get_xor_data() -> Tuple[np.ndarray, np.ndarray]:
        """Devuelve las cuatro combinaciones de XOR y su salida esperada."""
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 1, 0])
        return X, y

    @staticmethod
    def train_single_neuron(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
        """Entrena una sola neurona, equivalente a la regresión logística."""
        model = LogisticRegression()
        model.fit(X, y)
        return model

    @staticmethod
    def train_network(X: np.ndarray, y: np.ndarray) -> MLPClassifier:
        """Entrena una red con una capa oculta de cuatro neuronas."""
        model = MLPClassifier(
            hidden_layer_sizes=(4,),
            activation="tanh",
            solver="lbfgs",
            max_iter=1000,
            random_state=1,
        )
        model.fit(X, y)
        return model

    @staticmethod
    def build_report(
        X: np.ndarray,
        y: np.ndarray,
        single_neuron: LogisticRegression,
        network: MLPClassifier,
    ) -> XorReport:
        """Compara las predicciones y exactitudes de los dos modelos."""
        neuron_predictions = single_neuron.predict(X)
        network_predictions = network.predict(X)

        rows = tuple(
            XorRow(
                x1=int(X[index, 0]),
                x2=int(X[index, 1]),
                expected=int(y[index]),
                singleNeuron=int(neuron_predictions[index]),
                network=int(network_predictions[index]),
            )
            for index in range(len(X))
        )

        return XorReport(
            rows=rows,
            singleNeuronAccuracy=float(single_neuron.score(X, y)),
            networkAccuracy=float(network.score(X, y)),
        )
