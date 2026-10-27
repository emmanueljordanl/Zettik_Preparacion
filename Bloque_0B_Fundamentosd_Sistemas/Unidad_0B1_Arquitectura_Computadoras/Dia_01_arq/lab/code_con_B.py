# Las puertas logicas como funciones (1 = True, 0 = False)
def NOT(a): return 1 - a


def AND(a, b): return a & b  # & es el AND bit a bit en Python


def OR(a, b):  return a | b  # | es el OR bit a bit


# Tablas de verdad: probar TODAS las combinaciones de entrada
print("A B | AND OR  | A NOT")
for a in (0, 1):
    for b in (0, 1):
        print(f"{a} {b} |  {AND(a, b)}  {OR(a, b)}  | {a}  {NOT(a)}")
# Verifica las reglas: AND es 1 solo si ambos son 1; OR si alguno; NOT invierte.
