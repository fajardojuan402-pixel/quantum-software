"""Challenge 2: Entanglement

Objective: Create a Bell pair and observe correlations.

Time: 8-10 minutes
Level: Intermediate
"""

from qiskit import QuantumCircuit
from quantum_lab.simulator import run_circuit
from quantum_lab.utils import format_counts


def create_bell_pair() -> QuantumCircuit:
    """Create a two-qubit Bell pair circuit with measurements.

    TODO: Complete the circuit:
    1. Apply H to the first qubit
    2. Apply CX with control = first qubit, target = second qubit
    3. Measure both qubits

    Expected in ideal simulation: only 00 and 11.
    """
    qc = QuantumCircuit(2, 2)

    # H on qubit 0 -> superposition on the control qubit
    qc.h(0)

    # CX control=0, target=1 -> entangles both qubits into a Bell pair
    qc.cx(0, 1)

    # Measure both qubits
    qc.measure([0, 1], [0, 1])

    return qc


def main():
    print("=== Challenge 2: Entanglement ===\n")
    print("PREDICT: Which binary strings do you expect to see?")
    print("Why should 01 and 10 be absent in ideal simulation?\n")

    qc = create_bell_pair()
    counts = run_circuit(qc, shots=1024, seed=42)
    print(format_counts(counts))

    print("\nREFLECT:")
    print("- Which outcomes appeared?")
    print("- Note: Observing correlation in one measurement basis is not sufficient")
    print("  to experimentally prove entanglement. Additional bases are needed.")


if __name__ == "__main__":
    main()
