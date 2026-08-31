
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"


def load_frozen_session(ticker, date="2026-08-28"):
    """Devuelve las barras de 1 minuto de ese ticker y dia."""
    path = DATA_DIR / f"{ticker}_{date}_1m.csv"
    if not path.exists():
        raise FileNotFoundError(f"No existe {path.name}. Corre scripts/download_data.py")
    return pd.read_csv(path, index_col=0, parse_dates=True)