from __future__ import annotations

from math import exp, log, pi, sqrt

from scipy.stats import norm


def black_scholes_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    volatility: float,
    option_type: str = "call",
) -> float:
    """Price a European call or put with the Black-Scholes model."""
    if spot <= 0 or strike <= 0:
        raise ValueError("spot and strike must be strictly positive")
    if maturity < 0 or volatility < 0:
        raise ValueError("maturity and volatility must be non-negative")

    option_type = option_type.lower()
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    if maturity == 0:
        payoff = max(spot - strike, 0.0)
        return payoff if option_type == "call" else max(strike - spot, 0.0)

    if volatility == 0:
        forward_pv = spot - strike * exp(-rate * maturity)
        return max(forward_pv, 0.0) if option_type == "call" else max(-forward_pv, 0.0)

    d1 = (
        log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / (volatility * sqrt(maturity))
    d2 = d1 - volatility * sqrt(maturity)

    if option_type == "call":
        return spot * norm.cdf(d1) - strike * exp(-rate * maturity) * norm.cdf(d2)

    return strike * exp(-rate * maturity) * norm.cdf(-d2) - spot * norm.cdf(-d1)


def greeks(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    volatility: float,
    option_type: str = "call",
) -> dict[str, float]:
    """Return standard Black-Scholes Greeks."""
    if maturity <= 0 or volatility <= 0:
        raise ValueError("Greeks require maturity > 0 and volatility > 0")

    d1 = (
        log(spot / strike)
        + (rate + 0.5 * volatility**2) * maturity
    ) / (volatility * sqrt(maturity))
    d2 = d1 - volatility * sqrt(maturity)
    pdf = exp(-0.5 * d1**2) / sqrt(2 * pi)

    option_type = option_type.lower()
    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (
            -spot * pdf * volatility / (2 * sqrt(maturity))
            - rate * strike * exp(-rate * maturity) * norm.cdf(d2)
        )
        rho = strike * maturity * exp(-rate * maturity) * norm.cdf(d2)
    elif option_type == "put":
        delta = norm.cdf(d1) - 1
        theta = (
            -spot * pdf * volatility / (2 * sqrt(maturity))
            + rate * strike * exp(-rate * maturity) * norm.cdf(-d2)
        )
        rho = -strike * maturity * exp(-rate * maturity) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    gamma = pdf / (spot * volatility * sqrt(maturity))
    vega = spot * pdf * sqrt(maturity)

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }


def implied_volatility(
    market_price: float,
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    option_type: str = "call",
    lower: float = 1e-6,
    upper: float = 5.0,
    tolerance: float = 1e-8,
    max_iter: int = 200,
) -> float:
    """Solve for implied volatility using bisection."""
    low, high = lower, upper

    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        price = black_scholes_price(
            spot, strike, maturity, rate, mid, option_type
        )

        if abs(price - market_price) < tolerance:
            return mid

        if price < market_price:
            low = mid
        else:
            high = mid

    return 0.5 * (low + high)
