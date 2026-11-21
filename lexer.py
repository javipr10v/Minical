from dataclasses import dataclass


@dataclass
class Token:
    tipo: str
    valor: str
    linea: int


PALABRAS = {"if": "IF", "else": "ELSE", "while": "WHILE"}

SIMPLES = {
    "+": "PLUS", "-": "MINUS", "*": "STAR", "/": "SLASH",
    "<": "LT", ">": "GT", "=": "ASSIGN",
    "(": "LPAREN", ")": "RPAREN", "{": "LBRACE", "}": "RBRACE",
    ";": "SEMI",
}


def tokenizar(texto):
    """Devuelve (tokens, errores). No se detiene en el primer simbolo invalido."""
    tokens = []
    errores = []
    i = 0
    linea = 1
    n = len(texto)

    while i < n:
        c = texto[i]

        if c == "\n":
            linea += 1
            i += 1
        elif c in " \t\r":
            i += 1
        elif c.isdigit():
            j = i
            while j < n and texto[j].isdigit():
                j += 1
            if j + 1 < n and texto[j] == "." and texto[j + 1].isdigit():
                j += 1
                while j < n and texto[j].isdigit():
                    j += 1
            tokens.append(Token("NUM", texto[i:j], linea))
            i = j
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (texto[j].isalnum() or texto[j] == "_"):
                j += 1
            palabra = texto[i:j]
            tokens.append(Token(PALABRAS.get(palabra, "ID"), palabra, linea))
            i = j
        elif c == "=" and texto[i + 1:i + 2] == "=":
            tokens.append(Token("EQEQ", "==", linea))
            i += 2
        elif c in SIMPLES:
            tokens.append(Token(SIMPLES[c], c, linea))
            i += 1
        else:
            errores.append(f"Linea {linea}: simbolo invalido '{c}'")
            i += 1

    tokens.append(Token("EOF", "", linea))
    return tokens, errores


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python lexer.py archivo.mc")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8-sig") as f:
        codigo = f.read()

    toks, errs = tokenizar(codigo)
    print(f"{'LINEA':<7}{'TIPO':<9}VALOR")
    for t in toks:
        print(f"{t.linea:<7}{t.tipo:<9}{t.valor}")
    for e in errs:
        print("ERROR LEXICO ->", e)
