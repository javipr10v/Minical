from sintactico import analizar

CASOS = [
    ("V1 asignacion simple", "x = 1 + 2;", 0),
    ("V2 ejemplo del PDF", "x = 3 + 4 * (2 - 1);\nwhile (x > 0) {\n  if (x > 5) { x = x - 2; } else { x = x - 1; }\n}", 0),
    ("V3 if sin else", "if (x > 1) { x = 2; }", 0),
    ("V4 negativo y division", "a = -(2 + 3) * 4;\nb = a / 2 - 1;", 0),
    ("V5 while anidado", "while (n > 0) {\n  while (m == 1) {\n    m = m - 1;\n  }\n  n = n - 1;\n}", 0),
    ("E1 falta punto y coma", "x = 3\ny = 4;\nz = 5;", 1),
    ("E2 falta llave de cierre", "while (x > 0) {\n  x = x - 1;\n", 1),
    ("E3 dos errores seguidos", "x = (3 + 4;\ny = 5 +;\nz = 1;", 2),
]

ok = 0
print(f"{'CASO':<28}{'ESPERADO':<10}{'OBTENIDO':<10}RESULTADO")
for nombre, codigo, esperado in CASOS:
    _, _, errores = analizar(codigo)
    paso = len(errores) == esperado
    ok += paso
    print(f"{nombre:<28}{esperado:<10}{len(errores):<10}{'OK' if paso else 'FALLO'}")
    for e in errores:
        print("      ->", e)
print(f"\n{ok}/{len(CASOS)} casos correctos")
