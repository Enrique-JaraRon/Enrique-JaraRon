from __future__ import annotations

import numpy as np


def var_violations(returns, var: float) -> np.ndarray:
    """Boolean array indicating losses greater than VaR."""
    x = np.asarray(returns, dtype=float)
    return x < -var


def violation_ratio(returns, var: float) -> float:
    """Observed fraction of VaR violations."""
    violations = var_violations(returns, var)
    return float(violations.mean())


def expected_violation_rate(confidence: float) -> float:
    return 1.0 - confidence


def backtest_summary(returns, var: float, confidence: float = 0.99) -> dict[str, float]:
    observed = violation_ratio(returns, var)
    expected = expected_violation_rate(confidence)

    return {
        "observed_violation_rate": observed,
        "expected_violation_rate": expected,
        "difference": observed - expected,
    }
