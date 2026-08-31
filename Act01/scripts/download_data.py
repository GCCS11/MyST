
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKERS = {"liquid": "AAPL", "illiquid": "SIF"}
SESSION_DATE = "2026-08-28"
DATA_DIR = Path(__file__).parent.parent / "data"


def download_session(ticker, date):
    start = pd.Timestamp(date)
    df = yf.download(ticker, start=start, end=start + pd.Timedelta(days=1),
                     interval="1m", progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"{ticker}: sin barras para {date}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Open", "High", "Low", "Close", "Volume"]]


DATA_DIR.mkdir(exist_ok=True)
for label, ticker in TICKERS.items():
    df = download_session(ticker, SESSION_DATE)
    path = DATA_DIR / f"{ticker}_{SESSION_DATE}_1m.csv"
    df.to_csv(path)
    print(f"{ticker:6s} ({label:8s}) -> {len(df):>3} barras -> {path.name}")