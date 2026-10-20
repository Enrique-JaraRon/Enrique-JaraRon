# Market Risk & VaR Analytics

Small Python implementations illustrating how **tail-risk estimates depend on distributional assumptions**, and how observed loss exceptions can be checked against a stated confidence level.

## Implemented

| File | Functionality |
| --- | --- |
| [`var_models.py`](var_models.py) | Historical (empirical-quantile) VaR, Gaussian parametric VaR, Gaussian kernel-density VaR, empirical Expected Shortfall |
| [`backtest.py`](backtest.py) | Indicator for VaR violations, observed violation rate, expected exception rate, simple summary of their difference |

**Convention:** input returns are **decimal simple returns** (e.g. `-0.02` means −2%). VaR and Expected Shortfall are returned as **positive loss magnitudes** where applicable. A violation occurs when `return < -VaR`.

## Run an example

From this directory, using Python 3.11+:

```bash
python -m pip install numpy scipy
python
```

```python
import numpy as np
from var_models import historical_var, gaussian_var, kernel_var, expected_shortfall
from backtest import backtest_summary

# Synthetic illustration; these are not observed market returns.
rng = np.random.default_rng(42)
returns = rng.normal(loc=0.0002, scale=0.01, size=2_000)
train, test = returns[:1_500], returns[1_500:]

confidence = 0.99
var_historical = historical_var(train, confidence)
var_gaussian = gaussian_var(train, confidence)
var_kde = kernel_var(train, confidence)
es_historical = expected_shortfall(train, var_historical)

print({"historical_var": var_historical, "gaussian_var": var_gaussian,
       "kernel_var": var_kde, "historical_es": es_historical})

# Estimate the fixed threshold on training data; inspect exceptions on held-out data.
print(backtest_summary(test, var_historical, confidence))
```

## Interpretation

- **Historical VaR:** empirical lower-tail quantile; sensitive to sample size and regime changes.
- **Gaussian VaR:** uses sample mean and volatility under a normal-return approximation; heavy tails may be missed.
- **Kernel VaR:** estimates the return distribution non-parametrically; bandwidth and sample size matter.
- **Expected Shortfall:** averages realised sample losses exceeding a supplied threshold. The function returns `NaN` if no observation exceeds the threshold.

## Important limitations

- `backtest_summary` reports **exception frequency only**. It does **not implement** a rolling forecast engine, Kupiec unconditional-coverage test or Christoffersen independence test.
- The example's train/test split illustrates separation of estimation and evaluation, but a proper historical market-risk study should use **time-ordered forecasts**, appropriate horizons and multiple regimes.
- The functions do not validate every edge case (missing values, very small or constant samples, extreme confidence levels).
- These are educational estimators, not a regulatory VaR model or a complete market-risk system.

For an interactive portfolio-risk application with stress testing and reporting, see [ARIA](https://github.com/Enrique-JaraRon/ARIA).
