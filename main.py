import sys
from sintactico import analizar, lineas_ast


def leer_programa():
    archivos = [a for a in sys.argv[1:] if not a.startswith("-")]
    if archivos:
        with open(archivos[0], encoding="utf-8-sig") as f:
            return f.read()
    print("Escribe tu programa MiniCalc. Linea vacia para terminar:")
    lineas = []
    while True:
        try:
            l = input()
        except EOFError:
            break
        if l.strip() == "":
            break
        lineas.append(l)
    return "\n".join(lineas)


def main():
    codigo = leer_programa()
    toks, ast, errores = analizar(codigo)

    if "-t" in sys.argv:
        print("\nTOKENS")
        print(f"{'LINEA':<7}{'TIPO':<9}VALOR")
        for t in toks:
            print(f"{t.linea:<7}{t.tipo:<9}{t.valor}")

    print("\nAST")
    for l in lineas_ast(ast):
        print(l)

    print(f"\nERRORES ({len(errores)})")
    if not errores:
        print("Sin errores sintacticos.")
    for e in errores:
        print(" -", e)


if __name__ == "__main__":
    main()
