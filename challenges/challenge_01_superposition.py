"""Challenge 1: Superposition

Objective: Explore the Hadamard gate and measurement.

Time: 5-8 minutes
Level: Beginner
"""

from qiskit import QuantumCircuit
from quantum_lab.simulator import run_circuit, get_statevector
from quantum_lab.utils import format_counts


def create_superposition() -> QuantumCircuit:
    """Create a 1-qubit circuit that prepares superposition and measures.

    TODO: Complete the circuit so that it:
    1. Starts in |0>
    2. Applies a Hadamard (H) gate
    3. Measures the qubit

    Returns:
        QuantumCircuit with measurement.
    """
    qc = QuantumCircuit(1, 1)

    # Apply H gate to qubit 0 -> creates an equal superposition of |0> and |1>
    qc.h(0)

    # Measure qubit 0 into classical bit 0
    qc.measure(0, 0)

    return qc


def double_hadamard() -> QuantumCircuit:
    """Create a circuit with two successive Hadamard gates.

    H then H should return the qubit to |0> in ideal simulation.
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def main():
    print("=== Challenge 1: Superposition ===\n")
    print("PREDICT before running:")
    print("1. What approximate distribution do you expect for a single H + measure (1024 shots)?")
    print("2. What should happen with H + H + measure?\n")

    print("--- Single Hadamard ---")
    qc1 = create_superposition()
    counts1 = run_circuit(qc1, shots=1024, seed=42)
    print(format_counts(counts1))

    print("\n--- Double Hadamard ---")
    qc2 = double_hadamard()
    counts2 = run_circuit(qc2, shots=1024, seed=42)
    print(format_counts(counts2))

    print("\nREFLECT:")
    print("- Did the results match your prediction?")
    print("- Why does H+H return only 0 in the ideal simulator?")
    print("- A single measurement does not return all possibilities of the superposition.")


if __name__ == "__main__":
    main()
