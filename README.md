# MiniCalc - Analizador sintactico

Actividad de Compiladores, UNACH. Lenguaje: Python 3.

## Que hace
Analiza programas MiniCalc por descenso recursivo: toma los tokens del analizador lexico y construye un AST. Reporta errores con linea y token esperado, y no se detiene en el primero (modo panico, sincroniza en ; y }).

MiniCalc admite expresiones aritmeticas con parentesis y signo negativo, asignaciones, if/else y while.

## Archivos
- lexer.py: analizador lexico (tokens con tipo, valor y linea)
- sintactico.py: parser, evaluador de expresiones e impresion del AST
- main.py: lee un programa e imprime el AST y los errores
- pruebas_expr.py: 5 expresiones probadas (Etapa 3)
- pruebas_errores.py: 8 casos, 5 validos y 3 con error (Etapa 5)
- prueba1.mc, prueba2.mc, prueba_error.mc: programas de ejemplo

## Como ejecutarlo
Requiere Python 3 instalado.

    python lexer.py prueba1.mc          (lista de tokens)
    python main.py prueba2.mc           (AST y errores)
    python main.py prueba2.mc -t        (tambien muestra los tokens)
    python main.py                      (modo interactivo, linea vacia para terminar)
    python pruebas_expr.py              (5 expresiones)
    python pruebas_errores.py           (8 casos de prueba)
    python main.py prueba_error.mc      (programa con 3 errores)

Si "python" no responde, usar "py".

## Gramatica (EBNF)
    programa    -> sentencia*
    sentencia   -> asignacion | si | mientras
    asignacion  -> ID '=' expr ';'
    si          -> 'if' '(' condicion ')' bloque ( 'else' bloque )?
    mientras    -> 'while' '(' condicion ')' bloque
    bloque      -> '{' sentencia* '}'
    condicion   -> expr ( '<' | '>' | '==' ) expr
    expr        -> term ( ( '+' | '-' ) term )*
    term        -> factor ( ( '*' | '/' ) factor )*
    factor      -> '-' factor | NUM | ID | '(' expr ')'

## Declaracion de uso de herramientas de apoyo
Se uso Claude (Anthropic) como apoyo para estructurar el codigo y redactar documentos. El equipo reviso, probo y asume la responsabilidad del contenido.
