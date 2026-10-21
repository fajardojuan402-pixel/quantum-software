"""Demonstration mode that works without completing the challenges.

Verifies that the installation and simulator are working correctly.
"""

from qiskit import QuantumCircuit
from quantum_lab.simulator import run_circuit
from quantum_lab.utils import format_counts


def demo_classical_x() -> None:
    """Prepare |0>, apply X, measure. Should always return 1 in ideal simulation."""
    print("=== Quantum Software Lab - Installation Demo ===")
    print("Preparing a single-qubit circuit: |0> -> X -> measure")
    print("Expected result (ideal simulator): only |1>\n")

    qc = QuantumCircuit(1, 1)
    qc.x(0)
    qc.measure(0, 0)

    counts = run_circuit(qc, shots=1024, seed=42)
    print("Results:")
    print(format_counts(counts))

    if counts.get("1", 0) == 1024:
        print("\nSUCCESS: Installation is correct. You can now work on the challenges.")
    else:
        print("\nWARNING: Unexpected result. Check your environment.")


if __name__ == "__main__":
    demo_classical_x()
