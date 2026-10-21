"""Public tests for Challenge 3."""

import pytest
from challenges.challenge_03_grover import grover_circuit
from quantum_lab.simulator import run_circuit


def test_grover_marks_11():
    qc = grover_circuit("11")
    counts = run_circuit(qc, shots=1024, seed=42)
    # Marked state should dominate after one iteration
    assert counts.get("11", 0) > 800


@pytest.mark.parametrize("marked", ["00", "01", "10", "11"])
def test_grover_marks_any_state(marked):
    """Each 2-qubit marked state should dominate after one iteration."""
    qc = grover_circuit(marked)
    counts = run_circuit(qc, shots=1024, seed=42)
    assert counts.get(marked, 0) > 800
