# Act 04 - Indicadores tecnicos

Calculo de indicadores tecnicos sobre BTC-USD usando la libreria `ta`, revision
de nulos, graficas, y analisis de rezago, fallas, correlacion y look-ahead.

## Datos

- Archivo: `data/BTC-USD_1d.csv`
- Fuente: yfinance, velas diarias, `auto_adjust=True`
- Rango: 2020-01-01 a 2026-09-11 (2,446 barras)
- Sin nulos y sin dias faltantes

Los datos estan congelados en el csv para que los resultados no cambien cada vez
que se corre el notebook.

## Indicadores

Los 7 vistos en clase (SMA, EMA, Bollinger, ATR, RSI, MACD, Stochastic) mas ADX,
OBV y VWAP. `add_indicators(df)` deja el DataFrame en 25 columnas.

## Resultados

**Nulos.** Todos son calentamiento al inicio de cada ventana: `sma_100` necesita
99 barras, `macd_signal` 33 y `sma_10` solo 9. No hay huecos a media serie.

Un detalle de la libreria: `ta` rellena el calentamiento del ATR y del ADX con
0.0 en lugar de NaN, aun pasando `fillna=False`. Sin corregirlo, el reporte de
nulos dice que esas columnas no tienen ninguno y esos ceros entran a la matriz
de correlacion como si fueran datos reales.

**Pregunta 1, sma_10 vs sma_100.**

| | sma_10 | sma_100 |
|---|---|---|
| rezago | 4 dias | 50 dias |
| cruces con el precio | 409 | 87 |
| señales que se revierten en 5 dias | 60% | 53% |

El rezago coincide con la teoria de (n-1)/2 barras. La `sma_10` reacciona 46
dias antes pero cruza 4.7 veces mas seguido.

**Pregunta 2, tramos donde falla cada indicador.**

| Indicador | Tramo | Que paso |
|---|---|---|
| RSI | 2020-12-17 a 12-20 | RSI en 75 a 79 y el precio hizo +71% en 20 dias |
| MACD | 2021-04-30 | Cruce alcista y cayo 29.4% en 20 dias |
| Bollinger | 2023-01-08 a 01-16 | 9 dias cerrando sobre la banda alta, +23.9% |
| sma_10 | 2023-04-09 a 06-07 | 22 cruces en 60 dias y quedo en -7% |

Los dos tipos de error son opuestos y el ADX indica cual aplica: con ADX alto
(46.8 en el tramo del RSI) fallan los osciladores, y con ADX bajo (22.6 en el
lateral de 2023) fallan las medias y el MACD.

**Pregunta 3, correlacion.** Hay dos bloques. El de nivel (`close`, `sma_10`,
`sma_20`, `ema_20`, `vwap_14`) con correlaciones de 0.99 a 1.00, y el de momentum
(`rsi_14`, `stoch_k`, `stoch_d`, `bb_pct`) con 0.87 a 0.92. Los unicos que
aportan algo distinto son el `adx` y el `obv`.

El ATR sale 0.79 contra el precio, pero es artefacto de unidades: normalizado
entre el precio baja a -0.16.

**Pregunta 4, look-ahead.** Los 9 indicadores dan diferencia exactamente 0 al
recalcularlos sobre `df.iloc[:t+1]`. Ninguno mira al futuro. Como control se
agregaron dos indicadores mal hechos a proposito, una media centrada y un
z-score con estadisticos de toda la muestra, y ahi la prueba si detecta el
problema.

## Archivos

- `src/indicators.py` - indicadores, `add_indicators`, `nan_report`, `check_lookahead`
- `src/plots.py` - graficas de overlays, RSI, MACD, panel y matriz de correlacion
- `src/data.py` - carga del csv
- `scripts/download_data.py` - descarga los datos de yfinance
- `act04_indicators.ipynb` - notebook con los 4 pasos y las 4 preguntas
- `outputs/` - las 5 figuras

## Como correrlo

```
pip install -r requirements.txt
python scripts/download_data.py
jupyter notebook
```
