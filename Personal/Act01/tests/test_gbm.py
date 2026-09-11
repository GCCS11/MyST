
import numpy as np

from src.gbm import simulate_gbm, terminal_moments

S0, SIGMA, T = 100.0, 0.20, 1.0


def test_mean_median_identity():
    """La media y mediana simuladas caen dentro de 3 errores estandar."""
    terminal = simulate_gbm(S0, SIGMA, T)[:, -1]
    theory = terminal_moments(S0, SIGMA, T)
    se = terminal.std(ddof=1) / np.sqrt(len(terminal))

    assert abs(terminal.mean() - theory["mean"]) < 3 * se
    assert abs(np.median(terminal) - theory["median"]) < 3 * se


def test_ito_correction_present():
    """Sin la correccion de Ito la media saldria sesgada hacia arriba."""
    terminal = simulate_gbm(S0, SIGMA, T)[:, -1]
    assert terminal.mean() > np.median(terminal)