# Derivatives Pricing & Numerical Methods

A compact, inspectable collection of **European option-pricing examples** in Python and C++. The goal is to connect pricing formulas to numerical techniques, not to provide a production trading library.

## Implemented

| File | Methods |
| --- | --- |
| [`pricing.py`](pricing.py) | Black–Scholes call/put prices, put–call parity (via model prices), Delta, Gamma, Vega, Theta, Rho, implied volatility by bisection |
| [`numerical.py`](numerical.py) | Cox–Ross–Rubinstein binomial tree for European calls/puts; Monte Carlo terminal-payoff pricing under geometric Brownian motion |
| [`black_scholes.cpp`](black_scholes.cpp) | Standalone C++ Black–Scholes example for a European call/put |

All examples assume **no dividends** and use continuously compounded rates, annualised volatility and time to maturity in **years**.

## Run the Python examples

From this directory, using Python 3.11+:

```bash
python -m pip install numpy scipy
python
```

```python
from pricing import black_scholes_price, greeks, implied_volatility
from numerical import crr_price, monte_carlo_price

params = dict(spot=100.0, strike=100.0, maturity=1.0, rate=0.03, volatility=0.20)
bs = black_scholes_price(**params, option_type="call")
tree = crr_price(**params, steps=300, option_type="call")
mc = monte_carlo_price(**params, simulations=100_000, option_type="call", seed=42)
iv = implied_volatility(bs, spot=100.0, strike=100.0, maturity=1.0, rate=0.03)
risk = greeks(**params, option_type="call")

print({"black_scholes": bs, "binomial": tree, "monte_carlo": mc, "recovered_iv": iv})
print(risk)
```

Use this example to compare numerical estimates with the closed-form reference. Monte Carlo estimates are stochastic; a fixed seed makes this example repeatable.

## Run the C++ example

```bash
g++ -std=c++17 -O2 black_scholes.cpp -o black_scholes
./black_scholes
```

On Windows, run `black_scholes.exe` after compilation.

## Methodological notes

- Black–Scholes assumes lognormal dynamics and constant volatility/rate; it is a **model benchmark**, not a market calibration system.
- The bisection implementation does **not yet validate all no-arbitrage price bounds**; supplied market prices and volatility brackets should be checked before use.
- The tree routine assumes valid CRR inputs and does not include parameter validation for degenerate cases.
- The Monte Carlo function returns a point estimate, **not a confidence interval**. Compare convergence across simulation counts before using results for analysis.
- There is no automated test suite in this small project. The larger [ARIA project](https://github.com/Enrique-JaraRon/ARIA) includes a modular pricing/risk architecture and tests.

**Scope:** educational quantitative-finance implementations; not investment advice.
