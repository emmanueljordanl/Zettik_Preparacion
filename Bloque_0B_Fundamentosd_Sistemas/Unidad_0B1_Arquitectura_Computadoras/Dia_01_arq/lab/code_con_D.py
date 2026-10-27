def AND(a, b): return a & b


def XOR(a, b): return a ^ b  # ^ es el XOR bit a bit en Python


def NAND(a, b): return 1 - (a & b)  # NOT-AND


def NOR(a, b):  return 1 - (a | b)  # NOT-OR


# XOR construye la suma de dos bits: bit de suma = XOR, acarreo = AND
print("Suma de dos bits con XOR (suma) y AND (acarreo):")
for a in (0, 1):
    for b in (0, 1):
        suma, acarreo = XOR(a, b), AND(a, b)
        print(f"  {a} + {b} = {acarreo}{suma} (binario)  [suma={suma}, acarreo={acarreo}]")


# 1 + 1 = 10 (binario): suma=0, acarreo=1  -- el medio sumador del Dia 2

# Paridad: XOR de todos los bits (1 si hay un numero impar de unos)
def paridad(bits):
    resultado = 0
    for b in bits: resultado ^= b  # XOR acumulado
    return resultado


print(f"paridad de [1,0,1,1] = {paridad([1, 0, 1, 1])} (3 unos = impar -> 1)")
print(f"paridad de [1,0,1,0] = {paridad([1, 0, 1, 0])} (2 unos = par -> 0)")
