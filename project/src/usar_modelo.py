"""Carga el modelo guardado y predice movimientos nuevos sin reentrenar."""

import pandas as pd

from controllers.ModelController import ModelController
from helpers.output_helpers import print_separator
from helpers.project_paths import MODEL_METRICS_PATH, MODEL_PATH
from services.ModelPersistenceService import ModelPersistenceService


def main():
    """Carga el modelo, muestra su información y clasifica casos de ejemplo."""
    print_separator("USO DEL MODELO GUARDADO - LEO COUNTER AI")

    controller = ModelController(
        storage=ModelPersistenceService(MODEL_PATH, MODEL_METRICS_PATH)
    )

    try:
        payload = controller.loadModel()
    except FileNotFoundError as error:
        print(f"\n{error}")
        return

    print(f"\nModelo: {payload['modelName']}")
    print(f"Variables de entrada: {', '.join(payload['featureNames'])}")
    print(f"Variable objetivo: {payload['targetName']}")
    print(f"Entrenado con: {payload['trainCount']} filas | Probado con: {payload['testCount']} filas")
    if payload.get("bestParams"):
        print(f"Hiperparámetros: {payload['bestParams']}")

    print("\nMétricas de los modelos comparados (conjunto de prueba):")
    metrics = pd.DataFrame(
        [
            {
                "Modelo": score["modelName"],
                "Exactitud": round(score["accuracy"], 4),
                "F1 macro": round(score["f1Macro"], 4),
                "ROC-AUC": round(score["rocAuc"], 4),
                "CV F1 macro": round(score["crossValidationMean"], 4),
            }
            for score in payload["scores"]
        ]
    )
    print(metrics.to_string(index=False))

    newCases = [
        (85000.0, 6, 2),
        (3500000.0, 4, 1),
        (250000.0, 11, 6),
        (45000.0, 12, 5),
    ]
    predictions = controller.predictNewCases(newCases)

    print("\nPredicciones de casos nuevos (monto, mes, día de la semana):")
    table = pd.DataFrame(
        [
            {
                "Monto": f"${prediction.monto:,.0f}",
                "Mes": prediction.mes,
                "Día": prediction.diaSemana,
                "Prob. ingreso": f"{prediction.probability:.2%}",
                "Clase": "Ingreso" if prediction.label == 1 else "Gasto",
            }
            for prediction in predictions
        ]
    )
    print(table.to_string(index=False))

    print_separator("PREDICCIÓN COMPLETADA")


if __name__ == "__main__":
    main()
