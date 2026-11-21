from lexer import tokenizar

NOMBRES = {
    "ID": "un identificador", "NUM": "un numero", "ASSIGN": "'='",
    "SEMI": "';'", "LPAREN": "'('", "RPAREN": "')'",
    "LBRACE": "'{'", "RBRACE": "'}'",
    "IF": "'if'", "ELSE": "'else'", "WHILE": "'while'",
}


class ErrorSintactico(Exception):
    pass


class ErrorEjecucion(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.i = 0
        self.errores = []

    # ---------- utilidades ----------
    def peek(self):
        return self.toks[self.i]

    def describe(self, t):
        return "fin de archivo" if t.tipo == "EOF" else f"'{t.valor}'"

    def eat(self, tipo):
        t = self.peek()
        if t.tipo == tipo:
            self.i += 1
            return t
        linea = t.linea
        if tipo == "SEMI" and self.i > 0:
            linea = self.toks[self.i - 1].linea
        esperado = NOMBRES.get(tipo, tipo)
        raise ErrorSintactico(
            f"Linea {linea}: se esperaba {esperado} pero se encontro {self.describe(t)}")

    def sincronizar(self, en_bloque):
        # modo panico: avanzar hasta pasar un ';' o llegar a un '}'
        while self.peek().tipo != "EOF":
            tipo = self.peek().tipo
            if tipo == "SEMI":
                self.i += 1
                return
            if tipo == "RBRACE":
                if not en_bloque:
                    self.i += 1
                return
            self.i += 1

    # ---------- sentencias ----------
    def programa(self):
        sents = []
        while self.peek().tipo != "EOF":
            try:
                sents.append(self.sentencia())
            except ErrorSintactico as e:
                self.errores.append(str(e))
                self.sincronizar(False)
        return ("programa", sents)

    def sentencia(self):
        t = self.peek()
        if t.tipo == "ID":
            return self.asignacion()
        if t.tipo == "IF":
            return self.si()
        if t.tipo == "WHILE":
            return self.mientras()
        raise ErrorSintactico(
            f"Linea {t.linea}: se esperaba una sentencia (asignacion, if o while) "
            f"pero se encontro {self.describe(t)}")

    def asignacion(self):
        nombre = self.eat("ID")
        self.eat("ASSIGN")
        e = self.expr()
        self.eat("SEMI")
        return ("asigna", nombre.valor, e)

    def si(self):
        self.eat("IF")
        self.eat("LPAREN")
        c = self.condicion()
        self.eat("RPAREN")
        entonces = self.bloque()
        sino = None
        if self.peek().tipo == "ELSE":
            self.i += 1
            sino = self.bloque()
        return ("si", c, entonces, sino)

    def mientras(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        c = self.condicion()
        self.eat("RPAREN")
        cuerpo = self.bloque()
        return ("mientras", c, cuerpo)

    def bloque(self):
        self.eat("LBRACE")
        sents = []
        while self.peek().tipo not in ("RBRACE", "EOF"):
            try:
                sents.append(self.sentencia())
            except ErrorSintactico as e:
                self.errores.append(str(e))
                self.sincronizar(True)
        self.eat("RBRACE")
        return ("bloque", sents)

    def condicion(self):
        izq = self.expr()
        t = self.peek()
        if t.tipo not in ("LT", "GT", "EQEQ"):
            raise ErrorSintactico(
                f"Linea {t.linea}: se esperaba un operador de comparacion "
                f"('<', '>' o '==') pero se encontro {self.describe(t)}")
        self.i += 1
        der = self.expr()
        return ("cond", t.valor, izq, der)

    # ---------- expresiones ----------
    def expr(self):
        izq = self.term()
        while self.peek().tipo in ("PLUS", "MINUS"):
            op = self.peek()
            self.i += 1
            izq = ("bin", op.valor, izq, self.term())
        return izq

    def term(self):
        izq = self.factor()
        while self.peek().tipo in ("STAR", "SLASH"):
            op = self.peek()
            self.i += 1
            izq = ("bin", op.valor, izq, self.factor())
        return izq

    def factor(self):
        t = self.peek()
        if t.tipo == "MINUS":
            self.i += 1
            return ("neg", self.factor())
        if t.tipo == "NUM":
            self.i += 1
            return ("num", float(t.valor) if "." in t.valor else int(t.valor))
        if t.tipo == "ID":
            self.i += 1
            return ("var", t.valor)
        if t.tipo == "LPAREN":
            self.i += 1
            e = self.expr()
            self.eat("RPAREN")
            return e
        raise ErrorSintactico(
            f"Linea {t.linea}: se esperaba una expresion pero se encontro {self.describe(t)}")


# ---------- evaluacion de expresiones (Etapa 3) ----------
def evaluar(n, variables=None):
    if variables is None:
        variables = {}
    k = n[0]
    if k == "num":
        return n[1]
    if k == "var":
        if n[1] not in variables:
            raise ErrorEjecucion(f"la variable '{n[1]}' no tiene valor")
        return variables[n[1]]
    if k == "neg":
        return -evaluar(n[1], variables)
    if k == "bin":
        a = evaluar(n[2], variables)
        b = evaluar(n[3], variables)
        op = n[1]
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if b == 0:
            raise ErrorEjecucion("division entre cero")
        r = a / b
        return int(r) if r == int(r) else r
    raise ErrorEjecucion(f"no se puede evaluar el nodo '{k}'")


# ---------- impresion del AST con sangria (Etapa 4) ----------
def lineas_ast(n, nivel=0):
    p = "  " * nivel
    k = n[0]
    if k == "programa":
        out = [p + "Programa"]
        for s in n[1]:
            out += lineas_ast(s, nivel + 1)
        return out
    if k == "asigna":
        return [p + f"Asignacion {n[1]} ="] + lineas_ast(n[2], nivel + 1)
    if k == "si":
        out = [p + "Si"] + lineas_ast(n[1], nivel + 1)
        out += [p + "  Entonces"] + lineas_ast(n[2], nivel + 2)
        if n[3] is not None:
            out += [p + "  Sino"] + lineas_ast(n[3], nivel + 2)
        return out
    if k == "mientras":
        out = [p + "Mientras"] + lineas_ast(n[1], nivel + 1)
        out += [p + "  Cuerpo"] + lineas_ast(n[2], nivel + 2)
        return out
    if k == "bloque":
        out = [p + "Bloque"]
        for s in n[1]:
            out += lineas_ast(s, nivel + 1)
        return out
    if k == "cond":
        return ([p + f"Comparacion {n[1]}"] + lineas_ast(n[2], nivel + 1)
                + lineas_ast(n[3], nivel + 1))
    if k == "bin":
        return ([p + f"Operacion {n[1]}"] + lineas_ast(n[2], nivel + 1)
                + lineas_ast(n[3], nivel + 1))
    if k == "neg":
        return [p + "Negativo"] + lineas_ast(n[1], nivel + 1)
    if k == "num":
        return [p + f"Num {n[1]}"]
    return [p + f"Var {n[1]}"]


# ---------- funciones de entrada ----------
def analizar(texto):
    """Lexico + parser. Devuelve (tokens, ast, errores)."""
    toks, errs_lex = tokenizar(texto)
    p = Parser(toks)
    ast = p.programa()
    return toks, ast, errs_lex + p.errores


def parsear_expresion(texto):
    toks, _ = tokenizar(texto)
    p = Parser(toks)
    e = p.expr()
    if p.peek().tipo != "EOF":
        raise ErrorSintactico(
            f"Linea {p.peek().linea}: sobra {p.describe(p.peek())} despues de la expresion")
    return e
