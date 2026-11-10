"""Utilidades para presentar información en la terminal."""


def print_separator(title: str = "") -> None:
    """Imprime un bloque separador con un título opcional."""
    print("\n" + "=" * 68)
    if title:
        print(f"  {title}")
        print("=" * 68)


def print_dataframe(title: str, dataframe) -> None:
    """Imprime una tabla de Pandas redondeada y sin el índice."""
    print(f"\n{title}")
    print(dataframe.round(3).to_string(index=False))
