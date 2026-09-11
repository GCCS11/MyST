
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

COLORES = {
    "close": "#1f1f1f",
    "sma_10": "#1b6ca8",
    "sma_20": "#2e8b57",
    "sma_100": "#c2382c",
    "ema_20": "#e08b00",
    "vwap_14": "#7b4fa8",
    "banda": "#8c8c8c",
}


def _slice(df: pd.DataFrame, start=None, end=None) -> pd.DataFrame:
    return df.loc[start:end]


def plot_overlays(df: pd.DataFrame, cols=("sma_10", "sma_100"),
                  bandas: bool = True, start=None, end=None) -> plt.Figure:
    d = _slice(df, start, end)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(d.index, d["close"], color=COLORES["close"], lw=1.0, label="Cierre")
    if bandas and {"bb_high", "bb_low"} <= set(d.columns):
        ax.fill_between(d.index, d["bb_low"], d["bb_high"],
                        color=COLORES["banda"], alpha=0.18,
                        label="Bollinger (20, 2σ)")
    for c in cols:
        if c in d.columns:
            ax.plot(d.index, d[c], color=COLORES.get(c), lw=1.4, label=c)
    ax.set_title("Precio BTC-USD con overlays")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio (USD)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_rsi(df: pd.DataFrame, start=None, end=None) -> plt.Figure:
    d = _slice(df, start, end)
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(d.index, d["rsi_14"], color="#1b6ca8", lw=1.2, label="RSI(14)")
    ax.axhline(70, color="#c2382c", ls="--", lw=1.0, label="Sobrecompra (70)")
    ax.axhline(30, color="#2e8b57", ls="--", lw=1.0, label="Sobreventa (30)")
    ax.axhspan(70, 100, color="#c2382c", alpha=0.07)
    ax.axhspan(0, 30, color="#2e8b57", alpha=0.07)
    ax.set_ylim(0, 100)
    ax.set_title("RSI (14)")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("RSI")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", ncol=3, fontsize=8)
    fig.tight_layout()
    return fig


def plot_macd(df: pd.DataFrame, start=None, end=None) -> plt.Figure:
    d = _slice(df, start, end)
    fig, ax = plt.subplots(figsize=(12, 3.5))
    colores = ["#2e8b57" if v >= 0 else "#c2382c" for v in d["macd_hist"].fillna(0)]
    ax.bar(d.index, d["macd_hist"], color=colores, alpha=0.45, width=1.0,
           label="Histograma")
    ax.plot(d.index, d["macd"], color="#1b6ca8", lw=1.2, label="MACD")
    ax.plot(d.index, d["macd_signal"], color="#e08b00", lw=1.2, label="Señal")
    ax.axhline(0, color="black", lw=0.8, ls=":")
    ax.set_title("MACD (12, 26, 9)")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("USD")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", ncol=3, fontsize=8)
    fig.tight_layout()
    return fig


def plot_panel(df: pd.DataFrame, start=None, end=None) -> plt.Figure:
    d = _slice(df, start, end)
    fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True,
                             gridspec_kw={"height_ratios": [3, 1.2, 1.2, 1.2]})
    ax = axes[0]
    ax.plot(d.index, d["close"], color=COLORES["close"], lw=1.0, label="Cierre")
    ax.fill_between(d.index, d["bb_low"], d["bb_high"], color=COLORES["banda"],
                    alpha=0.18, label="Bollinger (20, 2σ)")
    for c in ("sma_10", "sma_100"):
        ax.plot(d.index, d[c], color=COLORES.get(c), lw=1.3, label=c)
    ax.set_ylabel("Precio (USD)")
    ax.set_title("BTC-USD: precio e indicadores")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", ncol=4, fontsize=8)

    ax = axes[1]
    ax.plot(d.index, d["rsi_14"], color="#1b6ca8", lw=1.1)
    ax.axhline(70, color="#c2382c", ls="--", lw=1.0)
    ax.axhline(30, color="#2e8b57", ls="--", lw=1.0)
    ax.set_ylim(0, 100)
    ax.set_ylabel("RSI(14)")
    ax.grid(alpha=0.3)

    ax = axes[2]
    colores = ["#2e8b57" if v >= 0 else "#c2382c" for v in d["macd_hist"].fillna(0)]
    ax.bar(d.index, d["macd_hist"], color=colores, alpha=0.45, width=1.0)
    ax.plot(d.index, d["macd"], color="#1b6ca8", lw=1.1)
    ax.plot(d.index, d["macd_signal"], color="#e08b00", lw=1.1)
    ax.axhline(0, color="black", lw=0.8, ls=":")
    ax.set_ylabel("MACD")
    ax.grid(alpha=0.3)

    ax = axes[3]
    ax.plot(d.index, d["atr_14"], color="#7b4fa8", lw=1.1)
    ax.set_ylabel("ATR(14)")
    ax.set_xlabel("Fecha")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig


def plot_corr(df: pd.DataFrame, cols=None) -> plt.Figure:
    d = df[cols] if cols is not None else df
    corr = d.corr()
    fig, ax = plt.subplots(figsize=(10, 9))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)))
    ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns, rotation=90, fontsize=8)
    ax.set_yticklabels(corr.index, fontsize=8)
    for i in range(len(corr)):
        for j in range(len(corr)):
            v = corr.iloc[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6,
                    color="white" if abs(v) > 0.6 else "black")
    ax.set_title("Matriz de correlacion de los indicadores")
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    return fig


def guardar(fig: plt.Figure, ruta: Path, dpi: int = 150) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return ruta
