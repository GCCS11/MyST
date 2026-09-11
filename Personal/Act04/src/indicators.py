
import numpy as np
import pandas as pd
import ta


def sma(df: pd.DataFrame, window: int = 20) -> pd.Series:
    return ta.trend.SMAIndicator(df["close"], window=window).sma_indicator()


def ema(df: pd.DataFrame, window: int = 20) -> pd.Series:
    return ta.trend.EMAIndicator(df["close"], window=window).ema_indicator()


def bollinger(df: pd.DataFrame, window: int = 20, n_std: float = 2.0) -> pd.DataFrame:
    bb = ta.volatility.BollingerBands(df["close"], window=window, window_dev=n_std)
    return pd.DataFrame({
        "bb_high": bb.bollinger_hband(),
        "bb_mid": bb.bollinger_mavg(),
        "bb_low": bb.bollinger_lband(),
        "bb_pct": bb.bollinger_pband(),
    }, index=df.index)


def atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    a = ta.volatility.AverageTrueRange(
        df["high"], df["low"], df["close"], window=window
    ).average_true_range()
    a.iloc[:window - 1] = np.nan
    return a


def rsi(df: pd.DataFrame, window: int = 14) -> pd.Series:
    return ta.momentum.RSIIndicator(df["close"], window=window).rsi()


def macd(df: pd.DataFrame, fast: int = 12, slow: int = 26,
         signal: int = 9) -> pd.DataFrame:
    m = ta.trend.MACD(df["close"], window_slow=slow, window_fast=fast,
                      window_sign=signal)
    return pd.DataFrame({
        "macd": m.macd(),
        "macd_signal": m.macd_signal(),
        "macd_hist": m.macd_diff(),
    }, index=df.index)


def stochastic(df: pd.DataFrame, window: int = 14,
               smooth: int = 3) -> pd.DataFrame:
    st = ta.momentum.StochasticOscillator(
        df["high"], df["low"], df["close"], window=window, smooth_window=smooth
    )
    return pd.DataFrame({
        "stoch_k": st.stoch(),
        "stoch_d": st.stoch_signal(),
    }, index=df.index)


def adx(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    a = ta.trend.ADXIndicator(df["high"], df["low"], df["close"], window=window)
    out = pd.DataFrame({
        "adx": a.adx(),
        "adx_pos": a.adx_pos(),
        "adx_neg": a.adx_neg(),
    }, index=df.index)
    out.iloc[:2 * window - 1, out.columns.get_loc("adx")] = np.nan
    out.iloc[:window + 1, [out.columns.get_loc("adx_pos"),
                           out.columns.get_loc("adx_neg")]] = np.nan
    return out


def obv(df: pd.DataFrame) -> pd.Series:
    return ta.volume.OnBalanceVolumeIndicator(
        df["close"], df["volume"]
    ).on_balance_volume()


def vwap(df: pd.DataFrame, window: int = 14) -> pd.Series:
    return ta.volume.VolumeWeightedAveragePrice(
        df["high"], df["low"], df["close"], df["volume"], window=window
    ).volume_weighted_average_price()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["sma_10"] = sma(df, 10)
    out["sma_20"] = sma(df, 20)
    out["sma_100"] = sma(df, 100)
    out["ema_20"] = ema(df, 20)
    out = out.join(bollinger(df, window=20, n_std=2.0))
    out["atr_14"] = atr(df, 14)
    out["rsi_14"] = rsi(df, 14)
    out = out.join(macd(df))
    out = out.join(stochastic(df))
    out = out.join(adx(df))
    out["obv"] = obv(df)
    out["vwap_14"] = vwap(df, 14)
    return out


def nan_report(df: pd.DataFrame) -> pd.DataFrame:
    rep = pd.DataFrame({
        "n_nan": df.isna().sum(),
        "pct_nan": (df.isna().mean() * 100).round(2),
        "first_valid": df.apply(lambda s: s.first_valid_index()),
    })
    rep["nan_interior"] = df.apply(
        lambda s: int(s.loc[s.first_valid_index():].isna().sum())
        if s.first_valid_index() is not None else int(s.isna().sum())
    )
    return rep


def centered_ma(df: pd.DataFrame, window: int = 20) -> pd.Series:
    return df["close"].rolling(window, center=True).mean()


def zscore_muestra(df: pd.DataFrame) -> pd.Series:
    return (df["close"] - df["close"].mean()) / df["close"].std()


def check_lookahead(df: pd.DataFrame, fn, ts) -> pd.DataFrame:
    completa = fn(df)
    filas = []
    for t in ts:
        parcial = fn(df.iloc[:t + 1])
        a, b = completa.iloc[t], parcial.iloc[-1]
        dif = abs(a - b)
        filas.append({
            "t": t,
            "fecha": df.index[t].date(),
            "completa": a,
            "hasta_t": b,
            "dif_abs": dif,
            "dif_rel_%": 100 * dif / abs(a) if a != 0 else np.nan,
        })
    return pd.DataFrame(filas).set_index("t")
