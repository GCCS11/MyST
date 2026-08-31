

import numpy as np
import pandas as pd
import yfinance as yf

BENCHMARK = "AAPL"

CANDIDATES = [
    "CULP",   # textiles
    "BSET",   # muebles
    "UTMD",   # dispositivos medicos
    "FONR",   # imagenologia
    "IEHC",   # conectores electronicos
    "PBHC",   # banca regional
    "CCRD",   # pagos
    "SIF",    # componentes industriales
    "AMS",    # equipo medico
    "TAYD",   # amortiguadores sismicos
    "SGC",    # uniformes
    "PLBC",   # banca regional
]

PERIOD = "3mo"


def liquidity_metrics(ticker: str) -> dict | None:
    """Cálculo de metricas de liquidez sobre barras diarias. """
    df = yf.download(ticker, period=PERIOD, interval="1d",
                     progress=False, auto_adjust=True)
    if df.empty or len(df) < 20:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    volume = df["Volume"].astype(float)
    close = df["Close"].astype(float)
    rel_range = ((df["High"] - df["Low"]) / df["Close"]).astype(float)
    returns = np.log(close / close.shift(1)).dropna()

    return {
        "ticker": ticker,
        "days": len(df),
        "mean_volume": volume.mean(),
        "adv_usd": (volume * close).mean(),
        "zero_volume_days": int((volume == 0).sum()),
        "mean_rel_range": rel_range.mean(),
        "daily_vol": returns.std(),
    }


rows = []
for ticker in [BENCHMARK] + CANDIDATES:
    m = liquidity_metrics(ticker)
    if m is None:
        print(f"{ticker:6s} -> sin datos suficientes, se descarta")
        continue
    rows.append(m)

table = pd.DataFrame(rows).set_index("ticker").sort_values("adv_usd")

pd.set_option("display.float_format",
              lambda x: f"{x:,.6f}" if abs(x) < 1 else f"{x:,.0f}")
print()
print(table)
print()
print(f"ADV de {BENCHMARK}: ${table.loc[BENCHMARK, 'adv_usd']:,.0f}")