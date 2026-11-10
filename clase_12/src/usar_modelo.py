"""Paso 2: usar el modelo guardado para predecir lotes nuevos."""

import pandas as pd

from controllers.ClassificationController import ClassificationController
from helpers.output_helpers import print_separator
from helpers.project_paths import CLASSIFICATION_MODEL_PATH
from pipelines.classification.ClassificationRunner import ClassificationRunner
from services.ModelPersistenceService import ModelPersistenceService


def main() -> None:
    """Carga el modelo y predice tres lotes de ejemplo."""
    print_separator("CLASE 12 - USO DEL MODELO GUARDADO")

    controller = ClassificationController(
        runner=ClassificationRunner(modelPath=CLASSIFICATION_MODEL_PATH),
        storage=ModelPersistenceService(CLASSIFICATION_MODEL_PATH),
    )

    lotesNuevos = [
        (220.0, 23.5),
        (60.0, 30.0),
        (150.0, 26.0),
    ]
    predictions = controller.predictNewCases(lotesNuevos)

    table = pd.DataFrame(
        [
            {
                "precipitacion_mm": prediction.precipitacion_mm,
                "temperatura_c": prediction.temperatura_c,
                "probabilidad_exito_%": round(prediction.probability * 100, 1),
                "resultado": (
                    "Exitosa" if prediction.label == 1 else "No exitosa"
                ),
            }
            for prediction in predictions
        ]
    )

    print("Predicciones con el modelo guardado:")
    print(table.to_string(index=False))
    print_separator("PREDICCIÓN COMPLETADA")


if __name__ == "__main__":
    main()
