
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"


def load_ohlcv(ticker: str = "BTC-USD", interval: str = "1d") -> pd.DataFrame:
    path = DATA_DIR / f"{ticker}_{interval}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path.name}. Corre scripts/download_data.py"
        )
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.columns = [c.lower() for c in df.columns]
    return df
