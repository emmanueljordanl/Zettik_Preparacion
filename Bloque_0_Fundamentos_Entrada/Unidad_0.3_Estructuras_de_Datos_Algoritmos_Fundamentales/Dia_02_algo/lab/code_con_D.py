class Pila:
    """Pila LIFO. Todas las operaciones son O(1)."""

    def __init__(self):
        self._datos: list = []  # array dinamico interno

    def push(self, x) -> None:
        self._datos.append(x)  # anadir al final: O(1) amortizado

    def pop(self):
        if self.esta_vacia():
            raise IndexError("pop de una pila vacia")
        return self._datos.pop()  # quitar del final: O(1)

    def peek(self):
        if self.esta_vacia():
            raise IndexError("peek de una pila vacia")
        return self._datos[-1]  # consultar el final: O(1)

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0  # O(1)

    def __len__(self) -> int:
        return len(self._datos)


# Comportamiento LIFO: el ultimo en entrar es el primero en salir
p = Pila()
for x in [1, 2, 3]:
    p.push(x)
print(p.pop(), p.pop(), p.pop())  # 3 2 1  (orden inverso al de insercion: LIFO)


# Aplicacion: verificar parentesis balanceados (uso clasico de pila)
def parentesis_balanceados(texto: str) -> bool:
    pila = Pila()
    pares = {")": "(",
             "]": "[",
             "}": "{"}
    for c in texto:
        if c in "([{":
            pila.push(c)  # apertura: apilar
        elif c in ")]}":
            if pila.esta_vacia() or pila.pop() != pares[c]:
                return False  # cierre sin apertura correspondiente
    return pila.esta_vacia()  # balanceado si no quedan aperturas


print(parentesis_balanceados("(a[b]{c})"))  # True
print(parentesis_balanceados("()[]{}"))  # False
