from sintactico import parsear_expresion, evaluar

CASOS = [
    ("-(2 + 3) * 4", -20),
    ("3 + 4 * (2 - 1)", 7),
    ("10 - 4 - 3", 3),
    ("100 / 5 / 2", 10),
    ("2 * (3 + 4) - -1", 15),
]

ok = 0
print(f"{'EXPRESION':<22}{'ESPERADO':<10}{'OBTENIDO':<10}RESULTADO")
for texto, esperado in CASOS:
    obtenido = evaluar(parsear_expresion(texto))
    paso = obtenido == esperado
    ok += paso
    print(f"{texto:<22}{esperado:<10}{obtenido:<10}{'OK' if paso else 'FALLO'}")
print(f"\n{ok}/{len(CASOS)} expresiones correctas")
