def NAND(a, b):
    return 1 - (a & b)  # Puerta base

def NOT_nand(a):
    return NAND(a, a)  # Negación mediante entradas iguales

def AND_nand(a, b):
    x = NAND(a, b)  # AND negado
    return NAND(x, x)  # Segunda negación

def OR_nand(a, b):
    na = NAND(a, a)  # NOT A
    nb = NAND(b, b)  # NOT B
    return NAND(na, nb)  # De Morgan