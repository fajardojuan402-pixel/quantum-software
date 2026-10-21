# Concepts

## Superposition

A qubit can be in a linear combination of |0> and |1>. The Hadamard gate creates an equal superposition. Measuring collapses the state to one of the basis states with a probability given by the amplitudes squared.

A single measurement does not return all possibilities of the superposition.

## Entanglement

Two or more qubits can be in a joint state that cannot be described independently. The Bell state (produced by H + CX) shows perfect correlation: measuring one immediately determines the other in the computational basis. Correlation in one basis alone is not sufficient experimental proof of entanglement.

## Grover's Algorithm (educational)

Grover's search amplifies the amplitude of a marked state. For two qubits and one marked solution, a single iteration is enough to make the marked state have probability close to 1 in ideal simulation. This is a teaching example only and does not demonstrate practical advantage over classical search for four items.

## Measurement

Measurement is a destructive process that returns a classical bit string according to the Born rule. Ideal simulators allow us to explore the pure quantum behavior without noise.

## Relation to Software Engineering

- Probabilistic tests require statistical margins or deterministic methods (statevector).
- Simulator is an adapter between the quantum circuit API and a classical backend.
- Separation of concerns: circuit construction, execution, and result analysis.
- Reproducibility via seeds.
- Hybrid architecture: classical control + quantum accelerator.
