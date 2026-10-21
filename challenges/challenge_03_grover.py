"""Challenge 3: Grover with 2 qubits (educational)

Objective: Implement a simplified Grover search that marks one state.

Time: 10-12 minutes
Level: Intermediate

This is a didactic example only. It does not demonstrate practical
speedup over a classical CPU for four options.
"""

from qiskit import QuantumCircuit
from quantum_lab.simulator import run_circuit, get_statevector
from quantum_lab.utils import format_counts


def oracle_mark_11() -> QuantumCircuit:
    """Oracle that marks the state |11> by applying a phase of -1.

    For educational purposes, a simple Z on both qubits when both are 1
    can be approximated, but we use a controlled-Z equivalent.
    """
    oracle = QuantumCircuit(2, name="Oracle")
    # Mark |11> with a phase flip (equivalent to CZ for this case)
    oracle.cz(0, 1)
    return oracle


def oracle_mark(marked: str = "11") -> QuantumCircuit:
    """Oracle that marks any 2-qubit computational state with a phase of -1.

    To mark a state we flip (X) the qubits that should be 0, apply a CZ that
    only adds the -1 phase to |11>, then undo the X gates. This turns the CZ
    into a phase flip on the chosen ``marked`` state.

    Args:
        marked: Two-character string such as "00", "01", "10" or "11". The
            convention follows Qiskit counts, where the left character is
            qubit 1 and the right character is qubit 0.
    """
    if len(marked) != 2 or any(c not in "01" for c in marked):
        raise ValueError(f"'marked' must be a 2-bit string of 0/1, got {marked!r}")

    # marked[0] -> qubit 1, marked[1] -> qubit 0 (Qiskit little-endian ordering)
    zeros = [q for q, bit in ((1, marked[0]), (0, marked[1])) if bit == "0"]

    oracle = QuantumCircuit(2, name=f"Oracle[{marked}]")
    if zeros:
        oracle.x(zeros)
    oracle.cz(0, 1)
    if zeros:
        oracle.x(zeros)
    return oracle


def diffusion_operator() -> QuantumCircuit:
    """Incomplete diffusion operator for 2 qubits.

    TODO: Complete the diffusion (inversion about the mean):
    - H on both qubits
    - X on both qubits
    - CZ (or controlled phase)
    - X on both qubits
    - H on both qubits
    """
    diff = QuantumCircuit(2, name="Diffusion")

    # Inversion about the mean (2|s><s| - I) for 2 qubits:
    # H on both
    diff.h([0, 1])

    # X on both
    diff.x([0, 1])

    # Controlled phase (CZ) flips the phase of the |11> component
    diff.cz(0, 1)

    # X on both
    diff.x([0, 1])

    # H on both
    diff.h([0, 1])

    return diff


def grover_circuit(marked: str = "11") -> QuantumCircuit:
    """Build one iteration of Grover for 2 qubits.

    Args:
        marked: Which state to mark. Any 2-qubit state is supported
            ("00", "01", "10" or "11"); defaults to "11".
    """
    qc = QuantumCircuit(2, 2)

    # Initial superposition
    qc.h([0, 1])

    # Oracle: mark the requested state with a phase flip.
    qc.compose(oracle_mark(marked), inplace=True)

    # Diffusion
    qc.compose(diffusion_operator(), inplace=True)

    # Measure
    qc.measure([0, 1], [0, 1])
    return qc


def main():
    print("=== Challenge 3: Grover (2 qubits, educational) ===\n")
    print("PREDICT: After one iteration, which state should have probability close to 1?\n")

    qc = grover_circuit("11")
    counts = run_circuit(qc, shots=1024, seed=42)
    print(format_counts(counts))

    print("\nREFLECT:")
    print("- Did the marked state dominate?")
    print("- This is a teaching example. It is NOT evidence of practical quantum speedup")
    print("  for a search space of only 4 elements.")
    print("- Grover does not 'read all states at once'.")


if __name__ == "__main__":
    main()
