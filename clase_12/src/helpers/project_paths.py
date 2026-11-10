"""Rutas compartidas para ejecutar el proyecto desde cualquier directorio."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
CHARTS_DIR = SRC_DIR / "charts"
MODELS_DIR = SRC_DIR / "models"

CROP_DATASET_PATH = DATA_DIR / "cultivos_cartago.csv"
REGRESSION_DATASET_PATH = DATA_DIR / "rendimiento_cartago.csv"

CLASSIFICATION_MODEL_PATH = MODELS_DIR / "modelo_cultivos.joblib"

CONFUSION_MATRIX_PATH = CHARTS_DIR / "matriz_confusion.png"
REGRESSION_PLOT_PATH = CHARTS_DIR / "real_vs_predicho.png"
OVERFITTING_PLOT_PATH = CHARTS_DIR / "sobreajuste_arbol.png"
