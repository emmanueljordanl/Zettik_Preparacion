"""Segunda Universidad | B0-B, U0-B.1, Dia 1.

Implementacion de referencia para estudio, NO evidencia de autoria independiente.
Representacion binaria, logica digital, paridad, universalidad y overflow.
"""

from itertools import product
import warnings

import numpy as np


# --------------------------------------------------
# A. Representacion binaria y rangos
# --------------------------------------------------
def rango_sin_signo(bits: int) -> tuple[int, int]:
    if type(bits) is not int or bits <= 0:
        raise ValueError("bits debe ser un entero positivo")
    return 0, 2**bits - 1


def rango_con_signo(bits: int) -> tuple[int, int]:
    if type(bits) is not int or bits <= 0:
        raise ValueError("bits debe ser un entero positivo")
    return -(2 ** (bits - 1)), 2 ** (bits - 1) - 1


def decimal_a_binario(n: int, bits: int = 8) -> str:
    minimo, maximo = rango_sin_signo(bits)
    if type(n) is not int or not (minimo <= n <= maximo):
        raise ValueError(f"n debe estar en [{minimo}, {maximo}]")
    return format(n, f"0{bits}b")


def binario_a_decimal(b: str) -> int:
    if not isinstance(b, str) or not b or any(x not in "01" for x in b):
        raise ValueError("b debe contener solamente digitos 0 y 1")
    return int(b, 2)


# --------------------------------------------------
# B. Contrato de entradas: enteros 0 o 1
# --------------------------------------------------
def _validar(*valores: int) -> None:
    if any(type(v) is not int or v not in (0, 1) for v in valores):
        raise ValueError("Entradas invalidas: use solo los enteros 0 y 1")


def NOT(a: int) -> int:
    _validar(a)
    return 1 - a


def AND(a: int, b: int) -> int:
    _validar(a, b)
    return a & b


def OR(a: int, b: int) -> int:
    _validar(a, b)
    return a | b


def XOR(a: int, b: int) -> int:
    _validar(a, b)
    return a ^ b


def NAND(a: int, b: int) -> int:
    _validar(a, b)
    return 1 - (a & b)


def NOR(a: int, b: int) -> int:
    _validar(a, b)
    return 1 - (a | b)


def tabla_puertas() -> list[tuple[int, int, int, int, int, int, int]]:
    """Columnas: A, B, AND, OR, XOR, NAND, NOR."""
    return [(a, b, AND(a, b), OR(a, b), XOR(a, b), NAND(a, b), NOR(a, b))
            for a, b in product((0, 1), repeat=2)]


# --------------------------------------------------
# C. Leyes booleanas; se comprueban TODAS las entradas
# --------------------------------------------------
def verificar_leyes_booleanas() -> int:
    pruebas = 0
    for a, b, c in product((0, 1), repeat=3):
        assert NOT(AND(a, b)) == OR(NOT(a), NOT(b))  # De Morgan 1
        assert NOT(OR(a, b)) == AND(NOT(a), NOT(b))  # De Morgan 2
        assert AND(a, OR(b, c)) == OR(AND(a, b), AND(a, c))  # distributiva
        assert AND(a, a) == a  # idempotencia AND
        assert OR(a, a) == a  # idempotencia OR
        pruebas += 1
    return pruebas


# --------------------------------------------------
# D. Suma binaria y paridad
# --------------------------------------------------
def medio_sumador(a: int, b: int) -> tuple[int, int]:
    """Devuelve (suma, acarreo)."""
    return XOR(a, b), AND(a, b)


def paridad_impar(bits: list[int]) -> int:
    """Devuelve 1 cuando la cantidad de unos es impar."""
    acumulado = 0
    for bit in bits:
        acumulado = XOR(acumulado, bit)
    return acumulado


def paridad_par_3(a: int, b: int, c: int) -> int:
    """Devuelve 1 cuando hay 0 o 2 unos, segun el contrato integrador."""
    return NOT(XOR(XOR(a, b), c))


# --------------------------------------------------
# E. Universalidad usando SOLO la puerta NAND
# --------------------------------------------------
def NOT_nand(a: int) -> int:
    return NAND(a, a)


def AND_nand(a: int, b: int) -> int:
    x = NAND(a, b)
    return NAND(x, x)


def OR_nand(a: int, b: int) -> int:
    return NAND(NAND(a, a), NAND(b, b))


def XOR_nand(a: int, b: int) -> int:
    p = NAND(a, b)
    q = NAND(a, p)
    r = NAND(b, p)
    return NAND(q, r)


def NOR_nand(a: int, b: int) -> int:
    x = OR_nand(a, b)
    return NAND(x, x)


def verificar_universalidad() -> int:
    pruebas = 0
    for a, b in product((0, 1), repeat=2):
        assert NOT_nand(a) == NOT(a)
        assert AND_nand(a, b) == AND(a, b)
        assert OR_nand(a, b) == OR(a, b)
        assert XOR_nand(a, b) == XOR(a, b)
        assert NOR_nand(a, b) == NOR(a, b)
        pruebas += 1
    return pruebas


# --------------------------------------------------
# F. Metodo de diseno: mayoria de 3 bits
# --------------------------------------------------
def mayoria_sop(a: int, b: int, c: int) -> int:
    """A'BC + AB'C + ABC' + ABC (forma canonica)."""
    return OR(
        OR(AND(AND(NOT(a), b), c), AND(AND(a, NOT(b)), c)),
        OR(AND(AND(a, b), NOT(c)), AND(AND(a, b), c)),
    )


def mayoria(a: int, b: int, c: int) -> int:
    """AB + AC + BC (forma simplificada)."""
    return OR(OR(AND(a, b), AND(a, c)), AND(b, c))


def verificar_circuitos() -> tuple[int, int]:
    casos_mayoria = 0
    casos_paridad = 0
    for a, b, c in product((0, 1), repeat=3):
        esperado_mayoria = int(a + b + c >= 2)
        esperado_paridad = int((a + b + c) % 2 == 0)
        assert mayoria_sop(a, b, c) == esperado_mayoria
        assert mayoria(a, b, c) == esperado_mayoria
        assert paridad_par_3(a, b, c) == esperado_paridad
        casos_mayoria += 1
        casos_paridad += 1
    return casos_mayoria, casos_paridad


# --------------------------------------------------
# G. Overflow y cuantizacion
# --------------------------------------------------
def demo_desbordamiento() -> tuple[int, int, bool]:
    """Overflow con un int8 de NumPy; int de Python usa precision arbitraria."""
    with warnings.catch_warnings(record=True) as capturadas:
        warnings.simplefilter("always", RuntimeWarning)
        numpy_resultado = int(np.int8(127) + np.int8(1))
    python_resultado = 127 + 1
    assert numpy_resultado == -128
    assert python_resultado == 128
    return numpy_resultado, python_resultado, bool(capturadas)


def demo_cuantizacion() -> tuple[list[int], list[int], list[int], int, int]:
    """Simulacion logica de 4 bits: para ahorrar bytes hace falta empaquetar.

    NumPy sigue almacenando el vector cuantizado en uint8 (4 bytes).
    El almacenamiento de los cuatro valores con 4 bits empaquetados seria 2 bytes.
    """
    canal = np.array([0, 128, 200, 255], dtype=np.uint8)
    cuantizado = (canal // 16).astype(np.uint8)
    reconstruido = (cuantizado.astype(np.int16) * 16).astype(np.uint8)
    errores = np.abs(canal.astype(np.int16) - reconstruido.astype(np.int16))
    assert cuantizado.tolist() == [0, 8, 12, 15]
    assert int(errores.max()) == 15
    return canal.tolist(), cuantizado.tolist(), errores.tolist(), canal.nbytes, 2


def main() -> None:
    print("SEGUNDA UNIVERSIDAD | B0-B | U0-B.1 | DIA 1")
    print("\nA. REPRESENTACION")
    for valor in (42, 127, 255):
        binario = decimal_a_binario(valor)
        assert binario_a_decimal(binario) == valor
        print(f"  {valor:3d} -> {binario}")
    for bits in (8, 16, 32):
        print(f"  {bits} bits: unsigned={rango_sin_signo(bits)}; signed={rango_con_signo(bits)}")

    print("\nB. TABLAS DE VERDAD")
    print("  A B | AND OR XOR NAND NOR")
    for valores in tabla_puertas():
        print(" ", " ".join(map(str, valores[:2])), "|", "   ".join(map(str, valores[2:])))
    print("  NOT(0) =", NOT(0), "; NOT(1) =", NOT(1))

    print("\nC. LEYES BOOLEANAS")
    print("  De Morgan / distributiva / idempotencia: PASS en", verificar_leyes_booleanas(), "combinaciones")

    print("\nD. SUMA Y PARIDAD")
    for a, b in product((0, 1), repeat=2):
        suma, acarreo = medio_sumador(a, b)
        print(f"  {a} + {b} = {acarreo}{suma} (base 2)")
    print("  Paridad impar [1,0,1,1] =", paridad_impar([1, 0, 1, 1]))

    print("\nE. UNIVERSALIDAD DE NAND")
    print("  NOT, AND, OR, XOR, NOR con NAND: PASS en", verificar_universalidad(), "combinaciones")

    print("\nF. CIRCUITOS COMBINACIONALES")
    m, p = verificar_circuitos()
    print(f"  Mayoria: PASS en {m} combinaciones")
    print(f"  Paridad par 3 bits: PASS en {p} combinaciones")

    print("\nG. DESBORDAMIENTO")
    np_resultado, py_resultado, advertencia = demo_desbordamiento()
    print(f"  np.int8(127) + np.int8(1) = {np_resultado}; aviso NumPy={advertencia}")
    print(f"  int de Python: 127 + 1 = {py_resultado}")
    print("  Nota: NumPy advierte sobre overflow en esta version; no se debe depender de ello.")

    print("\nH. CUANTIZACION DE PIXELES")
    original, cuant, error, memoria, empaquetado = demo_cuantizacion()
    print(f"  Original={original}; 4 bits={cuant}; errores={error}")
    print(f"  Almacenamiento original uint8={memoria} bytes; ideal 4 bits empaquetados={empaquetado} bytes")
    print("  IMPORTANTE: uint8 de NumPy para valores cuantizados sigue usando 4 bytes.")
    print("\nRESULTADO: REFERENCIA TECNICA VALIDADA (no equivale a gate individual).")


if __name__ == "__main__":
    main()
