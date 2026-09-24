from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
from scipy.stats import gaussian_kde, norm


def historical_var(returns, confidence: float = 0.99) -> float:
    """Positive loss VaR estimated from the empirical return distribution."""
    x = np.asarray(returns, dtype=float)
    return float(-np.quantile(x, 1.0 - confidence))


def gaussian_var(returns, confidence: float = 0.99) -> float:
    """Positive loss VaR under a Gaussian return assumption."""
    x = np.asarray(returns, dtype=float)
    mu = x.mean()
    sigma = x.std(ddof=1)
    q = mu + sigma * norm.ppf(1.0 - confidence)
    return float(-q)


def kernel_var(returns, confidence: float = 0.99) -> float:
    """Positive loss VaR estimated from a Gaussian KDE."""
    x = np.asarray(returns, dtype=float)
    kde = gaussian_kde(x)
    target = 1.0 - confidence

    lo = x.min() - 5.0 * x.std(ddof=1)
    hi = x.max() + 5.0 * x.std(ddof=1)

    def objective(q: float) -> float:
        return kde.integrate_box_1d(-np.inf, q) - target

    quantile = brentq(objective, lo, hi)
    return float(-quantile)


def expected_shortfall(returns, var: float) -> float:
    """Average loss conditional on exceeding the supplied VaR threshold."""
    x = np.asarray(returns, dtype=float)
    tail = x[x < -var]
    if tail.size == 0:
        return float("nan")
    return float(-tail.mean())
