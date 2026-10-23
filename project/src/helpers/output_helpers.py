"""Utilidades para mostrar información formateada en la terminal."""


def print_separator(title: str = ""):
    """Imprime un bloque separador con un título opcional.

    El formato es una línea de signos igual, el título y otra línea igual.
    """
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)
