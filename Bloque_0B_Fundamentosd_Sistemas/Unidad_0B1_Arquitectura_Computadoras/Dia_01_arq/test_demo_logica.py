"""Pruebas para la implementacion de referencia del Dia 1."""

from itertools import product

import pytest

from demo_logica import (
    AND, OR, NOT, XOR, NAND, NOR, AND_nand, OR_nand, NOT_nand,
    XOR_nand, NOR_nand, rango_sin_signo, rango_con_signo,
    decimal_a_binario, binario_a_decimal, verificar_leyes_booleanas,
    verificar_universalidad, medio_sumador, paridad_par_3,
    mayoria_sop, mayoria, demo_desbordamiento, demo_cuantizacion,
)


def test_conversiones_y_rangos():
    assert rango_sin_signo(8) == (0, 255)
    assert rango_con_signo(8) == (-128, 127)
    assert rango_sin_signo(10) == (0, 1023)
    for n in (0, 42, 127, 255):
        assert binario_a_decimal(decimal_a_binario(n)) == n
    with pytest.raises(ValueError):
        decimal_a_binario(256)
    with pytest.raises(ValueError):
        binario_a_decimal("10201")


@pytest.mark.parametrize("a,b,esperados", [
    (0, 0, (0, 0, 0, 1, 1)),
    (0, 1, (0, 1, 1, 1, 0)),
    (1, 0, (0, 1, 1, 1, 0)),
    (1, 1, (1, 1, 0, 0, 0)),
])
def test_puertas_tabla_completa(a, b, esperados):
    assert (AND(a, b), OR(a, b), XOR(a, b), NAND(a, b), NOR(a, b)) == esperados
    assert NOT(a) == 1 - a


@pytest.mark.parametrize("a,b", [(2, 1), (0, 3), (-1, 0), (1, 2), (True, 1)])
def test_entradas_invalidas(a, b):
    with pytest.raises(ValueError):
        AND(a, b)


def test_leyes_booleanas():
    assert verificar_leyes_booleanas() == 8


def test_puertas_desde_nand():
    assert verificar_universalidad() == 4
    for a, b in product((0, 1), repeat=2):
        assert NOT_nand(a) == NOT(a)
        assert AND_nand(a, b) == AND(a, b)
        assert OR_nand(a, b) == OR(a, b)
        assert XOR_nand(a, b) == XOR(a, b)
        assert NOR_nand(a, b) == NOR(a, b)


def test_medio_sumador():
    for a, b in product((0, 1), repeat=2):
        s, c = medio_sumador(a, b)
        assert c * 2 + s == a + b


def test_mayoria_y_paridad_exhaustivos():
    for a, b, c in product((0, 1), repeat=3):
        esperado_mayoria = 1 if a + b + c >= 2 else 0
        esperado_paridad = 1 if (a + b + c) % 2 == 0 else 0
        assert mayoria_sop(a, b, c) == esperado_mayoria
        assert mayoria(a, b, c) == esperado_mayoria
        assert paridad_par_3(a, b, c) == esperado_paridad


def test_overflow_int8():
    np_resultado, py_resultado, _ = demo_desbordamiento()
    assert np_resultado == -128
    assert py_resultado == 128


def test_cuantizacion_y_memoria():
    original, cuantizado, errores, original_bytes, ideal_bytes = demo_cuantizacion()
    assert original == [0, 128, 200, 255]
    assert cuantizado == [0, 8, 12, 15]
    assert errores == [0, 0, 8, 15]
    assert original_bytes == 4
    assert ideal_bytes == 2
