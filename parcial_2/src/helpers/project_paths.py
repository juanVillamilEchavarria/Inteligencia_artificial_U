"""Rutas compartidas para no depender del directorio desde donde se ejecuta el proyecto."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
SOURCE_DATA_DIR = SRC_DIR / "data"

SOURCE_DATASET_PATH = SOURCE_DATA_DIR / "grupo_07.csv"
CLEAN_DATASET_PATH = DATA_DIR / "grupo_07_limpio.csv"
SEABORN_CHARTS_DIR = SRC_DIR / "charts_seaborn"
PERCEPTRON_CHARTS_DIR = SRC_DIR / "charts_perceptron"
EDA_SUMMARY_PATH = SRC_DIR / "eda_summary.md"
