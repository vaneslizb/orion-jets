"""
Script de ejemplo para introducir argumentos de línea de comandos con argparse.

Este programa realiza una operación aritmética sencilla entre dos números
proporcionados por el usuario. Para esta primera versión, las operaciones
permitidas son:

- "sumar"  → suma de x y y
- "restar" → resta de x y y

Además, el usuario puede activar un modo "verbose" que imprime un mensaje más
informativo mostrando la operación completa. Si no se usa verbose, el programa
solo imprime el resultado numérico.

Ejemplos de uso:

    uv run scripts/calc.py 3 4
    uv run scripts/calc.py 10 7 --operacion restar
    uv run scripts/calc.py 5 6 --verbose

El objetivo principal de este script es mostrar cómo:
- definir argumentos obligatorios,
- definir opciones,
- y acceder a esos valores dentro del código.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Realiza una operación aritmética simple entre dos números."
    )

    # Argumentos obligatorios: x y y
    parser.add_argument(
        "x",
        help="Primer número.",
        type=float,
    )
    parser.add_argument(
        "y",
        help="Segundo número.",
        type=float,
    )

    # Opción para elegir la operación
    parser.add_argument(
        "--operacion",
        choices=["sumar", "restar"],
        default="sumar",
        help='Operación a realizar: "sumar" (por defecto) o "restar".',
    )

    # Opción booleana "verbose"
    parser.add_argument(
        "--verbose",
        action="store_false",
        help="Si se activa, muestra una salida más detallada.",
    )

    args = parser.parse_args()

    # Lógica de la operación
    if args.operacion == "sumar":
        resultado = args.x + args.y
        operador = "+"
    else:  # "restar"
        resultado = args.x - args.y
        operador = "-"

    # Impresión según verbose
    if args.verbose:
        print(f"{resultado}")
    else:
        print(f"{args.x} {operador} {args.y} = {resultado}")


if __name__ == "__main__":
    main()