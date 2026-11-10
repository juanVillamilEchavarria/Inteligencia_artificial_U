"""Paso 4: resolver la compuerta XOR con una red neuronal."""

import pandas as pd

from controllers.XorController import XorController
from helpers.output_helpers import print_dataframe, print_separator
from pipelines.xor.XorRunner import XorRunner


def main() -> None:
    """Compara una neurona contra una red con capa oculta."""
    print_separator("CLASE 12 - COMPUERTA XOR")

    context = XorController(XorRunner()).run()
    report = context.report
    if report is None:
        raise RuntimeError("El pipeline no generó el reporte de XOR.")

    table = pd.DataFrame(
        [
            {
                "x1": row.x1,
                "x2": row.x2,
                "Esperado": row.expected,
                "Una neurona": row.singleNeuron,
                "Red neuronal": row.network,
            }
            for row in report.rows
        ]
    )
    print_dataframe("Comparación de modelos para XOR:", table)

    print(f"\nExactitud de una neurona:   {report.singleNeuronAccuracy:.0%}")
    print(f"Exactitud de la red neuronal: {report.networkAccuracy:.0%}")
    print_separator("EXPERIMENTO COMPLETADO")


if __name__ == "__main__":
    main()
