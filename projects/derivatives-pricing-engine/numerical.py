from __future__ import annotations

from math import exp, sqrt

import numpy as np


def crr_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    volatility: float,
    steps: int = 200,
    option_type: str = "call",
) -> float:
    """Cox-Ross-Rubinstein price of a European option."""
    dt = maturity / steps
    up = exp(volatility * sqrt(dt))
    down = 1.0 / up
    q = (exp(rate * dt) - down) / (up - down)

    j = np.arange(steps + 1)
    terminal_spots = spot * up ** (steps - j) * down**j

    if option_type.lower() == "call":
        values = np.maximum(terminal_spots - strike, 0.0)
    else:
        values = np.maximum(strike - terminal_spots, 0.0)

    disc = exp(-rate * dt)
    for _ in range(steps):
        values = disc * (q * values[:-1] + (1.0 - q) * values[1:])

    return float(values[0])


def monte_carlo_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    volatility: float,
    simulations: int = 100_000,
    option_type: str = "call",
    seed: int = 42,
) -> float:
    """Monte Carlo price of a European option under GBM."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(simulations)

    terminal_spot = spot * np.exp(
        (rate - 0.5 * volatility**2) * maturity
        + volatility * sqrt(maturity) * z
    )

    if option_type.lower() == "call":
        payoff = np.maximum(terminal_spot - strike, 0.0)
    else:
        payoff = np.maximum(strike - terminal_spot, 0.0)

    return float(exp(-rate * maturity) * payoff.mean())
