# Solución del taller — Quantum Software Lab

En este documento dejo cómo resolví cada reto y qué me salió al correrlos. Trabajé los
cuatro retos del laboratorio, uno por uno, prediciendo primero qué esperaba ver y después
comparando con la ejecución real.

## Reto 1 — Superposición

Este fue el más sencillo y me sirvió para entender el flujo de todo el taller. Había que
armar un circuito de un qubit, aplicarle una compuerta Hadamard y medir.

```python
qc = QuantumCircuit(1, 1)
qc.h(0)          # pone el qubit en superposición
qc.measure(0, 0)
```

Antes de ejecutarlo pensé que el Hadamard simple me iba a dar algo cercano a mitad y mitad
entre `0` y `1`, pero no exactamente 512 y 512, porque al final es un proceso aleatorio y
los conteos se mueven un poco. Para el caso de aplicar dos Hadamard seguidos sí estaba casi
seguro de que iba a volver todo a `0`, aunque quería confirmarlo corriéndolo.

Al ejecutarlo me salió esto:

```text
(.venv) C:\Users\david\Desktop\Nueva carpeta> python challenges\challenge_01_superposition.py
=== Challenge 1: Superposition ===

--- Single Hadamard ---
  |0> : 526 (51.4%)
  |1> : 498 (48.6%)

--- Double Hadamard ---
  |0> : 1024 (100.0%)
```

Coincidió con lo que esperaba. El Hadamard simple quedó en 526 contra 498, bien cerca del
50/50, y el doble Hadamard dio los 1024 tiros en `0`. La razón de esto último es que el
Hadamard es su propia inversa: aplicarlo dos veces deshace la superposición y el qubit
regresa a donde estaba. Lo que me quedó claro es que una sola medición no me muestra
"todas" las posibilidades de la superposición, solo colapsa a un resultado.

## Reto 2 — Entrelazamiento

Acá armé un par de Bell, que es el ejemplo clásico de entrelazamiento. La idea es poner el
primer qubit en superposición con un Hadamard y luego usar una CNOT para que el segundo
quede atado al primero.

```python
qc = QuantumCircuit(2, 2)
qc.h(0)                    # superposición en el qubit de control
qc.cx(0, 1)                # enlaza el qubit 1 con el 0
qc.measure([0, 1], [0, 1])
```

Mi predicción era que solo iban a aparecer `00` y `11`, cada uno más o menos la mitad de las
veces, y que `01` y `10` no iban a salir nunca. Tenía algo de duda con el reparto exacto
entre `00` y `11`, pero del resto estaba tranquilo.

```text
(.venv) C:\Users\david\Desktop\Nueva carpeta> python challenges\challenge_02_entanglement.py
=== Challenge 2: Entanglement ===

  |00> : 521 (50.9%)
  |11> : 503 (49.1%)
```

Salió justo así: 521 veces `00` y 503 veces `11`, sin un solo `01` ni `10`. Los dos qubits
siempre salen iguales porque el estado de Bell no tiene componentes mezcladas; cuando mido
uno, el otro ya queda determinado.

Hay un detalle que me pareció importante y es que ver esta correlación en una sola base no
alcanza para afirmar que hay entrelazamiento. Una fuente clásica correlacionada daría el
mismo 00/11 en esta base. Para distinguir el entrelazamiento de verdad habría que medir
también en otras bases.

## Reto 3 — Grover

Este fue el más interesante y donde más tuve que pensar. Primero completé el operador de
difusión, que es la parte que amplifica la amplitud del estado marcado. El oráculo que ya
venía marcaba el estado `11` con un cambio de fase usando una CZ.

```python
diff = QuantumCircuit(2, name="Diffusion")
diff.h([0, 1])
diff.x([0, 1])
diff.cz(0, 1)
diff.x([0, 1])
diff.h([0, 1])
```

Al correr una iteración con el estado marcado `11` esperaba que ese estado quedara con casi
toda la probabilidad, y efectivamente se llevó todo:

```text
(.venv) C:\Users\david\Desktop\Nueva carpeta> python challenges\challenge_03_grover.py
=== Challenge 3: Grover (2 qubits, educational) ===

  |11> : 1024 (100.0%)
```

Una aclaración sobre la matemática de la difusión. La secuencia `H-X-CZ-X-H` implementa
`I - 2|s><s|`, que es lo mismo que `2|s><s| - I` salvo un signo global de `-1`. Ese signo
global no cambia las probabilidades que se miden, así que las dos formas describen la misma
difusión de Grover en la práctica.

### Extensión: marcar cualquier estado

Quise ir un poco más allá y que Grover funcionara para los cuatro estados de dos qubits, no
solo para `11`. Agregué una función `oracle_mark(marked)` que marca el estado que uno le
pida. El truco es aplicar una X a los qubits que deberían valer 0, después la CZ (que solo
mete la fase sobre `11`) y volver a aplicar la X para deshacer. Con eso la CZ termina
marcando el estado que elegí. Mantuve la firma original `grover_circuit(marked="11")` para
no romper nada de lo que ya estaba.

Probé los cuatro casos y cada estado marcado se lleva el 100% de los tiros:

```text
(.venv) C:\Users\david\Desktop\Nueva carpeta> python -c "from challenges.challenge_03_grover import grover_circuit; from quantum_lab.simulator import run_circuit; [print(m, '->', run_circuit(grover_circuit(m), shots=1024, seed=42)) for m in ['00','01','10','11']]"
00 -> {'00': 1024}
01 -> {'01': 1024}
10 -> {'10': 1024}
11 -> {'11': 1024}
```

Dos cosas que quiero dejar anotadas para no engañarme a mí mismo. Con solo cuatro opciones
esto no demuestra ninguna ventaja real frente a una búsqueda clásica, que las revisa en muy
pocos pasos; el beneficio de Grover se nota cuando el espacio de búsqueda es enorme. Y Grover
tampoco "lee todos los estados al tiempo": la superposición existe antes de medir, pero al
medir colapsa a un único resultado. Lo que hace el algoritmo es subir la amplitud del estado
correcto para que, cuando mida, salga con alta probabilidad.

## Reto 4 — Pruebas

En este reto el foco era aprender a escribir pruebas para circuitos cuánticos, distinguiendo
lo que es determinista de lo que es probabilístico. El código base ya traía los tres tests
originales funcionando, incluido el del Hadamard simple, que usa un margen en lugar de exigir
exactamente 512 (eso fallaría por la variación normal de los tiros). Mi trabajo acá fue
sumar cuatro pruebas nuevas:

- Una que verifica que el par de Bell solo produce `00` y `11`, y que la suma de los dos da
  el total de tiros.
- Una determinista de verdad: tomo el statevector de `H + H` sin medir y confirmo con
  `numpy.allclose` que el estado quedó en `|0>`. Al no depender de los tiros, siempre da el
  mismo resultado.
- Una de reproducibilidad: corro el mismo circuito dos veces con la misma semilla y compruebo
  que los conteos son idénticos.
- Una probabilística con 4096 tiros y un margen amplio, suficiente para que un circuito
  correcto nunca falle por azar pero sí detecte si algo está mal armado.

Para que estas pruebas corrieran junto con las demás tuve que agregarlas también en
`tests/test_challenge_04.py`, que es el archivo que reúne por nombre los tests del reto.

La idea de fondo que me llevo es que con resultados probabilísticos uno no puede pedir
igualdad exacta: o usa un margen razonable, o busca una forma determinista como mirar el
statevector. Y la semilla es clave para poder repetir los experimentos.

## Pruebas

Corrí toda la suite y pasaron las 15 pruebas:

```text
(.venv) C:\Users\david\Desktop\Nueva carpeta> $env:PYTHONPATH = "$PWD;$PWD\src"; pytest -q
...............                                                          [100%]
15 passed in 1.07s
```

El demo de instalación también quedó bien, con el circuito `|0> -> X -> medición` devolviendo
solo `1`:

```text
(.venv) C:\Users\david\Desktop\Nueva carpeta> python -m quantum_lab.demo
=== Quantum Software Lab - Installation Demo ===
Preparing a single-qubit circuit: |0> -> X -> measure
Expected result (ideal simulator): only |1>

Results:
  |1> : 1024 (100.0%)

SUCCESS: Installation is correct. You can now work on the challenges.
```

## Entorno

Ejecuté todo en Windows 11, con Python 3.14.0, Qiskit 2.6.0 y Qiskit Aer 0.17.2.
