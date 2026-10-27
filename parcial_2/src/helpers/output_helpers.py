"""Utilidades para mostrar información formateada en la terminal."""


def print_separator(title: str = ""):
    """Imprime un bloque separador con un título opcional."""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
