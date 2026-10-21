"""Challenge 4: Quantum Testing

Objective: Distinguish deterministic from probabilistic results using pytest.

Time: 8-10 minutes
Level: Intermediate
"""

import numpy as np
import pytest
from qiskit import QuantumCircuit
from quantum_lab.simulator import run_circuit, get_statevector


def circuit_h_then_h() -> QuantumCircuit:
    """Deterministic circuit: H + H returns to |0>."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def circuit_single_h() -> QuantumCircuit:
    """Probabilistic circuit: single H."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


# Tests completed below.
# Run with: pytest -q challenges/challenge_04_testing.py

def test_double_hadamard_is_deterministic():
    """H + H must return only 0 in ideal simulation."""
    qc = circuit_h_then_h()
    counts = run_circuit(qc, shots=1024, seed=42)
    # This assertion is correct
    assert counts.get("0", 0) == 1024


def test_single_hadamard_is_probabilistic():
    """Single H should be roughly 50/50. Do not require exact equality."""
    qc = circuit_single_h()
    counts = run_circuit(qc, shots=1024, seed=42)
    count_0 = counts.get("0", 0)
    # An exact `== 512` would be too strict: a single H is probabilistic and
    # shot counts fluctuate around 512. We keep the base assertion with a margin.
    assert abs(count_0 - 512) < 100  # Reasonable margin


def test_grover_marks_correct_state():
    """After one Grover iteration the marked state should dominate."""
    # Import the function from the challenge (student must complete it)
    from challenges.challenge_03_grover import grover_circuit
    qc = grover_circuit("11")
    counts = run_circuit(qc, shots=1024, seed=42)
    # The marked state "11" should have the large majority of shots
    assert counts.get("11", 0) > 800


def test_bell_pair_only_correlated_outcomes():
    """Bell pair: only '00' and '11' appear and together they sum all shots."""
    from challenges.challenge_02_entanglement import create_bell_pair
    shots = 1024
    counts = run_circuit(create_bell_pair(), shots=shots, seed=42)
    assert set(counts).issubset({"00", "11"})
    assert counts.get("00", 0) + counts.get("11", 0) == shots


def test_double_hadamard_statevector_is_zero():
    """Deterministic via statevector: H+H (no measurement) yields exactly |0>."""
    # Build H+H without measurements so get_statevector can inspect the ideal state.
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.h(0)
    state = get_statevector(qc)
    # Ideal |0> amplitude vector is [1, 0]; compare without relying on shots.
    assert np.allclose(state.data, [1.0, 0.0])


def test_same_seed_is_reproducible():
    """Reproducibility: two runs with the same seed give identical counts."""
    qc = circuit_single_h()
    counts_a = run_circuit(qc, shots=1024, seed=123)
    counts_b = run_circuit(qc, shots=1024, seed=123)
    assert counts_a == counts_b


def test_single_hadamard_probabilistic_with_margin():
    """Probabilistic with margin: single H over 4096 shots stays near 50/50."""
    shots = 4096
    counts = run_circuit(circuit_single_h(), shots=shots, seed=42)
    count_0 = counts.get("0", 0)
    # Margin rationale: for a fair coin the shot count has standard deviation
    # sqrt(shots * 0.5 * 0.5) = 32. A tolerance of 0.05 * shots ~= 205 covers
    # roughly +/-6 sigma, so a correct circuit practically never fails this test.
    assert abs(count_0 - shots / 2) < 0.05 * shots


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
