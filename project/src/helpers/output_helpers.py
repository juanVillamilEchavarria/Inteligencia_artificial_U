## este archivo contiene helpers de output, es decir, para mostrar informacion en la terminal 

def print_separator(title: str = ""):
    """
    Imprime un separador en la consola.
    el formato es : 
    [lineas]
    [title]
    [lineas]
    """
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)