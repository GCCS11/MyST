
import pandas as pd


def bar_range(df, normalize=True):
    """Rango high-low por barra. """
    rng = df["High"] - df["Low"]
    return rng / df["Close"] if normalize else rng


def coverage_stats(df, session_minutes=390):
    """cuenta barras reportadas"""
    zero_vol = int((df["Volume"] == 0).sum())
    return {
        "bars_reported": len(df),
        "zero_volume_bars": zero_vol,
        "bars_with_trades": len(df) - zero_vol,
        "coverage": len(df) / session_minutes,
        "effective_coverage": (len(df) - zero_vol) / session_minutes,
    }


def drop_zero_volume(df):
    return df[df["Volume"] > 0]