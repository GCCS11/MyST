
import numpy as np
import pandas as pd
import yfinance as yf

BENCHMARK = "AAPL"
CANDIDATES = ["CULP", "BSET", "UTMD", "IEHC", "PBHC",
              "SIF", "AMS", "TAYD", "SGC", "PLBC"]
SESSION_MINUTES = 390


def _flatten(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def daily_metrics(ticker):
    df = yf.download(ticker, period="3mo", interval="1d",
                     progress=False, auto_adjust=True)
    if df.empty or len(df) < 20:
        return None
    df = _flatten(df)
    close = df["Close"].astype(float)
    volume = df["Volume"].astype(float)
    returns = np.log(close / close.shift(1)).dropna()
    return {
        "adv_usd": (volume * close).mean(),
        "zero_vol_days": int((volume == 0).sum()),
        "rel_range": ((df["High"] - df["Low"]) / close).mean(),
        "daily_vol": returns.std(),
    }


def intraday_coverage(ticker):
    """yfinance omite el minuto si no hubo trades: menos barras, no barras planas."""
    df = yf.download(ticker, period="5d", interval="1m",
                     progress=False, auto_adjust=True)
    if df.empty:
        return None
    df = _flatten(df)
    per_day = df.groupby(df.index.date).size()
    return {
        "bars_max_day": int(per_day.max()),
        "coverage": per_day.max() / SESSION_MINUTES,
        "flat_bars": float((df["High"] == df["Low"]).mean()),
    }


rows = []
for ticker in [BENCHMARK] + CANDIDATES:
    daily, intra = daily_metrics(ticker), intraday_coverage(ticker)
    if daily is None or intra is None:
        print(f"{ticker:6s} -> sin datos, se descarta")
        continue
    rows.append({"ticker": ticker, **daily, **intra})

table = pd.DataFrame(rows).set_index("ticker").sort_values("adv_usd")
pd.set_option("display.float_format",
              lambda x: f"{x:,.4f}" if abs(x) < 1 else f"{x:,.0f}")
print(f"\n{table}\n")
print("Coverage entre 0.40 y 0.90:",
      table[table["coverage"].between(0.40, 0.90)].index.tolist())