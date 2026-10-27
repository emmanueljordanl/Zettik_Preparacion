def NOT(a): return 1 - a


def AND(a, b): return a & b


def OR(a, b):  return a | b


# Verificar De Morgan EXHAUSTIVAMENTE: (A AND B)' == A' OR B' para TODAS las entradas
print("Verificacion de De Morgan: (A AND B)' = A' OR B'")
todas_coinciden = True
for a in (0, 1):
    for b in (0, 1):
        izquierda = NOT(AND(a, b))  # (A AND B)'
        derecha = OR(NOT(a), NOT(b))  # A' OR B'
        coincide = izquierda == derecha
        todas_coinciden &= coincide
        print(f"  A={a} B={b}: (A AND B)'={izquierda}, A' OR B'={derecha}  {'OK' if coincide else 'FALLO'}")
print(f"De Morgan {'se cumple' if todas_coinciden else 'FALLA'} para todas las entradas")
