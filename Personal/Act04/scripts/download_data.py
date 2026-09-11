
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKER = "BTC-USD"
INTERVAL = "1d"
START = "2020-01-01"
DATA_DIR = Path(__file__).parent.parent / "data"


def download(ticker: str, start: str, interval: str):
    df = yf.download(ticker, start=start, interval=interval,
                     progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"{ticker}: sin barras desde {start}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Open", "High", "Low", "Close", "Volume"]]


DATA_DIR.mkdir(exist_ok=True)
df = download(TICKER, START, INTERVAL)
path = DATA_DIR / f"{TICKER}_{INTERVAL}.csv"
df.to_csv(path)
print(f"{TICKER} -> {len(df):,} barras "
      f"({df.index.min():%Y-%m-%d} a {df.index.max():%Y-%m-%d}) -> {path.name}")
