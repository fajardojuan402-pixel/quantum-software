"""Public tests for Challenge 4 (testing patterns)."""

import pytest
from challenges.challenge_04_testing import (
    test_double_hadamard_is_deterministic,
    test_single_hadamard_is_probabilistic,
    test_grover_marks_correct_state,
    test_bell_pair_only_correlated_outcomes,
    test_double_hadamard_statevector_is_zero,
    test_same_seed_is_reproducible,
    test_single_hadamard_probabilistic_with_margin,
)
