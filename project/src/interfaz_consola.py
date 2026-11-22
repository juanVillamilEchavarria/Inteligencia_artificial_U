"""Interfaz interactiva en consola (con Rich) para usar el modelo guardado.

Valor agregado del proyecto final: permite a un usuario de Leo Counter
clasificar movimientos nuevos, revisar la comparación de modelos y entender
qué variables pesan más en la decisión, sin volver a entrenar.

Ejecución:
    docker compose run --rm -it app python src/interfaz_consola.py
"""

import re
from pathlib import Path
from typing import List, Optional

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

from controllers.ModelController import ModelController
from helpers.project_paths import MODEL_CHARTS_DIR, MODEL_METRICS_PATH, MODEL_PATH
from pipelines.model.dtos.ModelPredictionResult import ModelPredictionResult
from services.ModelPersistenceService import ModelPersistenceService
from services.SklearnModelService import SklearnModelService

THEME = Theme(
    {
        "brand": "bold #7C5CFF",
        "accent": "bold #00C2A8",
        "ingreso": "bold #22C55E",
        "gasto": "bold #F43F5E",
        "muted": "grey62",
        "warn": "bold #F59E0B",
        "error": "bold red",
    }
)
console = Console(theme=THEME)


class ConfirmEs(Confirm):
    """Confirmación en español: acepta s (sí) o n (no)."""

    validate_error_message = "[prompt.invalid]Responde s (sí) o n (no)"
    choices = ["s", "n"]


DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MONTHS = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
SAMPLE_CASES = [
    (85000.0, 6, 2),
    (3500000.0, 4, 1),
    (250000.0, 11, 6),
    (45000.0, 12, 5),
]
MENU_OPTIONS = [
    ("1", "Predecir un movimiento nuevo", "Ingresa monto, mes y día"),
    ("2", "Probar un lote de ejemplo", "4 casos listos para la demo"),
    ("3", "Comparar modelos", "Métricas de prueba y validación cruzada"),
    ("4", "Ver el modelo por dentro", "Variables, hiperparámetros y gráficos"),
    ("5", "Salir", ""),
]


# --------------------------------------------------------------------------- #
# Utilidades de formato
# --------------------------------------------------------------------------- #
def formatMoney(value: float) -> str:
    """Formatea un monto en pesos con separador de miles colombiano."""
    return "$" + f"{value:,.0f}".replace(",", ".")


def parseAmount(raw: str) -> Optional[float]:
    """Convierte textos como '250.000', '$3,500,000' o '85000.5' en número."""
    text = raw.strip().replace("$", "").replace(" ", "")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", text):
        text = text.replace(".", "").replace(",", ".")
    else:
        text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return None


def probabilityBar(probability: float, width: int = 24) -> Text:
    """Dibuja una barra horizontal con la probabilidad de ser ingreso."""
    filled = round(probability * width)
    style = "ingreso" if probability >= 0.5 else "gasto"
    bar = Text()
    bar.append("█" * filled, style=style)
    bar.append("░" * (width - filled), style="muted")
    bar.append(f" {probability:6.2%}", style=style)
    return bar


def confidenceLabel(probability: float) -> Text:
    """Traduce la distancia al umbral 0.5 en un nivel de confianza legible."""
    distance = abs(probability - 0.5)
    if distance >= 0.35:
        return Text("Alta", style="ingreso" if probability >= 0.5 else "gasto")
    if distance >= 0.15:
        return Text("Media", style="warn")
    return Text("Baja · revisar manualmente", style="warn")


def classText(label: int) -> Text:
    """Devuelve la clase con su color e ícono."""
    return Text("▲ Ingreso", style="ingreso") if label == 1 else Text("▼ Gasto", style="gasto")


# --------------------------------------------------------------------------- #
# Pantallas
# --------------------------------------------------------------------------- #
def showHeader(payload: dict) -> None:
    """Muestra el encabezado con el nombre del sistema y el modelo cargado."""
    title = Text("LEO COUNTER AI", style="brand", justify="center")
    subtitle = Text(
        "Clasificación inteligente de movimientos financieros · Cartago, Valle",
        style="muted",
        justify="center",
    )
    status = Text.assemble(
        ("● ", "accent"),
        ("Modelo cargado: ", "muted"),
        (payload["modelName"], "bold"),
        ("   |   Variables: ", "muted"),
        (", ".join(payload["featureNames"]), "bold"),
        justify="center",
    )
    console.print(
        Panel(
            Group(title, subtitle, Text(""), status),
            box=box.DOUBLE,
            border_style="#7C5CFF",
            padding=(1, 2),
        )
    )


def showMenu() -> None:
    """Muestra las opciones del menú principal."""
    table = Table(box=box.SIMPLE_HEAVY, show_header=False, expand=True, padding=(0, 1))
    table.add_column(justify="center", style="accent", width=5)
    table.add_column(style="bold")
    table.add_column(style="muted")
    for key, label, hint in MENU_OPTIONS:
        table.add_row(f"[{key}]", label, hint)
    console.print(Panel(table, title="[brand]Menú principal[/]", border_style="grey35"))


def predictionsTable(predictions: List[ModelPredictionResult], title: str) -> Table:
    """Construye la tabla de predicciones con barra de probabilidad."""
    table = Table(
        title=title,
        title_style="brand",
        box=box.ROUNDED,
        header_style="bold white on #3B2F80",
        border_style="grey35",
    )
    table.add_column("Monto", justify="right")
    table.add_column("Mes")
    table.add_column("Día")
    table.add_column("Probabilidad de ingreso")
    table.add_column("Clase", justify="center")
    table.add_column("Confianza")
    for prediction in predictions:
        table.add_row(
            formatMoney(prediction.monto),
            MONTHS[prediction.mes - 1],
            DAYS[prediction.diaSemana],
            probabilityBar(prediction.probability),
            classText(prediction.label),
            confidenceLabel(prediction.probability),
        )
    return table


def askAmount() -> float:
    """Pide el monto hasta recibir un número positivo."""
    while True:
        raw = Prompt.ask("  [accent]Monto[/] en pesos [muted](ej. 250.000)[/]")
        value = parseAmount(raw)
        if value is not None and value > 0:
            return value
        console.print("  [error]Monto inválido.[/] Escribe un número mayor que cero.")


def askRange(label: str, minimum: int, maximum: int) -> int:
    """Pide un entero dentro de un rango."""
    while True:
        value = IntPrompt.ask(label)
        if minimum <= value <= maximum:
            return value
        console.print(f"  [error]Debe estar entre {minimum} y {maximum}.[/]")


def predictSingle(controller: ModelController) -> None:
    """Pide un movimiento al usuario y muestra la predicción interpretada."""
    console.print(Rule("[brand]Nuevo movimiento[/]", style="grey35"))
    monto = askAmount()
    mes = askRange("  [accent]Mes[/] [muted](1 = enero … 12 = diciembre)[/]", 1, 12)
    dayHint = "  ".join(f"{i}={d[:3]}" for i, d in enumerate(DAYS))
    dia = askRange(f"  [accent]Día de la semana[/] [muted]({dayHint})[/]", 0, 6)

    try:
        with console.status("[accent]Consultando el modelo…[/]", spinner="dots"):
            prediction = controller.predictNewCases([(monto, mes, dia)])[0]
    except ValueError as error:
        console.print(f"\n  [error]No se pudo predecir:[/] {error}")
        return

    isIncome = prediction.label == 1
    color = "#22C55E" if isIncome else "#F43F5E"
    verdict = Text("INGRESO" if isIncome else "GASTO", style=f"bold {color}", justify="center")
    detail = Text.assemble(
        (formatMoney(monto), "bold"),
        (f"  ·  {MONTHS[mes - 1]}  ·  {DAYS[dia]}", "muted"),
        justify="center",
    )
    bar = Align.center(probabilityBar(prediction.probability, width=36))
    explanation = Text(
        "La barra es la probabilidad de que el movimiento sea un ingreso. "
        "Por encima de 50 % el modelo lo clasifica como ingreso; cerca de 50 % "
        "la decisión es incierta y conviene que el usuario la confirme.",
        style="muted",
        justify="center",
    )
    confidence = Text.assemble(("Confianza: ", "muted"), confidenceLabel(prediction.probability))
    console.print(
        Panel(
            Group(verdict, detail, Text(""), bar, Align.center(confidence), Text(""), explanation),
            title="[bold]Resultado[/]",
            border_style=color,
            padding=(1, 4),
        )
    )


def predictBatch(controller: ModelController) -> None:
    """Clasifica el lote de ejemplo usado en la demostración."""
    with console.status("[accent]Clasificando lote de ejemplo…[/]", spinner="dots"):
        predictions = controller.predictNewCases(SAMPLE_CASES)
    console.print(predictionsTable(predictions, "Lote de ejemplo"))


def showMetrics(controller: ModelController) -> None:
    """Muestra la comparación de modelos y la matriz de confusión del mejor."""
    try:
        metrics = controller.loadMetrics()
    except FileNotFoundError as error:
        console.print(f"\n[error]{error}[/]")
        return

    columns = [
        ("Exact.", "accuracy"),
        ("Prec.", "precision"),
        ("Recall", "recall"),
        ("F1 macro", "f1Macro"),
        ("F1 ingr.", "f1Class1"),
        ("AUC", "rocAuc"),
        ("CV F1", "crossValidationMean"),
    ]
    best = {key: max(score[key] for score in metrics["models"]) for _, key in columns}

    table = Table(
        title=f"Comparación de modelos · prueba con {metrics['testCount']} filas",
        title_style="brand",
        box=box.ROUNDED,
        header_style="bold white on #3B2F80",
        border_style="grey35",
        caption=(
            "Verde = mejor valor de la columna · ★ = elegido por F1 macro de validación cruzada\n"
            "Exact. = exactitud · Prec. = precisión · F1 ingr. = F1 de la clase Ingreso · "
            "AUC = ROC-AUC · CV F1 = F1 macro medio en 5 folds"
        ),
        caption_style="muted",
    )
    table.add_column("Modelo", style="bold", no_wrap=True)
    for label, _ in columns:
        table.add_column(label, justify="right", no_wrap=True)

    for score in metrics["models"]:
        isChosen = score["modelName"] == metrics["modelName"]
        cells = [
            Text(f"{score[key]:.4f}", style="ingreso" if score[key] == best[key] else "")
            for _, key in columns
        ]
        name = Text(("★ " if isChosen else "  ") + score["modelName"], style="accent" if isChosen else "")
        table.add_row(name, *cells)
    console.print(table)

    chosen = next(s for s in metrics["models"] if s["modelName"] == metrics["modelName"])
    (tn, fp), (fn, tp) = chosen["confusionMatrix"]
    matrix = Table(box=box.SQUARE, title="Matriz de confusión (mejor modelo)", title_style="brand")
    matrix.add_column("Real \\ Predicho", style="bold")
    matrix.add_column("Gasto", justify="center")
    matrix.add_column("Ingreso", justify="center")
    matrix.add_row("Gasto", Text(str(tn), style="ingreso"), Text(str(fp), style="gasto"))
    matrix.add_row("Ingreso", Text(str(fn), style="gasto"), Text(str(tp), style="ingreso"))

    note = Text.assemble(
        ("¿Por qué F1 macro? ", "accent"),
        (
            "Hay 86 gastos y 34 ingresos. La exactitud premia predecir siempre "
            "'Gasto'; el F1 macro promedia el desempeño de ambas clases por igual.",
            "muted",
        ),
    )
    console.print(Columns([matrix, Panel(note, border_style="grey35", width=52)], padding=(0, 2)))


def showModelInside(payload: dict) -> None:
    """Muestra hiperparámetros, peso de cada variable y gráficos disponibles."""
    info = Table.grid(padding=(0, 2))
    info.add_column(style="muted")
    info.add_column(style="bold")
    info.add_row("Modelo", payload["modelName"])
    info.add_row("Variable objetivo", f"{payload['targetName']} (1 = ingreso, 0 = gasto)")
    info.add_row("Archivo del modelo", str(MODEL_PATH))
    info.add_row("Archivo de métricas", str(MODEL_METRICS_PATH))
    if payload.get("bestParams"):
        info.add_row("Hiperparámetros", str(payload["bestParams"]).replace("modelo__", ""))
    console.print(Panel(info, title="[brand]Modelo guardado[/]", border_style="grey35"))

    weights = SklearnModelService.describeModel(payload["model"], tuple(payload["featureNames"]))
    if weights:
        top = max(abs(v) for v in weights.values()) or 1.0
        table = Table(
            title="Importancia de cada variable",
            title_style="brand",
            box=box.SIMPLE_HEAVY,
            caption="monto_log domina: el monto es lo que más\nsepara ingresos de gastos",
            caption_style="muted",
        )
        table.add_column("Variable", style="bold")
        table.add_column("Peso", justify="right")
        table.add_column("")
        for name, value in sorted(weights.items(), key=lambda item: -abs(item[1])):
            bar = Text("█" * max(1, round(abs(value) / top * 30)), style="accent")
            table.add_row(name, f"{value:+.4f}", bar)
        console.print(table)

    charts = sorted(Path(MODEL_CHARTS_DIR).glob("*.png"))
    if charts:
        console.print("[brand]Gráficos de evaluación disponibles:[/]")
        for chart in charts:
            console.print(f"  [accent]•[/] {chart}")
    else:
        console.print("[warn]Todavía no hay gráficos. Ejecuta: python src/modelo_proyecto.py[/]")


# --------------------------------------------------------------------------- #
# Programa principal
# --------------------------------------------------------------------------- #
def main() -> None:
    """Ejecuta el menú hasta que el usuario decida salir."""
    controller = ModelController(
        storage=ModelPersistenceService(MODEL_PATH, MODEL_METRICS_PATH)
    )

    try:
        payload = controller.loadModel()
    except FileNotFoundError as error:
        console.print(Panel(f"{error}\n\nEntrena primero con: python src/modelo_proyecto.py",
                            title="[error]Modelo no encontrado[/]", border_style="red"))
        return

    console.clear()
    showHeader(payload)

    actions = {
        "1": lambda: predictSingle(controller),
        "2": lambda: predictBatch(controller),
        "3": lambda: showMetrics(controller),
        "4": lambda: showModelInside(payload),
    }

    while True:
        showMenu()
        try:
            option = Prompt.ask("[brand]Elige una opción[/]", choices=[k for k, *_ in MENU_OPTIONS],
                                show_choices=False)
        except (EOFError, KeyboardInterrupt):
            option = "5"

        if option == "5":
            console.print(Panel(Text("¡Hasta luego!", justify="center", style="brand"),
                                border_style="#7C5CFF"))
            break

        console.print()
        try:
            actions[option]()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[warn]Operación cancelada.[/]")
        console.print()
        try:
            if not ConfirmEs.ask("[muted]¿Volver al menú?[/]", default=True):
                break
        except (EOFError, KeyboardInterrupt):
            break
        console.clear()
        showHeader(payload)


if __name__ == "__main__":
    main()
