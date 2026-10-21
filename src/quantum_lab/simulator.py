"""Simulator utilities for the lab.

Provides a consistent interface to AerSimulator for educational purposes.
"""

from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


def get_simulator(seed: int | None = None) -> AerSimulator:
    """Return a local AerSimulator instance.

    Args:
        seed: Optional seed for reproducible shots.

    Returns:
        Configured AerSimulator.
    """
    backend = AerSimulator()
    if seed is not None:
        backend.set_options(seed_simulator=seed)
    return backend


def run_circuit(circuit, shots: int = 1024, seed: int | None = None):
    """Execute a circuit on the local simulator and return counts.

    Args:
        circuit: QuantumCircuit with measurements.
        shots: Number of shots.
        seed: Optional seed for reproducibility.

    Returns:
        dict of measurement counts.
    """
    backend = get_simulator(seed)
    job = backend.run(circuit, shots=shots)
    result = job.result()
    return result.get_counts()


def get_statevector(circuit) -> Statevector:
    """Return the ideal statevector of a circuit (no measurements).

    Useful for deterministic validation of ideal circuits.
    """
    return Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
