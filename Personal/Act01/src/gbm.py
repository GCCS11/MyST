
import numpy as np

SEED = 42


def calibrate_sigma(prices, periods_per_year=98_280):
    """Volatilidad anualizada a partir de log-returns.

    98_280 = 390 minutos x 252 dias habiles.
    """
    returns = np.log(prices / prices.shift(1)).dropna()
    return float(returns.std() * np.sqrt(periods_per_year))


def simulate_gbm(s0, sigma, T, n_paths=10_000, n_steps=252, mu=0.0, seed=SEED):
    """Simula trayectorias GBM. Devuelve array (n_paths, n_steps + 1)."""
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    shocks = rng.standard_normal((n_paths, n_steps))
    increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
    log_paths = np.concatenate(
        [np.zeros((n_paths, 1)), np.cumsum(increments, axis=1)], axis=1
    )
    return s0 * np.exp(log_paths)


def terminal_moments(s0, sigma, T, mu=0.0):
    """Media y mediana teoricas de S_T."""
    return {
        "mean": s0 * np.exp(mu * T),
        "median": s0 * np.exp((mu - 0.5 * sigma**2) * T),
    }