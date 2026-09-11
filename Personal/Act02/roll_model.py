
import numpy as np


def roll_covariance(price: np.ndarray) -> float:
    """Cov(dP_t, dP_{t-1}) sobre una serie de precios."""
    price = np.asarray(price, dtype=float)
    dp = np.diff(price)
    if len(dp) < 3:
        return np.nan
    cov_matrix = np.cov(dp[1:], dp[:-1])
    return cov_matrix[0, 1]


def roll_estimator(price: np.ndarray):
    """
    Estimador de Roll: s = 2*sqrt(-Cov(dP_t, dP_{t-1})), sigma_u^2 = Var(dP_t) - s^2/2.
    Retorna (s, sigma_u, cov). Si cov >= 0, s = np.nan (NO se fuerza con abs()).
    """
    price = np.asarray(price, dtype=float)
    dp = np.diff(price)
    cov = roll_covariance(price)

    if cov < 0:
        s = 2.0 * np.sqrt(-cov)
    else:
        s = np.nan  # no definido bajo el modelo: Cov >= 0 no tiene raiz real valida

    var_dp = np.var(dp[1:], ddof=1) if len(dp) > 2 else np.nan
    if not np.isnan(s):
        sigma_u2 = var_dp - (s ** 2) / 2.0
        sigma_u = np.sqrt(sigma_u2) if sigma_u2 > 0 else np.nan
    else:
        sigma_u = np.nan

    return s, sigma_u, cov


def infer_trade_direction(price: np.ndarray) -> np.ndarray:
    """
    Regla de tick: q_t = +1 si sube, -1 si baja, hereda el signo anterior si no cambia.
    """
    price = np.asarray(price, dtype=float)
    n = len(price)
    q = np.zeros(n)
    q[0] = 1.0
    for t in range(1, n):
        diff = price[t] - price[t - 1]
        if diff > 0:
            q[t] = 1.0
        elif diff < 0:
            q[t] = -1.0
        else:
            q[t] = q[t - 1]
    return q


def roll_efficient_price(price: np.ndarray, s: float, q: np.ndarray) -> np.ndarray:
    """Precio eficiente: m_t = p_t - (s/2) * q_t."""
    price = np.asarray(price, dtype=float)
    q = np.asarray(q, dtype=float)
    if np.isnan(s):
        raise ValueError("s es nan: no se puede reconstruir m_t sin un spread valido.")
    return price - (s / 2.0) * q