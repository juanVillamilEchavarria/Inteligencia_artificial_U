"""Menú interactivo en consola para usar el modelo guardado."""

from pathlib import Path

import pandas as pd

from controllers.ModelController import ModelController
from helpers.output_helpers import print_separator
from helpers.project_paths import (
    MODEL_CHARTS_DIR,
    MODEL_METRICS_PATH,
    MODEL_PATH,
)
from services.ModelPersistenceService import ModelPersistenceService


def askFloat(prompt: str) -> float:
    """Pide un número decimal y repite hasta recibir uno válido."""
    while True:
        try:
            return float(input(prompt).strip().replace(",", ""))
        except ValueError:
            print("  Valor inválido. Escribe un número, por ejemplo 250000.")


def askInt(prompt: str, minimum: int, maximum: int) -> int:
    """Pide un entero dentro de un rango y repite hasta recibir uno válido."""
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum <= value <= maximum:
                return value
            print(f"  El valor debe estar entre {minimum} y {maximum}.")
        except ValueError:
            print(f"  Valor inválido. Escribe un entero entre {minimum} y {maximum}.")


def printPredictions(predictions) -> None:
    """Muestra una tabla con las predicciones del modelo."""
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
    print("\n" + table.to_string(index=False))


def showMetrics(controller: ModelController) -> None:
    """Muestra la comparación de modelos guardada en el JSON de métricas."""
    try:
        metrics = controller.loadMetrics()
    except FileNotFoundError as error:
        print(f"\n{error}")
        return

    print(f"\nMejor modelo: {metrics['modelName']}")
    print(f"Entrenamiento: {metrics['trainCount']} filas | Prueba: {metrics['testCount']} filas")
    if metrics.get("bestParams"):
        print(f"Hiperparámetros: {metrics['bestParams']}")

    table = pd.DataFrame(
        [
            {
                "Modelo": score["modelName"],
                "Exactitud": round(score["accuracy"], 4),
                "Precisión": round(score["precision"], 4),
                "Recall": round(score["recall"], 4),
                "F1 macro": round(score["f1Macro"], 4),
                "F1 Ingreso": round(score["f1Class1"], 4),
                "ROC-AUC": round(score["rocAuc"], 4),
                "CV F1 macro": round(score["crossValidationMean"], 4),
            }
            for score in metrics["models"]
        ]
    )
    print("\n" + table.to_string(index=False))


def showModelInfo(payload: dict) -> None:
    """Muestra la metadata del modelo y las rutas de los gráficos."""
    print(f"\nModelo: {payload['modelName']}")
    print(f"Variables: {', '.join(payload['featureNames'])}")
    print(f"Objetivo: {payload['targetName']}")
    print(f"Archivo del modelo: {MODEL_PATH}")
    print(f"Archivo de métricas: {MODEL_METRICS_PATH}")

    charts = sorted(Path(MODEL_CHARTS_DIR).glob("*.png"))
    if charts:
        print("\nGráficos de evaluación disponibles:")
        for chart in charts:
            print(f"  - {chart}")
    else:
        print("\nTodavía no hay gráficos. Ejecuta: python src/modelo_proyecto.py")


def main() -> None:
    """Ejecuta el menú hasta que el usuario decida salir."""
    print_separator("LEO COUNTER AI - INTERFAZ DE PREDICCIÓN")

    controller = ModelController(
        storage=ModelPersistenceService(MODEL_PATH, MODEL_METRICS_PATH)
    )

    try:
        payload = controller.loadModel()
    except FileNotFoundError as error:
        print(f"\n{error}")
        print("Después de entrenar, vuelve a ejecutar este menú.")
        return

    print(f"\nModelo cargado: {payload['modelName']}")

    sampleCases = [
        (85000.0, 6, 2),
        (3500000.0, 4, 1),
        (250000.0, 11, 6),
        (45000.0, 12, 5),
    ]

    while True:
        print("\n" + "-" * 60)
        print("  1. Predecir un movimiento nuevo")
        print("  2. Probar un lote de ejemplo")
        print("  3. Ver comparación de modelos")
        print("  4. Ver información del modelo y gráficos")
        print("  5. Salir")
        print("-" * 60)

        try:
            option = input("Elige una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if option == "1":
            print("\nIngresa los datos del movimiento:")
            monto = askFloat("  Monto en pesos: ")
            mes = askInt("  Mes (1-12): ", 1, 12)
            dia = askInt("  Día de la semana (0 = lunes, 6 = domingo): ", 0, 6)
            try:
                predictions = controller.predictNewCases([(monto, mes, dia)])
                printPredictions(predictions)
            except ValueError as error:
                print(f"\n  No se pudo predecir: {error}")
        elif option == "2":
            printPredictions(controller.predictNewCases(sampleCases))
        elif option == "3":
            showMetrics(controller)
        elif option == "4":
            showModelInfo(payload)
        elif option == "5":
            print("\nHasta luego.")
            break
        else:
            print("\n  Opción inválida. Elige un número del 1 al 5.")


if __name__ == "__main__":
    main()
