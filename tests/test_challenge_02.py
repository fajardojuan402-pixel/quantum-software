"""Public tests for Challenge 2."""

import pytest
from challenges.challenge_02_entanglement import create_bell_pair
from quantum_lab.simulator import run_circuit


def test_bell_pair_outcomes():
    qc = create_bell_pair()
    counts = run_circuit(qc, shots=2048, seed=42)
    # Only 00 and 11 should appear in ideal simulation
    allowed = {"00", "11"}
    for outcome in counts:
        assert outcome in allowed, f"Unexpected outcome {outcome}"
    # Both should appear with high probability
    assert counts.get("00", 0) > 500
    assert counts.get("11", 0) > 500
