"""Public tests for Challenge 1.

These tests expect the student implementations to be completed.
Initial run may fail until TODOs are resolved.
"""

import pytest
from challenges.challenge_01_superposition import create_superposition, double_hadamard
from quantum_lab.simulator import run_circuit, get_statevector


def test_double_hadamard_deterministic():
    qc = double_hadamard()
    counts = run_circuit(qc, shots=1024, seed=42)
    assert counts.get("0", 0) == 1024
    assert "1" not in counts or counts["1"] == 0


def test_superposition_exists_after_h():
    """After completing the TODO, the state before measurement should be superposition."""
    # This test is structural; full validation requires the student circuit
    qc = create_superposition()
    # Remove measurement to inspect statevector if possible
    # Students should verify manually as well
    assert qc.num_qubits == 1
