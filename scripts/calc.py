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
        choices=["sumar", "restar", "multiplicar", "dividir"],
        default="sumar",
        help='Operación a realizar: "sumar" (por defecto)',
    )

    parser.add_argument(
        "--precision",
        help="Especificar numero cifras decimales",
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
    elif args.operacion == "restar":
        resultado = args.x - args.y
        operador = "-"
    elif args.operacion == "multiplicar":
        resultado = args.x * args.y
        operador = "*"
    elif args.operacion == "dividir":
        resultado = args.x / args.y
        operador = "/"

    ND = args.precision
    ND = int(ND)

    if args.precision:
        resultado = round(resultado, ndigits=ND)
    

    # Impresión según verbose
    if args.verbose:
        print(f"{resultado}")
    else:
        print(f"{args.x} {operador} {args.y} = {resultado}")


if __name__ == "__main__":
    main()
