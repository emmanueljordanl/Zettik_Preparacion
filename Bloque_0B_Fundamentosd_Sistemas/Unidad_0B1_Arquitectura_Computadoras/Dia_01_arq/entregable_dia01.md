# SEGUNDA UNIVERSIDAD — VixIA
## Bloque B0-B · Unidad 0-B.1 · Día 1/8
### Lógica digital y representación binaria: del bit a la puerta

**Fecha de sesión:** 26 de octubre de 2026.  
**Estado de la sesión:** cerrada por decisión del estudiante.  
**Estado académico:** conocimientos fundamentales y depuración superados; **práctica integradora independiente y gate en frío pendientes**.  
**Marco didáctico:** `IniciarClases.md`.  
**Fuente del contenido:** `Dia-01_B0-B_U0-B.1_Logica-Digital-Representacion-Binaria.docx`.

> **Declaración de evidencia.** Las resoluciones de checkpoints y la prueba de regresión fueron realizadas o reportadas por el estudiante durante la conversación. El programa `lab/demo_logica.py`, el conjunto de pruebas `lab/test_demo_logica.py` y este informe fueron preparados por el asistente como **material de referencia y continuidad**. Sus pruebas automatizadas sí se ejecutaron en el entorno de preparación, pero no representan una implementación individual ya defendida por el estudiante.

---

## 1. Objetivo

Explicar cómo los bits codifican información; diseñar puertas y expresiones booleanas; demostrar la universalidad de NAND; construir circuitos combinacionales a partir de tablas de verdad; reconocer el desbordamiento y las consecuencias de reducir precisión en datos digitales.

## 2. Registro de aprendizaje real

| Etapa | Evidencia observada | Estado |
|---|---|---|
| Diagnóstico | Identificó robustez física del binario y funciones de las puertas; se detectó confusión inicial de rangos. | Completado |
| Concepto A | Calculó 64 configuraciones, rango 0–63 y `101101₂ = 45`. | PASS |
| Concepto B | Diseñó `(A OR B) AND NOT(S)` para alerta con modo silencioso. | PASS |
| Concepto C | Simplificó `(A+B)' + AA'` a `A'B'`. | PASS |
| Concepto D | Explicó suma binaria: XOR como suma, AND como acarreo. | PASS |
| Concepto E | Construyó NOR con NAND a partir de OR y una segunda negación. | PASS |
| Concepto F | Derivó `AB'C + ABC' + ABC` y simplificó a `AB + AC`. | PASS |
| Recuperación activa | Justificó `uint8`, `int8`, XOR, y universalidad de NAND; se reparó la limitación de AND. | Completado |
| Transferencia | Corrigió elección de bits, `uint16` y cálculo modular: `300 mod 256 = 44`. | PASS tras reintento |
| Caso límite | Distinguió entrada inválida y la decisión de rechazarla, en lugar de normalizarla sin contrato. | PASS |
| Depuración | Corrigió el `and` defectuoso de la validación por `or`. | PASS |
| Regresión | Escribió prueba con `pytest.raises(ValueError)` y comunicó que se ejecutó correctamente. | PASS reportado |
| Integrador de paridad de 3 bits | Enunciado presentado; sin respuesta individual. | PENDIENTE |
| Práctica independiente principal | No ejecutada íntegramente por el estudiante. | PENDIENTE |
| Gate en frío | No aplicado todavía. | PENDIENTE |

**Fortalezas observadas:** simplificación booleana, razonamiento con XOR/AND, construcción por NAND, identificación de errores en validación.  
**Lagunas que se corrigieron:** distinción entre `int8` y `uint8`, número mínimo de bits frente al tamaño de un tipo estándar, diferencia entre máximo 255 y ciclo modular de 256, y operadores `and`/`or` en validaciones.

---

## 3. Representación binaria y rangos

Con `n` bits existen `2^n` combinaciones. Sin signo, el rango es `0` a `2^n - 1`; con signo en complemento a dos, el rango es `-2^(n-1)` a `2^(n-1)-1`.

| Tipo | Rango mínimo | Rango máximo |
|---|---:|---:|
| uint8 | 0 | 255 |
| int8 | -128 | 127 |
| uint16 | 0 | 65 535 |
| int16 | -32 768 | 32 767 |
| uint32 | 0 | 4 294 967 295 |
| int32 | -2 147 483 648 | 2 147 483 647 |

Conversiones de referencia, con ocho bits:

| Decimal | Binario |
|---:|---|
| 42 | `00101010` |
| 127 | `01111111` |
| 255 | `11111111` |

**Derivación:** `42 = 32 + 8 + 2 = 2^5 + 2^3 + 2^1`. Por ello `42₁₀ = 00101010₂`.

## 4. Puertas y tablas de verdad

Funciones implementadas: `NOT`, `AND`, `OR`, `XOR`, `NAND` y `NOR`.

| A | B | AND | OR | XOR | NAND | NOR |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 |

| A | NOT A |
|---:|---:|
| 0 | 1 |
| 1 | 0 |

Las funciones rechazan entradas que no sean **enteros** `0` o `1` mediante `ValueError`.

## 5. Álgebra booleana: equivalencias verificadas

- De Morgan 1: `(AB)' = A' + B'`.
- De Morgan 2: `(A+B)' = A'B'`.
- Distributiva: `A(B+C) = AB + AC`.
- Idempotencia: `AA = A`, `A+A = A`.

El módulo verifica exhaustivamente estas propiedades sobre las ocho combinaciones de tres entradas, incluyendo las cuatro combinaciones de los casos de dos entradas.

## 6. XOR: suma y detección de paridad

Un medio sumador con entradas `A,B` produce:

- **Bit de suma:** `S = A XOR B`.
- **Acarreo:** `C = A AND B`.

Ejemplo: `1 + 1 = 10₂`, con `C=1` y `S=0`.

La paridad impar de una secuencia se puede calcular con XOR acumulado. Para un detector de **paridad par**, de tres entradas, se niega el XOR acumulado:

`F = NOT(XOR(XOR(A,B),C))`.

## 7. Universalidad de NAND

Se implementan, utilizando solo puertas NAND:

- `NOT(A) = NAND(A,A)`.
- `AND(A,B) = NAND(X,X)`, donde `X=NAND(A,B)`.
- `OR(A,B) = NAND(NAND(A,A),NAND(B,B))`.
- `NOR(A,B) = NAND(X,X)`, donde `X=OR_nand(A,B)`.
- `XOR(A,B)` a partir de cuatro puertas NAND.

Las cuatro combinaciones posibles de `A,B` se verifican para todas estas reconstrucciones.

## 8. Diseño combinacional de mayoría

Contrato: `F=1` cuando al menos dos de las tres entradas son 1.

| A | B | C | F |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

Forma canónica SOP: `F=A'BC + AB'C + ABC' + ABC`.  
Forma simplificada: `F=AB+AC+BC`.  
Implementación: tres puertas AND que alimentan una puerta OR de tres entradas (o su equivalente en cascada). Ambas expresiones se comparan con las ocho filas del contrato.

## 9. Integrador de paridad par de tres bits — referencia, no entregado por el estudiante

La tabla y la expresión siguientes están incluidas como **referencia técnica del asistente**; el estudiante no resolvió ni defendió aún el ejercicio en la sesión.

| A | B | C | F (número de unos par) |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 |

Expresión SOP: `F=A'B'C' + A'BC + AB'C + ABC'`.  
Expresión funcional compacta: `F=NOT(XOR(XOR(A,B),C))`.  
Verificación de referencia: ocho combinaciones contrastadas con la definición independiente `(A+B+C)%2==0`.

## 10. Overflow: NumPy frente a Python

- `np.int8(127) + np.int8(1)` produce `-128` mediante desbordamiento en el tipo fijo, con advertencia de overflow en la versión de NumPy utilizada aquí.
- `127 + 1` con `int` de Python produce `128`; el entero de Python dispone de precisión arbitraria, limitada por memoria y recursos disponibles.

**Implicación de seguridad:** un contador que desborda puede informar números incorrectos. Validar capacidad, ejecutar cálculos en tipos suficientemente amplios y comprobar el rango antes de convertir.

## 11. Cuantización ilustrativa de píxeles

Un canal original `uint8` se reduce conceptualmente a 4 bits mediante división entera entre 16.

| Valor original | Cuantizado (0–15) | Reconstruido | Error absoluto |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 128 | 8 | 128 | 0 |
| 200 | 12 | 192 | 8 |
| 255 | 15 | 240 | 15 |

**Precisión técnica:** si los valores cuantizados siguen almacenados en un array NumPy de tipo `uint8`, consumen **4 bytes** para estos cuatro valores; solo ahorrarían espacio real mediante un almacenamiento empaquetado de 4 bits por elemento, equivalente a **2 bytes** de datos en este ejemplo. Reducir precisión no implica automáticamente reducir memoria si no cambia la representación física.

## 12. Verificación realizada sobre el código de referencia

Archivos:

- `lab/demo_logica.py`: implementación ilustrativa y verificaciones exhaustivas.
- `lab/test_demo_logica.py`: pruebas automatizadas y regresión de valores inválidos.
- `resultado_pytest.txt`: salida real de la ejecución de pruebas en el entorno de preparación.
- `ejecucion_referencia.txt`: salida real de la demostración.

**Resultado obtenido en el entorno del asistente:** `16 passed`. La evidencia automatizada corresponde al **código de referencia**, no al trabajo independiente del estudiante.

Para reproducir en Linux/WSL desde el directorio del paquete:

```bash
python3 -m pip install -r requirements.txt
cd lab
python3 demo_logica.py
python3 -m pytest -v test_demo_logica.py
```

## 13. Cierre académico y continuidad

**Sesión cerrada por hoy.** No se asigna `PASS` al Día 1 completo hasta completar de forma independiente el integrador/práctica y el Gate en frío que exige `IniciarClases.md`.

**Apertura del Día 2:** verificar brevemente, sin consulta, un circuito de paridad o suma, un caso límite y la justificación de una prueba. Resolver las brechas puntuales y continuar con **aritmética binaria, complemento a dos, medio sumador, sumador completo y ALU**, respetando el temario maestro y la estructura didáctica habitual.

**Principio de avance:** la aprobación de las pruebas del material de referencia demuestra que el ejemplo funciona, pero solo la explicación, implementación y verificación del estudiante pueden acreditar dominio individual.
